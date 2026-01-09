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
