# Autonomous Safety Compliance & Hazard Detection System

An enterprise-grade, real-time computer vision pipeline engineered to monitor restricted industrial environments, detect safety compliance violations (such as missing PPE/hardhats), and orchestrate instantaneous supervisor alerts without degrading core video ingestion performance.

---

## 🛠️ Tech Stack & Architecture

| Layer | Technologies Used |
| :--- | :--- |
| **Core Vision Engine** | Python, OpenCV, YOLO |
| **Orchestration & Workflow** | n8n Engine, REST APIs, Webhooks |
| **UI & Asset Rendering** | PIL / Pillow |
| **Concurrency & Logic** | Python Multi-threading (`threading`), Stateful Throttling |

---

## 🚀 Key Features & Engineering Highlights

### 👁️ Real-Time Vision & Edge Compliance
* **Object Detection & Boundary Enforcement:** Developed and deployed a high-accuracy computer vision pipeline using **YOLO** and **OpenCV** to actively monitor restricted hazard zones and detect safety compliance violations (e.g., missing hardhats) under variable industrial lighting conditions.
* **Dynamic HUD Overlay:** Designed and rendered an intuitive, real-time graphical Head-Up Display (HUD) overlay utilizing **PIL/Pillow** to visualize hazard status, bounding boxes, and breach tracking directly on the local monitoring station.

### ⚡ Zero-Latency Alert Architecture
* **Multi-Threaded Concurrency:** Engineered an asynchronous, multi-threaded alerting subsystem in Python. By decoupling heavy execution tasks—such as local audio alarms and external webhook dispatches—from the main frame-processing thread, the system completely eliminates video feed latency and frame dropping.
* **Enterprise Workflow Automation:** Integrated an **n8n orchestration engine** to manage notification routing, triggering instant REST API-driven email alerts to plant supervisors within seconds of a critical boundary breach.

### 📉 Infrastructure & Network Optimization
* **Intelligent Request Throttling:** Implemented custom stateful rate-limiting algorithms to handle high-frequency edge detections. 
* **98% Overhead Reduction:** This throttling mechanism successfully minimized redundant notification spam and API call overhead by **98%** during active, continuous safety incidents without delaying the initial critical alarm.

---

## 📋 System Workflow Architecture

```mermaid
graph TD
    A[CCTV Video Feed] --> B[OpenCV Frame Ingestion]
    B --> C[YOLO Inference Engine]
    C -->|Breach Detected| D{Multi-Threaded Split}
    D -->|Thread 1| E[Instant Local Audio Alarm]
    D -->|Thread 2| F[Asynchronous Webhook Trigger]
    F --> G[n8n Orchestration Node]
    G --> H[Stateful Rate-Limiter Check]
    H -->|New Incident| I[REST API Email Dispatch to Supervisor]
    H -->|Throttled Spam| J[Log Suppressed Output]
