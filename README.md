# Generic AI Kubernetes Troubleshooter

This project is a demo **AI-powered Kubernetes troubleshooting tool**.

It collects **Kubernetes namespace events**, sends them to a Python backend, and uses **Ollama LLM** to generate **root cause analysis and suggested fixes**.

The system contains:

* **React UI** – User interface for submitting cluster details
* **FastAPI Backend** – Collects Kubernetes events and calls Ollama
* **Ollama AI Model** – Generates troubleshooting suggestions
* **Docker Desktop Kubernetes** – Local Kubernetes cluster for testing

---

# Architecture

React UI
↓
FastAPI Backend
↓
Kubernetes API (events / pods)
↓
Ollama LLM
↓
AI Root Cause Analysis

---

# Prerequisites

Install the following:

* Node.js
* Python 3.9+
* Docker Desktop
* Kubernetes enabled in Docker Desktop
* Ollama installed

Tools used:

* React
* FastAPI
* Uvicorn
* Kubernetes Python Client
* Ollama

---

# Step 1 – Start Kubernetes

Enable Kubernetes inside **Docker Desktop**.

Verify cluster:

```
kubectl get nodes
```

Expected output:

```
docker-desktop Ready
```

---

# Step 2 – Start Ollama

Start Ollama server:

```
ollama serve
```

Check available models:

```
ollama list
```

If no model exists, pull one:

```
ollama pull mistral
```

---

# Step 3 – Run Python Backend

Navigate to backend folder:

```
cd backend
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the API server:

```
python -m uvicorn main:app --reload
```

Backend will run at:

```
http://localhost:8000
```

Swagger API documentation:

```
http://localhost:8000/docs
```

---

# Step 4 – Run React Frontend

Navigate to frontend folder:

```
cd frontend
```

Install dependencies:

```
npm install
```

Start React application:

```
npm start
```

Frontend will run at:

```
http://localhost:3000
```

---

# Using the Application

Open browser:

```
http://localhost:3000
```

Fill the form:

Environment
Application Name
Cluster Name
Namespace

Click:

**Analyze Kubernetes Events**

The system will:

1. Collect Kubernetes namespace events
2. Send them to the Python backend
3. Call Ollama AI model
4. Display root cause analysis

---

# Incident Watch Feature

You can also monitor namespace incidents.

Click:

**Watch Namespace for Incidents**

The backend watches Kubernetes pods and triggers AI analysis when failures occur such as:

* CrashLoopBackOff
* ImagePullBackOff
* Pod failures

---

# Example Failure for Demo

Create a failing pod:

```
kubectl run test-fail --image=nginx:wrongtag
```

This generates an **ImagePullBackOff** event.

Your tool will detect the incident and provide AI analysis.

---

# Troubleshooting

Backend not starting:

```
pip install uvicorn fastapi kubernetes requests
```

Kubernetes not responding:

```
kubectl get pods -A
```

Ollama not running:

```
ollama serve
```

React cannot connect to backend:

Check backend is running on port **8000**.

---

# Project Structure

```
project-root
│
├── frontend
│   ├── src
│   ├── package.json
│
├── backend
│   ├── main.py
│   ├── k8s_events.py
│   ├── ollama_client.py
│   └── requirements.txt
│
└── README.md
```

---

# Future Improvements

* Pod log analysis
* AI incident correlation
* Kubernetes event timeline
* Real-time cluster monitoring
* Grafana-style dashboard
* Need to integrate k8s network health check 

---

# Author

Rupesh Nayak
