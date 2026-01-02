import random
import csv

NUM_MUESTRAS = 1000
salida = "dataset.csv"

def generar_muestra(estado):
    if estado == "ralenti":
        velocidad = 0
        rpm = random.randint(700, 950)
        acelerador = random.randint(5, 15)
        carga = random.randint(10, 25)
        delta_v = 0

    elif estado == "aceleracion":
        velocidad = random.randint(10, 80)
        rpm = random.randint(1500, 4000)
        acelerador = random.randint(40, 90)
        carga = random.randint(40, 80)
        delta_v = random.randint(4, 20)

    elif estado == "frenado":
        velocidad = random.randint(10, 80)
        rpm = random.randint(1200, 3000)
        acelerador = random.randint(0, 10)
        carga = random.randint(10, 40)
        delta_v = random.randint(-20, -4)

    else:  # velocidad_constante
        velocidad = random.randint(20, 100)
        rpm = random.randint(1800, 3000)
        acelerador = random.randint(10, 30)
        carga = random.randint(25, 50)
        delta_v = random.randint(-2, 2)

    return [rpm, velocidad, acelerador, carga, delta_v, estado]

estados = ["ralenti", "aceleracion", "frenado", "velocidad_constante"]

with open(salida, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "rpm",
        "velocidad",
        "acelerador",
        "carga_motor",
        "delta_velocidad",
        "estado"
    ])

    for _ in range(NUM_MUESTRAS):
        estado = random.choice(estados)
        writer.writerow(generar_muestra(estado))

print("Dataset generado:", salida)
