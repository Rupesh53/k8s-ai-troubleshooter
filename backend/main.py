from fastapi import FastAPI
from pydantic import BaseModel
from k8s_events import get_namespace_events
from ollama_client import ask_ollama

app = FastAPI()

class K8sRequest(BaseModel):
    environment: str
    application: str
    cluster: str
    namespace: str

@app.post("/analyze")
def analyze(req: K8sRequest):

    events = get_namespace_events(req.namespace)

    prompt = f"""
You are a Kubernetes SRE expert.

Environment: {req.environment}
Application: {req.application}
Cluster: {req.cluster}
Namespace: {req.namespace}

Recent Kubernetes Events:
{events}

Explain the root cause and provide troubleshooting steps.
"""

    solution = ask_ollama(prompt)

    return {
        "events": events,
        "analysis": solution
    }
