import React from 'react';

function ThreadItem({ thread, selectThread }) {
  return (
    <button
      onClick={() => selectThread(thread)}
      className="list-group-item list-group-item-action"
    >
      {thread.task_description} - {thread.status}
    </button>
  );
}

export default ThreadItem;