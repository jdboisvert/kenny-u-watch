import React, { useState } from 'react';
import axios from 'axios';
import './Signup.css';
import {useNavigate} from 'react-router-dom';
import {useTranslation} from 'react-i18next';

const Signup = (props) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const navigate = useNavigate();

  const {t} = useTranslation();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      await axios.post('http://127.0.0.1:8000/signup/v1/new', {
        email,
        username: email,
        password,
      });

      navigate('/login');
    } catch (error) {
      console.error(error);

      // TODO display error message to user
    }
  };

  return (
    <form className="Signup" onSubmit={handleSubmit}>
      <h2>Sign Up</h2>
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
      <button type="submit">{t('signUp.title')}</button>
    </form>
  );
};

export default Signup;
