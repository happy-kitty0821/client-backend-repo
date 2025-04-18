import React, { useEffect, useRef, useState } from 'react';
import axios from '../api/axiosConfig';

const ChatBox = ({ selectedUser }) => {
  const [messages, setMessages] = useState([]);
  const [message, setMessage] = useState('');
  const chatEndRef = useRef(null);

  const userData = JSON.parse(localStorage.getItem('user'));
  const currentUserId = parseInt(userData?.id);

  const fetchMessages = async () => {
    const token = userData?.access;

    try {
      const res = await axios.get('http://localhost:8000/chat/api/get-messages/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });

      const filtered = res.data.filter(
        (msg) =>
          (parseInt(msg.sender) === currentUserId && parseInt(msg.receiver) === parseInt(selectedUser.id)) ||
          (parseInt(msg.receiver) === currentUserId && parseInt(msg.sender) === parseInt(selectedUser.id))
      );

      setMessages(filtered);
    } catch (error) {
      console.error("Error fetching messages:", error);
    }
  };

  const sendMessage = async () => {
    if (!message.trim()) return;

    const token = userData?.access;

    try {
      await axios.post(
        'http://localhost:8000/chat/api/send/',
        {
          sender: currentUserId,
          receiver: selectedUser.id,
          message: message,
        },
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      setMessage('');
      fetchMessages(); // fetch the latest messages after sending a message
    } catch (error) {
      console.error("Error sending message:", error);
    }
  };

  useEffect(() => {
    if (selectedUser) {
      fetchMessages(); // Fetch messages initially for the selected user

      // Set up polling to fetch messages every 1 seconds
      const intervalId = setInterval(fetchMessages, 1000);

      // Clear the interval when the component unmounts
      return () => clearInterval(intervalId);
    }
  }, [selectedUser]);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  if (!selectedUser) return <div className="chat-box">Select a user to chat</div>;

  return (
    <div style={styles.chatContainer}>
      <h3 style={styles.header}>Chat with {selectedUser.username}</h3>
      <div style={styles.chatMessages}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              ...styles.messageBubble,
              alignSelf: msg.sender === currentUserId ? 'flex-end' : 'flex-start',
              backgroundColor: msg.sender === currentUserId ? '#DCF8C6' : '#F1F0F0',
            }}
          >
            <span>{msg.message}</span>
          </div>
        ))}
        <div ref={chatEndRef} />
      </div>
      <div style={styles.inputContainer}>
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Type a message..."
          style={styles.input}
        />
        <button onClick={sendMessage} style={styles.sendButton}>Send</button>
      </div>
    </div>
  );
};

const styles = {
  chatContainer: {
    border: '1px solid #ccc',
    borderRadius: '10px',
    width: '100%',
    maxWidth: '500px',
    margin: '0 auto',
    padding: '10px',
    backgroundColor: '#ffffff',
    boxShadow: '0 0 10px rgba(0,0,0,0.1)',
    display: 'flex',
    flexDirection: 'column',
    height: '500px',
  },
  header: {
    margin: '0 0 10px 0',
    textAlign: 'center',
    color: '#333',
  },
  chatMessages: {
    flex: 1,
    overflowY: 'auto',
    display: 'flex',
    flexDirection: 'column',
    gap: '10px',
    padding: '10px',
    backgroundColor: '#f9f9f9',
    borderRadius: '8px',
  },
  messageBubble: {
    maxWidth: '75%',
    padding: '10px',
    borderRadius: '15px',
    fontSize: '14px',
    wordWrap: 'break-word',
    boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
  },
  inputContainer: {
    display: 'flex',
    marginTop: '10px',
    borderTop: '1px solid #eee',
    paddingTop: '10px',
  },
  input: {
    flex: 1,
    padding: '10px',
    fontSize: '14px',
    borderRadius: '20px',
    border: '1px solid #ccc',
    outline: 'none',
    marginRight: '10px',
  },
  sendButton: {
    padding: '10px 20px',
    borderRadius: '20px',
    backgroundColor: '#007bff',
    color: '#fff',
    border: 'none',
    cursor: 'pointer',
  },
};

export default ChatBox;
