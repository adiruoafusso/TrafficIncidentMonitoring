# 🚦 Traffic Incident Monitoring: V-JEPA Real-Time Detection

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-0.95+-green.svg) ![FastHTML](https://img.shields.io/badge/FastHTML-Modern-orange.svg) ![ONNX](https://img.shields.io/badge/ONNX-Runtime_Int8-blueviolet.svg) ![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)

**Traffic Incident Monitoring** is an end-to-end AI surveillance system designed to detect high-severity traffic events (collisions, congestion) in real-time. It utilizes a **Vision Transformer (V-JEPA2)** architecture, optimized via **ONNX Int8 Quantization** to run efficiently on standard CPUs without heavy GPU dependencies.

---

## 🚀 Quick Start (Docker)

The entire system (Backend, Frontend, and Database) is containerized for immediate deployment.

1.  **Clone the project:**
    ```bash
    git clone https://github.com/adiruoafusso/TrafficIncidentMonitoring.git
    cd TrafficIncidentMonitoring
    ```

2.  **Launch the System:**
    ```bash
    docker-compose up --build
    ```

3.  **Access the Dashboard:**
    *   **Live Dashboard:** [http://localhost:5001](http://localhost:5001)
    *   **API Documentation:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

🏗 System Architecture
The project follows a Microservices pattern designed for low latency and high portability.
Service
Tech Stack
Description
🧠 The Brain (Backend)
FastAPI + ONNX Runtime	Handles video ingestion, runs AI inference, and manages the SQLite event log. Uses async execution to prevent blocking.
👀 The Face (Frontend)
FastHTML (Python)	A Server-Side Rendered (SSR) dashboard. Uses HTMX for real-time polling without heavy JavaScript bundles.
🔬 The Lab (Research)
Jupyter + PyTorch	Contains the model training, validation, and ONNX conversion pipelines.
⚡ Engineering Highlights
1. AI Optimization (Quantization)
Instead of deploying a raw PyTorch model (~800MB + dependencies), this project utilizes Post-Training Quantization (INT8).
Model Format: ONNX (Open Neural Network Exchange).
Engine: onnxruntime (CPU Optimized).
Impact:
Docker Image size reduced by 70%.
Inference latency reduced by ~3x on CPU.
Accuracy loss < 1.5%.
2. Real-World Data Simulation
The system does not rely on random numbers. The backend/static folder is hydrated with actual video samples extracted from the model's test set tensors (prod.pt), ensuring the demo reflects real model performance on unseen data.
3. Shared Type Safety
Both the Backend and Frontend utilize Pydantic models (models.py) to share data schemas. This ensures that the data contract (Events, Alerts, Logs) is strictly typed and validated on both ends of the network.

📂 Project Structure

traffic_incident_monitoring/
├── docker-compose.yml       # Orchestration
├── backend/                 # FastAPI Service
│   ├── models.py            # Shared Pydantic Schemas (Source of Truth)
│   ├── ai_engine.py         # ONNX Inference Logic
│   ├── main.py              # API Routes
│   ├── database.py          # SQLite DAL
│   ├── model_int8.onnx      # Quantized Model Artifact
│   └── static/              # Video storage
├── frontend/                # FastHTML Dashboard
│   ├── models.py            # Shared Pydantic Schemas (Consumer)
│   ├── main.py              # UI Components & Polling Logic
│   └── Dockerfile
└── lab/                     # Data Science Work
    ├── experiment.ipynb     # Training/Validation Notebook
    ├── convert_model.py     # ONNX Conversion Script
    └── extract_stream.py    # Tensor -> Video converter

🧪 Running the Benchmarks
To verify the speedup of the Quantized model vs the Original PyTorch model:
1. Navigate to lab/.
2. Run the benchmark script:
    
    python benchmark_models.py
