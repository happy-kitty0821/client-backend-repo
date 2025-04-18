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
    const currentUserId = parseInt(userData?.id);
    const token = userData?.access;

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
            msg.sender_profile.id === currentUserId ? 
            msg.receiver_profile : msg.sender_profile
          ) : null;

          // Exclude the logged-in user
          if (user && user.id !== currentUserId && !userMap[user.id]) {
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

  const styles = {
    chatList: {
      maxWidth: '400px',
      margin: '0 auto',
      padding: '10px',
      borderRadius: '5px',
      backgroundColor: '#f9f9f9',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    },
    input: {
      width: '100%',
      padding: '8px',
      marginBottom: '10px',
      border: '1px solid #ccc',
      borderRadius: '4px',
      fontSize: '14px',
    },
    ul: {
      listStyleType: 'none',
      padding: '0',
      margin: '0',
    },
    chatListItem: {
      display: 'flex',
      alignItems: 'center',
      padding: '10px',
      cursor: 'pointer',
      borderBottom: '1px solid #ddd',
    },
    chatListItemHover: {
      backgroundColor: '#f1f1f1',
    },
    userProfileImg: {
      width: '40px',
      height: '40px',
      borderRadius: '50%',
      marginRight: '10px',
    },
    userName: {
      fontWeight: 'bold',
      fontSize: '16px',
    },
    chatListItemActive: {
      backgroundColor: '#ddd',
    }
  };

  return (
    <div style={styles.chatList}>
      <input
        style={styles.input}
        type="text"
        placeholder="Search users..."
        value={searchText}
        onChange={(e) => setSearchText(e.target.value)}
        onKeyDown={(e) => e.key === 'Enter' && searchUser()}
      />
      {loading && <p>Loading...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <ul style={styles.ul}>
        {users.length > 0 ? (
          users.map(user => (
            <li
              key={user.id}
              onClick={() => onUserSelect(user)}
              style={styles.chatListItem}
              className="chat-list-item"
            >
              <img src={user.profile_image} alt={user.username} style={styles.userProfileImg} />
              <span style={styles.userName}>{user.username}</span>
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
