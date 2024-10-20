import React, { useState, useEffect } from 'react';
import { Modal, Button, Form } from 'react-bootstrap';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import ThreadInfo from './ThreadInfo';

function ThreadDetail({ thread }) {
  const [newMessage, setNewMessage] = useState('');
  const [children, setChildren] = useState([]);
  const [showModal, setShowModal] = useState(true);

  useEffect(() => {
    fetch(`http://localhost:5000/api/threads/${thread.thread_id}/children`)
      .then(res => res.json())
      .then(data => setChildren(data))
      .catch(err => console.error('Error fetching child threads:', err));
  }, [thread.thread_id]);

  const sendMessage = () => {
    if (newMessage) {
      fetch(`http://localhost:5000/api/threads/${thread.thread_id}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ content: newMessage, sender: 'User' }),
      })
        .then(res => res.json())
        .then(data => {
          thread.messages = data;
          setNewMessage('');
        })
        .catch(err => console.error('Error sending message:', err));
    }
  };

  const completeThread = () => {
    fetch(`http://localhost:5000/api/threads/${thread.thread_id}/complete`, {
      method: 'POST',
    })
      .then(res => res.json())
      .then(data => {
        thread.status = data.status;
        thread.completed_at = data.completed_at;
      })
      .catch(err => console.error('Error completing thread:', err));
  };

  return (
    <Modal show={showModal} onHide={() => setShowModal(false)} size="lg">
      <Modal.Header closeButton>
        <Modal.Title>{thread.task_description}</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        <ThreadInfo thread={thread} />
        <MessageList messages={thread.messages} />
        <MessageInput newMessage={newMessage} setNewMessage={setNewMessage} sendMessage={sendMessage} />
        <Button variant="success" onClick={completeThread} className="mt-2">Complete Thread</Button>
        {children.length > 0 && (
          <div className="mt-4">
            <h5>Child Threads</h5>
            <div className="list-group">
              {children.map((child) => (
                <div key={child.thread_id} className="list-group-item">
                  <p>Task: {child.task_description}</p>
                  <p>Status: {child.status}</p>
                  <p>Messages: {child.messages.length}</p>
                </div>
              ))}
            </div>
          </div>
        )}
      </Modal.Body>
    </Modal>
  );
}

export default ThreadDetail;