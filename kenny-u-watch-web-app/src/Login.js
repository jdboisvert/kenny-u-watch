import React, { useState } from 'react';
import './Login.css';
import axios from 'axios';
import useSessionStorage from './useSessionStorage';
import { useTranslation } from 'react-i18next';

import {useNavigate} from 'react-router-dom';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  const { t } = useTranslation();

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
      <h2>
        {t('header.title')}
      </h2>
      <div>
        <label htmlFor="email">{t('email.title')}:</label>
        <input
          type="email"
          id="email"
          value={email}
          onChange={(event) => setEmail(event.target.value)}
        />
      </div>
      <div>
        <label htmlFor="password">{t('password.title')}:</label>
        <input
          type="password"
          id="password"
          value={password}
          onChange={(event) => setPassword(event.target.value)}
        />
      </div>
      <button type="submit">{t('login.title')}:</button>
    </form>
  );
};

export default Login;
