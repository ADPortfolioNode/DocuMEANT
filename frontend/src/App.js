import React, { useEffect, useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import './App.css';
import ThreadList from './components/ThreadList/ThreadList';
import ThreadDetail from './components/ThreadDetail/ThreadDetail';

function App() {
  const [threads, setThreads] = useState([]);
  const [selectedThread, setSelectedThread] = useState(null);

  useEffect(() => {
    fetch('http://localhost:5000/api/threads')
      .then(res => res.json())
      .then(data => setThreads(data))
      .catch(err => console.error('Error fetching threads:', err));
  }, []);

  const selectThread = (thread) => {
    setSelectedThread(thread);
  };

  return (
    <div className="container-fluid">
      <nav className="navbar navbar-expand-lg navbar-light bg-light fixed-top">
        <a className="navbar-brand" href="#">Thread Manager</a>
      </nav>
      <div className="row mt-5 pt-4">
        <div className="col-md-3">
          <ThreadList threads={threads} selectThread={selectThread} />
        </div>
        <div className="col-md-9">
          {selectedThread && (
            <ThreadDetail thread={selectedThread} />
          )}
        </div>
      </div>
    </div>
  );
}

export default App;