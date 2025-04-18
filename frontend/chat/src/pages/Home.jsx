import React from 'react';

const Home = () => {
  const user = JSON.parse(localStorage.getItem('user'));

  return (
    <div>
      <h1>Welcome, {user?.username}!</h1>
      <p>Your role is: {user?.role}</p>
    </div>
  );
};

export default Home;
