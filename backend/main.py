from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from k8s_events import get_namespace_events
from watch_pods import watch_pods
from k8s_copilot import get_problem_pods
from ollama_client import ask_ollama
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class K8sRequest(BaseModel):
    environment: str
    application: str
    cluster: str
    namespace: str

@app.post("/analyze")
def analyze(req: K8sRequest):

    events = get_namespace_events(req.namespace)

    prompt = f"""
Environment: {req.environment}
Application: {req.application}
Cluster: {req.cluster}
Namespace: {req.namespace}

Kubernetes Events:
{events}

Explain root cause and give solution.
"""
    print("Calling Ollama...")

    solution = ask_ollama(prompt)

    print("Ollama response in", solution)


    return {
        "events": events,
        "analysis": solution
    }

@app.get("/watch/{namespace}")
def watch_namespace(namespace: str):
    print("1")
    incident = watch_pods(namespace)
    print("2")
    if incident:

        prompt = f"""
Pod {incident['pod']} has failure reason {incident['reason']}.

Explain root cause and give kubectl commands to fix.
"""
        print("Calling Ollama...")
        solution = ask_ollama(prompt)

        return {
            "incident": incident,
            "analysis": solution
        }

    return {"message": "No incident detected"}

@app.get("/copilot/{namespace}")
def k8s_copilot(namespace: str):

    issues = get_problem_pods(namespace)

    if not issues:
        return {"message": "No failing pods detected"}

    prompt = f"""
You are a Kubernetes SRE Copilot.

Analyze the issue and respond ONLY in this format:

Pod: <pod name>
Error: <short error>
RootCause: <one sentence>
Fix: <kubectl command>

Issues:
{issues}
"""
    print("Calling Ollama...")
    analysis = ask_ollama(prompt)

    return {
        "issues": issues,
        "analysis": analysis
    }    