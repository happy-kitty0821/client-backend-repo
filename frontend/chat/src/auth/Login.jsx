import React, { useState } from 'react';
import axios from '../api/axiosConfig';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [form, setForm] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleChange = (e) => {
    setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(''); // Clear previous errors

    console.log("Sending payload:", form); // Debugging payload

    try {
      const response = await axios.post('/auth-app/api/login/', form, {
        headers: {
          'Content-Type': 'application/json',
        }
      });

      localStorage.setItem('user', JSON.stringify(response.data));
      navigate('/home');
    } catch (err) {
      console.error("Login failed:", err.response?.data || err.message);
      setError(err.response?.data?.non_field_errors?.[0] || "Login failed. Check your credentials.");
    }
  };

  return (
    <div>
      <h2>Login</h2>

      {error && <div style={{ color: 'red', marginBottom: '10px' }}>{error}</div>}

      <form onSubmit={handleSubmit}>
        <input
          type="text"
          name="username"
          value={form.username}
          onChange={handleChange}
          placeholder="Username"
          required
        />
        <br />
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          placeholder="Password"
          required
        />
        <br />
        <button type="submit">Login</button>
      </form>

      {/* Debugging: Show payload */}
      <div style={{ marginTop: '20px' }}>
        <h4>Payload being sent:</h4>
        <pre>{JSON.stringify(form, null, 2)}</pre>
      </div>
    </div>
  );
};

export default Login;
