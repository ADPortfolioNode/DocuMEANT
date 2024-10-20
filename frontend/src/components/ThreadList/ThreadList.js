import React from 'react';
import ThreadItem from './ThreadItem';

function ThreadList({ threads, selectThread }) {
  return (
    <div className="list-group">
      {threads.map(thread => (
        <ThreadItem key={thread.thread_id} thread={thread} selectThread={selectThread} />
      ))}
    </div>
  );
}

export default ThreadList;