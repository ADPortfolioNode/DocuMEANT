import React, { useEffect, useState } from 'react';

function App() {
  const [status, setStatus] = useState(null);
  const [chromaStatus, setChromaStatus] = useState(null);
  const [threads, setThreads] = useState([]);
  const [newTaskDescription, setNewTaskDescription] = useState('');

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

    // Fetch active threads
    fetchThreads();
  }, []);

  const fetchThreads = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/threads');
      const data = await response.json();
      setThreads(Object.values(data));
    } catch (err) {
      console.error('Error fetching threads:', err);
    }
  };

  const createThread = async () => {
    try {
      await fetch('http://localhost:5000/api/threads', {  // Removed unused data variable
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          task_description: newTaskDescription,
        }),
      });
      fetchThreads();
      setNewTaskDescription('');
    } catch (err) {
      console.error('Error creating thread:', err);
    }
  };

  return (
    <div className="p-4">
      <h1>System Status</h1>
      <div className="mb-4">
        <p>Backend Status: {status && status.message ? status.message : 'Loading...'}</p>
        <p>ChromaDB Status: {chromaStatus && chromaStatus.message ? chromaStatus.message : 'Loading...'}</p>
      </div>

      <div className="mb-4">
        <h2>Create New Thread</h2>
        <input
          type="text"
          value={newTaskDescription}
          onChange={(e) => setNewTaskDescription(e.target.value)}
          placeholder="Enter task description"
          className="mr-2 p-2 border"
        />
        <button onClick={createThread} className="p-2 bg-blue-500 text-white">
          Create Thread
        </button>
      </div>

      <div>
        <h2>Active Threads</h2>
        <div className="grid gap-4">
          {threads.map((thread) => (
            <div key={thread.thread_id} className="p-4 border rounded">
              <p>Thread ID: {thread.thread_id}</p>
              <p>Task: {thread.task}</p>
              <p>Status: {thread.status}</p>
              <p>Messages: {thread.message_count}</p>
              <p>Children: {thread.children_count}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}

export default App;