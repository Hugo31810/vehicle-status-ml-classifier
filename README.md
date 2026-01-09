# 🚗 IoT Vehicle Status ML Classifier

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python)
![Raspberry Pi](https://img.shields.io/badge/Raspberry%20Pi-Edge-C51A4A?style=for-the-badge&logo=raspberrypi)
![MQTT](https://img.shields.io/badge/MQTT-Protocol-660066?style=for-the-badge&logo=eclipse-mosquitto)
![Machine Learning](https://img.shields.io/badge/AI-Scikit--Learn-orange?style=for-the-badge&logo=scikit-learn)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

> **Edge Computing and Machine Learning applied to real-time vehicle telemetry.**

This project implements a complete **End-to-End IoT solution** that acquires vehicle telemetry via OBD-II, processes it on the edge (Raspberry Pi), and uses a **Machine Learning model** to classify the driving state in real-time. The results are transmitted via **4G/LTE** to a cloud dashboard for visualization.

---

## 📸 Demo & Visualization

**Live Dashboard:** [View Dashboard Here](https://hugo31810.github.io/vehicle-status-ml-classifier/)

*(Place a screenshot of your dashboard here)*
`![Dashboard Preview](assets/dashboard_screenshot.png)`

---

## 💡 Project Overview

In the context of **Ambient Intelligence** and **Smart Transportation**, this project moves beyond simple data logging. It demonstrates **Edge Intelligence** by enabling the device to understand *what* the vehicle is doing, not just reporting raw numbers.

**Key Capabilities:**
* **OBD-II Acquisition:** Reads live data from the vehicle's CAN bus.
* **Auto-Labeling Pipeline:** Automatically generates labeled datasets using heuristic rules, eliminating manual tagging.
* **Edge Inference:** Runs a Random Forest classifier locally on the Raspberry Pi.
* **4G Connectivity:** Independent of Wi-Fi networks using the Air780EU module.
* **Decoupled Architecture:** Uses MQTT to separate data generation from visualization.

---

## 🏗️ System Architecture

 The system follows a distributed architecture where the heavy lifting (inference) is done at the edge to reduce latency and bandwidth usage.

```mermaid
graph LR
    A[Vehicle OBD-II] -->|CAN Bus| B(MCP2515 + TJA1050)
    B -->|SPI| C{Raspberry Pi<br/>Edge Device}
    
    subgraph Edge Computing
    C -->|1. Acquire| D[Data Processing]
    D -->|2. Classify| E[ML Model <br/> Random Forest]
    end
    
    E -->|JSON Payload| F[MQTT Publisher]
    F -->|4G LTE / WiFi| G((MQTT Broker))
    G -->|Subscribe| H[Web Dashboard]
    H -->|Visualize| I[User]

```

---

## 🧠 Machine Learning Approach

The goal is to classify the vehicle's behavior into 4 distinct states.

### 1. The Dataset

The dataset is generated continuously by the device. Features are extracted and labeled automatically based on dynamic thresholds (heuristic rules).

| Feature | Description |
| --- | --- |
| `speed` | Vehicle speed (km/h) |
| `rpm` | Engine Revolutions Per Minute |
| `throttle` | Accelerator pedal position (%) |
| `load` | Engine load (%) |
| `delta_speed` | Acceleration (derived from speed changes) |

### 2. The Classes

* 🟢 **Ralenti (Idle):** Vehicle stopped, engine running.
* 🔵 **Velocidad Constante (Cruising):** Stable speed, low variance.
* 🟡 **Aceleracion (Acceleration):** Positive delta speed, high throttle.
* 🔴 **Frenado (Braking):** Negative delta speed, sudden drop.

### 3. The Model

A **Random Forest Classifier** was selected for its robustness against noise and low computational cost during inference, making it ideal for the Raspberry Pi.

---

## 🛠️ Hardware & Tech Stack

### Hardware

* **Computing:** Raspberry Pi (Edge Device).
* **Interface:** MCP2515 CAN Bus Controller + TJA1050 Transceiver.
* **Connectivity:** Air780EU 4G LTE Module (UART).
* **Vehicle:** Any car with standard OBD-II support.

### Software

* **Language:** Python 3.
* **Libraries:** `python-can`, `paho-mqtt`, `pandas`, `scikit-learn`.
* **Web:** HTML5, CSS3, JavaScript (MQTT over WebSockets).
* **Tools:** Mosquitto Broker, Git.

---

## 🚀 Installation & Usage

### 1. Prerequisites

Ensure your Raspberry Pi has the CAN interface enabled in `/boot/config.txt`:

```bash
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25

```

### 2. Clone and Install

```bash
git clone [https://github.com/Hugo31810/vehicle-status-ml-classifier.git](https://github.com/Hugo31810/vehicle-status-ml-classifier.git)
cd vehicle-status-ml-classifier
pip install -r requirements.txt

```

### 3. Run the System

To start data acquisition and inference:

```bash
python main.py

```

To run the dataset generator (for training new models):

```bash
python data_generator.py

```

---

## 📂 Project Structure

```text
.
├── dataset/                # Generated CSV datasets
├── models/                 # Trained .pkl models
├── src/
│   ├── main.py             # Main execution script
│   ├── data_generator.py   # Script for creating datasets
│   ├── inference.py        # ML loading and prediction logic
│   └── mqtt_client.py      # MQTT communication handler
├── dashboard/              # Web interface (HTML/JS)
├── requirements.txt        # Python dependencies
└── README.md

```

---

## 🔮 Future Improvements

* **Deep Learning:** Implementation of LSTM (Long Short-Term Memory) networks to analyze time-series sequences rather than instantaneous snapshots.
* **Anomaly Detection:** Unsupervised learning to detect mechanical failures or dangerous driving.
* **Integration:** Connection with ADAS (Advanced Driver Assistance Systems).

---

## 👨‍💻 Author

**Hugo Salvador Aizpún** *Degree in Artificial Intelligence* *Subject: Ambient Intelligence and Ubiquitous Computing*

[GitHub Profile](https://www.google.com/search?q=https://github.com/Hugo31810)

```

---

### ¿Qué mejoras incluye este README?

1.  **Badges (Escudos):** Dan un aspecto profesional inmediato y resumen las tecnologías.
2.  **Contexto Académico/Profesional:** La introducción "vende" el proyecto no solo como código, sino como una solución de ingeniería completa.
3.  **Diagrama Mermaid:** GitHub renderiza automáticamente el bloque `mermaid` como un diagrama de flujo. Es mucho mejor que el arte ASCII y se ve muy moderno.
4.  **Tablas:** Organizan la información de los datos de forma limpia.
5.  **Sección de Hardware:** Especifica los módulos (MCP2515, Air780EU) que mencionaste en la memoria, lo que demuestra conocimiento de bajo nivel.
6.  **Instrucciones de uso:** Imprescindible para que quien visite el repo sepa que es un proyecto funcional y reproducible.

```
