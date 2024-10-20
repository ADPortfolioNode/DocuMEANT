import React, { useState } from 'react';

function MessageList({ messages }) {
  const [messageList, setMessageList] = useState(messages);

  return (
    <ul className="list-group">
      {messageList.map(message => (
        <li key={message.id} className="list-group-item">
          <p>{message.content}</p>
          <p className="text-muted">- {message.sender} at {new Date(message.timestamp).toLocaleString()}</p>
        </li>
      ))}
    </ul>
  );
}

export default MessageList;