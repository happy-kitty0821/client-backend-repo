import React, { useState } from 'react';
import ChatList from './ChatList';
import ChatBox from './ChatBox';

const ChatPage = () => {
  const [selectedUser, setSelectedUser] = useState(null);

  return (
    <div style={{ display: 'flex', height: '100vh' }}>
      <div style={{ flex: '1', borderRight: '1px solid #ccc', padding: '10px' }}>
        <ChatList onUserSelect={setSelectedUser} />
      </div>
      <div style={{ flex: '3', padding: '10px' }}>
        <ChatBox selectedUser={selectedUser} />
      </div>
    </div>
  );
};

export default ChatPage;
