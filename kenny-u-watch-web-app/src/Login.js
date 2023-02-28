import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import useSessionStorage from './useSessionStorage';

import {useNavigate} from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/token/', {
        username: email,
        password,
      });

      setAccess(response.data.access);
      setRefresh(response.data.refresh);

      navigate('/dashboard');
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <form className="Login" onSubmit={handleSubmit}>
      <h2>Kenny U-Watch</h2>
      <div>
        <label htmlFor="email">Email:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </div>
      <div>
        <label htmlFor="password">Password:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default Login;
