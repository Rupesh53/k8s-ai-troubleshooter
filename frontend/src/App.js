import React, { useState } from "react";
import "./ubs-theme.css";

function App() {

  const [environment, setEnvironment] = useState("");
  const [application, setApplication] = useState("");
  const [cluster, setCluster] = useState("");
  const [namespace, setNamespace] = useState("");
  const [result, setResult] = useState("");
  
  const runCopilot = async () => {

  const res = await fetch(`http://localhost:8000/copilot/${namespace}`);

  const data = await res.json();

  setResult(data.analysis);
};
  const watchNamespace = async () => {

  const res = await fetch(`http://localhost:8000/watch/${namespace}`);

  const data = await res.json();

  setResult(data.analysis);
};
  const submitForm = async (e) => {
    e.preventDefault();

    const res = await fetch("http://localhost:8000/analyze", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
        environment,
        application,
        cluster,
        namespace
      })
    });

    const data = await res.json();
    setResult(data.analysis);
  };

  return (
    <div>

      <div className="ubs-header">
        UK8s-UBS AI Kubernetes Copilot
      </div>

      <div className="container">

        <div className="card">

          <h3>Cluster Diagnostic Request</h3>

          <form onSubmit={submitForm}>

            <label>Environment</label>
            <input
              value={environment}
              onChange={(e) => setEnvironment(e.target.value)}
            />

            <label>Application</label>
            <input
              value={application}
              onChange={(e) => setApplication(e.target.value)}
            />

            <label>Cluster</label>
            <input
              value={cluster}
              onChange={(e) => setCluster(e.target.value)}
            />

            <label>Namespace</label>
            <input
              value={namespace}
              onChange={(e) => setNamespace(e.target.value)}
            />

            {/* <button type="submit">
              Analyze Kubernetes Events
            </button> */}
            

            <button type="button" onClick={watchNamespace}>
            Watch Namespace for Incidents
            </button>
            <button type="button" onClick={runCopilot}>
            Run AI Copilot
            </button>
          </form>

          {result && (
            <div className="result">
              <h4>AI Root Cause Analysis</h4>
              <p>{result}</p>
            </div>
          )}

        </div>

      </div>

    </div>
  );
}

export default App;