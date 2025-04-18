import React, { useEffect, useRef, useState } from 'react';
import axios from '../api/axiosConfig';

const ChatBox = ({ selectedUser }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const chatEndRef = useRef(null);

  const currentUserId = parseInt(localStorage.getItem('id'));

  const fetchMessages = async () => {
    const userData = JSON.parse(localStorage.getItem('user'));

    // Extract the access token
    const token = userData?.access;

    console.log(token);  
    
    const res = await axios.get('http://localhost:8000/chat/api/get-messages/', {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });    ;
    const filtered = res.data.filter(msg =>
      (msg.sender === currentUserId && msg.receiver === selectedUser.id) ||
      (msg.receiver === currentUserId && msg.sender === selectedUser.id)
    );
    setMessages(filtered);
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const res = await axios.post('http://localhost:8000/chat/api/send/', {
      sender: currentUserId,
      receiver: selectedUser.id,
      message: message,
    });
    setMessage('');
    fetchMessages(); // refresh
  };

  useEffect(() => {
    if (selectedUser) fetchMessages();
  }, [selectedUser]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!selectedUser) return <div className="chat-box">Select a user to chat</div>;

  return (
    <div className="chat-box">
      <h3>Chat with {selectedUser.username}</h3>
      <div className="chat-messages" style={{ maxHeight: '300px', overflowY: 'scroll' }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              textAlign: msg.sender === currentUserId ? 'right' : 'left',
              margin: '5px'
            }}
          >
            <span>{msg.message}</span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <input
        type="text"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
        placeholder="Type a message..."
      />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
};

export default ChatBox;
