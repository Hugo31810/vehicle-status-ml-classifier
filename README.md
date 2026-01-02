

# IoT Vehicle status ML classifier

## Edge Computing and Machine Learning applied to vehicle telemetria

This project presents a complete Edge Computing system for vehicle telemetria acquisition, dataset generation, and real-time machine learning inference using data collected from the OBD-II interface.

The system is designed as an academic and professional portfolio project, integrating IoT, Edge Intelligence, Machine Learning, and real-time visualization.

---

## Project Overview

The solution is composed of:

- A vehicle telemetria acquisition system using OBD-II
- A Raspberry Pi acting as an edge device
- Real-time data processing and storage
- Automatic dataset generation and labeling
- A Machine Learning model for driving state classification
- Real-time inference executed at the edge
- Data transmission via MQTT
- A web-based dashboard for visualization

The project evolves from raw telemetria acquisition to Edge Intelligence, following a real-world IoT workflow.

---

## Driving State Classification

The system classifies the vehicle driving state into four classes:

- ralenti
- aceleracion
- frenado
- velocidad_constante

Classification is based on features extracted directly at the edge:

- Speed
- RPM
- Throttle position
- Engine load
- Speed variation (delta_speed)

The model is trained offline and deployed on the Raspberry Pi for real-time inference.

---

## System Architecture

Vehicle (OBD-II)
|
v
CAN Bus (MCP2515 + TJA1050)
|
v
Raspberry Pi (Edge Device)

* Data acquisition
* Preprocessing
* Dataset generation (CSV)
* ML inference
* MQTT publisher
  |
  v
  MQTT Broker
  |
  v
  Web Dashboard



---

## Dataset Generation

The dataset is generated automatically on the edge device and stored locally in CSV format:

```csv
speed,rpm,throttle,load,delta_speed,label
```

Labels are assigned using heuristic rules, enabling scalable dataset creation without manual labeling.

---

## Machine Learning

* Problem type: Supervised multi-class classification
* Model: Random Forest (exported as .pkl)
* Inference location: Edge device (Raspberry Pi)
* Latency: Low, no cloud dependency

This approach demonstrates a real Edge Intelligence use case.

---

## Dashboard

The web dashboard provides:

* Real-time telemetria visualization
* Live driving state inference
* Historical charts
* Remote access via 4G connectivity

The dashboard receives data through MQTT and updates dynamically.

---

## Technologies Used

* Python 3
* SocketCAN
* MQTT (Mosquitto)
* HTML, CSS, JavaScript
* Paho MQTT
* Scikit-learn
* Raspberry Pi
* MCP2515 CAN module
* Air780EU 4G LTE module

---


## Academic Context

This project was developed as part of an Edge Computing academic course, demonstrating:

* IoT system design
* Dataset generation
* Machine Learning integration
* Edge-based inference
* Real-time systems

---

## Future Work

* Larger real-world dataset collection
* Sequential models (LSTM)
* Anomaly detection
* Energy consumption optimization
* Integration with ADAS systems

---

## Links

* Live Dashboard
  https://hugo31810.github.io/vehicle-status-ml-classifier/

---

## Author

Hugo Salvador Aizpún
