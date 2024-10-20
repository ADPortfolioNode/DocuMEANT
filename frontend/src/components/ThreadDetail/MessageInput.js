import React from 'react';
import { Form, Button } from 'react-bootstrap';

function MessageInput({ newMessage, setNewMessage, sendMessage }) {
  return (
    <Form.Group className="mt-3">
      <Form.Control
        as="textarea"
        rows={3}
        value={newMessage}
        onChange={(e) => setNewMessage(e.target.value)}
        placeholder="Type your message..."
      />
      <Button variant="primary" onClick={sendMessage} className="mt-2">Send</Button>
    </Form.Group>
  );
}

export default MessageInput;