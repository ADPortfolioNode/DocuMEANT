import React from 'react';

function ThreadInfo({ thread }) {
  return (
    <div>
      <p>Status: {thread.status}</p>
      <p>Created At: {new Date(thread.created_at).toLocaleString()}</p>
      {thread.completed_at && <p>Completed At: {new Date(thread.completed_at).toLocaleString()}</p>}
    </div>
  );
}

export default ThreadInfo;