import React, { useState } from "react";

function App() {

  const [environment, setEnvironment] = useState("");
  const [application, setApplication] = useState("");
  const [cluster, setCluster] = useState("");
  const [namespace, setNamespace] = useState("");
  const [output, setOutput] = useState("");

  const submitForm = async () => {

    const response = await fetch("http://localhost:8000/analyze", {
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

    const data = await response.json();

    setOutput(
      "Events:\n" +
      data.events +
      "\n\nAI Analysis:\n" +
      data.analysis
    );
  };

  return (

    <div style={{padding:"40px"}}>

      <h2>Kubernetes AI Troubleshooter</h2>

      <input placeholder="Environment"
      onChange={(e)=>setEnvironment(e.target.value)} /><br/><br/>

      <input placeholder="Application Name"
      onChange={(e)=>setApplication(e.target.value)} /><br/><br/>

      <input placeholder="Cluster"
      onChange={(e)=>setCluster(e.target.value)} /><br/><br/>

      <input placeholder="Namespace"
      onChange={(e)=>setNamespace(e.target.value)} /><br/><br/>

      <button onClick={submitForm}>Analyze</button>

      <pre style={{marginTop:"30px"}}>
        {output}
      </pre>

    </div>

  );
}

export default App;
