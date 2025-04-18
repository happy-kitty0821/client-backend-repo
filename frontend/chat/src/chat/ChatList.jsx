import React, { useEffect, useState } from 'react';
import axios from '../api/axiosConfig'; // Assuming this is your custom axios config
import { useNavigate } from 'react-router-dom';

const ChatList = ({ onUserSelect }) => {
  const [users, setUsers] = useState([]);
  const [searchText, setSearchText] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const searchUser = async () => {
    if (!searchText) return;
    const userData = JSON.parse(localStorage.getItem('user'));

    // Extract the access token
    const token = userData?.access;

    console.log(token);  
    
    try {
      // Sending query as a query parameter
      const res = await axios.get(`/chat/api/search/?user=${searchText}`, {
        headers: {
          Authorization: `Bearer ${token}`,
        }
      });
      setUsers(res.data);
    } catch (error) {
      console.error('Error searching for user:', error);
    }
  };

  useEffect(() => {
    const userData = JSON.parse(localStorage.getItem('user'));

    // Extract the access token
    const token = userData?.access;

    console.log(token);  
  
    setLoading(true);
    setError(null); // Reset the error message before trying to fetch
    axios.get('http://localhost:8000/chat/api/get-messages/', {
      headers: {
        Authorization: `Bearer ${token}`,
      }
    })
    .then(res => {
      const uniqueUsers = [];
      const userMap = {};
  
      res.data.forEach(msg => {
        const user = msg.sender_profile.id !== msg.receiver_profile.id ? (
          msg.sender_profile.id === parseInt(localStorage.getItem('id')) ? 
          msg.receiver_profile : msg.sender_profile
        ) : null;
  
        if (user && !userMap[user.id]) {
          userMap[user.id] = true;
          uniqueUsers.push(user);
        }
      });
  
      setUsers(uniqueUsers);
    })
    .catch(error => {
      setError('Error fetching messages. Please try again later.');
      console.error('Error fetching messages:', error);
    })
    .finally(() => {
      setLoading(false);
    });
  }, []);

  return (
    <div className="chat-list">
      <input
        type="text"
        placeholder="Search users..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && searchUser()}
      />
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul>
        {users.length > 0 ? (
          users.map(user => (
            <li key={user.id} onClick={() => onUserSelect(user)}>
              {user.username}
            </li>
          ))
        ) : (
          <p>No users found</p>
        )}
      </ul>
    </div>
  );
};

export default ChatList;
