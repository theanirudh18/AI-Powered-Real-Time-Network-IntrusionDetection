# AI-Powered Real-Time Network Intrusion Detection System (AI-RealTime-IDS)

A **hybrid AI-powered Network Intrusion Detection System (NIDS)** that performs **real-time packet capture, flow-based feature extraction, deep learning inference (CNN + BiLSTM + Attention), and live attack monitoring through a Flask dashboard**.

The project combines **machine learning** with **behavior-based intrusion detection** to monitor network traffic in real time and identify suspicious activities such as **PortScan** and other network attack categories.

## Features

* Real-time packet capture using **Scapy**
* Flow-based traffic analysis
* **47 network traffic features** extracted in real time
* **CNN + BiLSTM + Attention** deep learning architecture
* **Behavior-based PortScan detection**
* Live Flask dashboard
* Real-time detection feed
* Modular preprocessing, training, and deployment pipeline
* Easy extension for additional attack signatures

## Screenshots

### Real-Time Dashboard

![Real-Time Dashboard](screenshots/dashboard.png)

## System Architecture

```text
Network Traffic
       |
       v
Packet Capture (Scapy)
       |
       v
Flow Manager
       |
       +----------------------+
       |                      |
       v                      v
Feature Extraction      PortScan Detector
       |                      |
       v                      |
CNN + BiLSTM + Attention Model |
       |                      |
       +----------+-----------+
                  |
                  v
          Flask Dashboard
                  |
                  v
         Live Attack Monitoring
```

## Project Structure

```text
AI-RealTime-IDS/
├── app.py
├── config.py
├── dashboard/
├── packet_capture/
├── preprocessing/
├── realtime/
├── training/
├── static/
├── templates/
├── utils/
├── dataset/
│   └── metadata/
├── screenshots/
├── requirements.txt
└── README.md
```

## Technologies Used

* Python 3.11
* Flask
* Scapy
* TensorFlow / Keras
* NumPy
* Pandas
* scikit-learn
* Joblib
* HTML, CSS, JavaScript

## Deep Learning Model

The detection engine uses a hybrid architecture:

* **CNN** for local packet-pattern extraction
* **BiLSTM** for temporal sequence learning
* **Bahdanau Attention** for adaptive feature weighting

This architecture is designed to capture both **spatial** and **temporal characteristics** of network traffic flows.

## Dataset

The model was trained using traffic derived from the **CICIDS2017** dataset.

Supported attack categories include:

* BENIGN
* Bot
* DDoS
* DoS GoldenEye
* DoS Hulk
* DoS Slowhttptest
* DoS Slowloris
* FTP-Patator
* Heartbleed
* Infiltration
* PortScan
* SSH-Patator
* Web Attack - Brute Force
* Web Attack - SQL Injection
* Web Attack - XSS

## Installation

### Clone the repository

```bash
git clone https://github.com/theanirudh18/AI-Powered-Real-Time-Network-IntrusionDetection.git
cd AI-Powered-Real-Time-Network-IntrusionDetection
```

### Create a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

## Running the Project

Start the IDS:

```bash
sudo python app.py
```

The dashboard will be available at:

```text
http://127.0.0.1:8000
```

## Real-Time PortScan Test

From another machine (or a test device on the same network), run:

```bash
nmap -Pn -T4 -p 1-1000 <target-ip>
```

The system performs:

* Real-time packet capture
* Flow generation
* Feature extraction
* AI inference
* PortScan behavioral detection
* Live dashboard updates

## Current Status

### Implemented

* Real-time packet capture
* Flow management
* Feature extraction (47 features)
* CNN + BiLSTM + Attention inference
* Live Flask dashboard
* Behavioral PortScan detection

### Under Development

* ML-based PortScan classification alignment
* Additional attack signatures
* Dashboard visualization enhancements
* Performance optimization

## Future Improvements

* Retrain the model with real-time generated flows
* Integrate Zeek/Suricata logs
* Add email/SMS alert notifications
* REST API support
* Docker deployment
* Grafana / Prometheus integration
* Multi-interface monitoring

## Disclaimer

This project is intended for **educational, research, and authorized cybersecurity testing purposes only**. Use only on networks and systems for which you have explicit permission.

## Author

**Anirudh Singh**

GitHub: https://github.com/theanirudh18

---

If you find this project useful, consider giving it a **star** on GitHub.
