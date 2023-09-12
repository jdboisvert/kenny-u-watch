import React from 'react';
import './authStyles.css';
import axios from 'axios';
import useSessionStorage from './useSessionStorage';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const { register, handleSubmit, formState: { errors }, setError } = useForm();

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  const { t } = useTranslation();

  const navigate = useNavigate();

  const onSubmit = async (data) => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/api/v1/token/', {
        username: data.email,
        password: data.password,
      });

      setAccess(response.data.access);
      setRefresh(response.data.refresh);

      navigate('/dashboard');
    } catch (error) {
      console.error(error);
      setError("apiError", {
        type: "manual",
        message: "Something went wrong with the API request.",
      });
    }
  };

  return (
    <form className="Login" onSubmit={handleSubmit(onSubmit)}>
      <h2>
        {t("login.title")}
      </h2>
      <div>
        <label htmlFor="email">{t('email.title')}:</label>
        <input
          type="email"
          id="email"
          {...register("email", { required: true })}
        />
        {errors.email && <span>{t('requiredField.title')}</span>}
      </div>
      <div>
        <label htmlFor="password">{t('password.title')}:</label>
        <input
          type="password"
          id="password"
          {...register("password", { required: true })}
        />
        {errors.password && <span>{t('requiredField.title')}</span>}
      </div>
      {errors.apiError && <p className="error-message">{t('genericError.title')}</p>}
      <button type="submit">{t('login.title')}</button>
    </form>
  );
};

export default Login;
