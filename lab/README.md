
🚦 AI Traffic Incident Detection MVP
A real-time accident detection system utilizing a V-JEPA (Visual Joint-Embedding Predictive Architecture) backbone and a lightweight MLP Probe for high-efficiency classification.

🏗️ System Architecture: Distributed Inference
This MVP is designed using a Decoupled Edge-Cloud Architecture. This mimics a real-world deployment where heavy computation is handled at the source, and decision-making is centralized.

The Edge (Simulation Engine): Mimics a "Smart Camera." Instead of streaming heavy raw video, it processes video through a frozen V-JEPA backbone and sends compact visual embeddings to the backend.

The Brain (FastAPI Backend): Receives embeddings in real-time and performs sub-millisecond inference using a trained Classification Probe.

The UI (Frontend): A live dashboard that displays the incident category, confidence scores, and a synchronized video replay of the detected event.

🧠 Model Strategy
- Backbone: Frozen VL-JEPA (Video-JEPA). Chosen for its superior understanding of world physics and temporal motion over static image models.
- Classification: A lightweight MLP Probe trained on a mix of Real-world and Synthetic data.
- Domain Adaptation: By merging 2,211 synthetic samples with a limited real-world training set (500 samples), the model achieves high robustness against Geographic Domain Shift.

📊 Dataset & Evaluation
- In-Distribution Split: Standard benchmark for baseline performance.
- Geo-Aware Split: Critical evaluation for real-world deployment, testing generalization across different cities and camera angles.
- Prod Set: A curated, balanced "Gold Set" of 50 samples (10 per accident modality) reserved strictly for live demonstration and system validation.

🚀 One-Click Deployment
The entire stack is containerized for consistent evaluation.
bash
# Launch the Backend, Frontend, and Database
docker-compose up --build

🛠️ Project Structure
ai_research/: Notebooks covering data imbalance analysis and Probe training.
backend/: FastAPI server handling real-time embedding inference and SQLite history.
backend/simulation/: The generator.py script that simulates live camera feeds.
frontend/: React-based dashboard for incident monitoring.