import React, { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState(null);
  const [chromaStatus, setChromaStatus] = useState(null);

  useEffect(() => {
    // Test backend connection
    fetch('http://localhost:5000/api/status')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => console.error('Backend Error:', err));

    // Test ChromaDB connection
    fetch('http://localhost:5000/api/chromadb/status')
      .then(res => res.json())
      .then(data => setChromaStatus(data))
      .catch(err => console.error('ChromaDB Error:', err));
  }, []);

  return (
    <div>
      <h1>Backend Status: {status && status.message ? status.message : 'Loading...'}</h1>
      <h1>ChromaDB Status: {chromaStatus && chromaStatus.message ? chromaStatus.message : 'Loading...'}</h1>
    </div>
  );
}

export default App;