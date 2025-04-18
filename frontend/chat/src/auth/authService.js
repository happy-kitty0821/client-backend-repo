import axios from '../api/axiosConfig';

export const loginUser = async (username, password) => {
  try {
    const response = await axios.post('/auth-app/api/login/', {
      username,
      password,
    });

    // Save tokens and user info to localStorage
    localStorage.setItem('access_token', response.data.access);
    localStorage.setItem('refresh_token', response.data.refresh);
    localStorage.setItem('user', JSON.stringify({
      id: response.data.id,
      username: response.data.user,
      role: response.data.role
    }));

    return response.data;
  } catch (error) {
    throw error.response?.data || { detail: 'Login failed' };
  }
};

export const logoutUser = () => {
  localStorage.clear();
};
