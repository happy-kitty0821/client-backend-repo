import axios from 'axios';

const axiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true, // send cookies if needed
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosInstance;
