#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time
import json
import csv
import random
import threading
from datetime import datetime

import serial
import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
import joblib
import pandas as pd

try:
    import can
except ImportError:
    can = None

try:
    import pynmea2
except ImportError:
    pynmea2 = None

# --- CONFIGURACIÓN GENERAL ---
MODO_ACTIVO = False  # Alternar según disponibilidad de hardware

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "coches/raspi1/telemetria"
CAN_INTERFACE = "can0"

GPS_PORT = "/dev/serial0"
GPS_BAUDRATE = 9600

gps_data = {"lat": 0.0, "lon": 0.0, "sats": 0}
gps_running = True

# --- CARGA DE CLASIFICADOR ---
DATA_MODEL = "vehicle_state_model.pkl"
try:
    classifier = joblib.load(DATA_MODEL)
    print("Módulo de clasificación listo.")
except Exception as e:
    print(f"Error de sistema: {e}")
    classifier = None

# Variables de control de flujo
last_velocity = 0
last_data_cache = {
    "rpm": 800, "speed": 0, "temp": 80, "oil": 80, "fuel": 50,
    "voltage": 12.5, "load": 10, "map": 100, "iat": 25,
    "throttle": 0, "lambda": 1.0, "timing": 10,
    "lat": 0.0, "lon": 0.0, "sats": 0
}


# --- CONTROL DE HARDWARE (GPS / CAN) ---
def read_gps():
    global gps_data, gps_running
    if not pynmea2: return
    try:
        ser = serial.Serial(GPS_PORT, GPS_BAUDRATE, timeout=1)
    except:
        return
    while gps_running:
        try:
            line = ser.readline().decode(errors="replace").strip()
            if line.startswith(("$GPGGA", "$GNGGA")):
                msg = pynmea2.parse(line)
                if msg.gps_qual > 0:
                    gps_data["lat"] = round(msg.latitude, 6)
                    gps_data["lon"] = round(msg.longitude, 6)
                    gps_data["sats"] = int(msg.num_sats)
        except:
            continue
    ser.close()


def setup_can():
    os.system("sudo ip link set can0 down")
    time.sleep(0.5)
    os.system("sudo ip link set can0 up type can bitrate 500000")


def send_pid(bus, pid):
    try:
        msg = can.Message(arbitration_id=0x7DF, data=[0x02, 0x01, pid, 0, 0, 0, 0, 0], is_extended_id=False)
        bus.send(msg)
        start = time.time()
        while time.time() - start < 0.5:
            r = bus.recv(0.01)
            if r and r.arbitration_id == 0x7E8 and r.data[2] == pid:
                return r.data
    except:
        return None


def parse_pid(pid, data):
    if not data: return None
    if pid == 0x0C: return int(((data[3] << 8) + data[4]) / 4)
    if pid == 0x0D: return int(data[3])
    if pid == 0x11: return round(data[3] * 100 / 255, 1)
    if pid == 0x2F: return round(data[3] * 100 / 255, 1)
    if pid == 0x42: return round(((data[3] << 8) + data[4]) / 1000, 1)
    if pid in (0x05, 0x5C, 0x0F): return int(data[3] - 40)
    if pid == 0x04: return round(data[3] * 100 / 255, 1)
    if pid == 0x0B: return int(data[3])
    if pid == 0x0E: return round(data[3] / 2 - 64, 1)
    if pid == 0x44: return round(((data[3] << 8) + data[4]) / 32768, 3)
    return None


def read_obd(bus):
    global last_data_cache
    pids = {"rpm": 0x0C, "speed": 0x0D, "temp": 0x05, "throttle": 0x11, "map": 0x0B,
            "oil": 0x5C, "iat": 0x0F, "timing": 0x0E, "lambda": 0x44, "fuel": 0x2F,
            "voltage": 0x42, "load": 0x04}
    data = last_data_cache.copy()
    for k, pid in pids.items():
        val = parse_pid(pid, send_pid(bus, pid))
        if val is not None: data[k] = val
        time.sleep(0.01)
    data.update(gps_data)
    last_data_cache = data.copy()
    return data


# --- GESTIÓN DE DATOS ---
def generate_data():
    return {
        "rpm": random.randint(1500, 4000),
        "speed": random.randint(40, 120),
        "temp": random.randint(85, 95),
        "oil": random.randint(90, 100),
        "fuel": random.randint(10, 20),
        "voltage": 14.1,
        "load": random.randint(20, 70),
        "map": 100, "iat": 30, "throttle": random.randint(10, 90),
        "lambda": 1.0, "timing": 15, **gps_data
    }


def process_status(data):
    global last_velocity
    if classifier is None: return "desconocido"

    v_actual = data.get("speed", 0)
    d_v = v_actual - last_velocity
    last_velocity = v_actual

    # Estructura de columnas requerida por el clasificador
    cols = ["rpm", "velocidad", "acelerador", "carga_motor", "delta_velocidad"]
    frame = pd.DataFrame([[
        data["rpm"],
        v_actual,
        data["throttle"],
        data["load"],
        d_v
    ]], columns=cols)

    try:
        res = classifier.predict(frame)[0]
        return str(res)
    except:
        return "error_proceso"


def create_log():
    path = "logs"
    os.makedirs(path, exist_ok=True)
    filename = os.path.join(path, f"telemetria_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv")
    with open(filename, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Timestamp", "RPM", "Speed", "Temp", "Oil", "Throttle", "Load", "Lat", "Lon", "Status"])
    return filename


def save_log(filename, data):
    try:
        with open(filename, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.now().strftime("%H:%M:%S"),
                data["rpm"], data["speed"], data["temp"], data["oil"],
                data["throttle"], data["load"], data["lat"], data["lon"], data["status"]
            ])
    except:
        pass


def connect_service():
    client = mqtt.Client(CallbackAPIVersion.VERSION1)
    while True:
        try:
            client.connect(BROKER, PORT, 60)
            client.loop_start()
            print("Servicio de red conectado.")
            return client
        except:
            time.sleep(2)


def main():
    global gps_running
    print("--- SISTEMA DE TELEMETRÍA INICIADO ---")

    if pynmea2 and MODO_ACTIVO:
        threading.Thread(target=read_gps, daemon=True).start()

    bus = None
    if MODO_ACTIVO and can:
        setup_can()
        bus = can.interface.Bus(channel=CAN_INTERFACE, bustype="socketcan")

    log_file = create_log()
    service_client = connect_service()

    try:
        while True:
            current_data = read_obd(bus) if MODO_ACTIVO else generate_data()

            # Clasificación de estado
            current_data["status"] = process_status(current_data)

            # Transmisión y registro
            service_client.publish(TOPIC, json.dumps(current_data))
            save_log(log_file, current_data)

            print(
                f"Update: {current_data['speed']} km/h | RPM: {current_data['rpm']} | Status: {current_data['status']}")
            time.sleep(1)

    except KeyboardInterrupt:
        gps_running = False
        service_client.loop_stop()
        service_client.disconnect()


if __name__ == "__main__":
    main()