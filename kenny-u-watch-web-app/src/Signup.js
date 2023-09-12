import React from 'react';
import './authStyles.css';
import axios from 'axios';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

const Signup = (props) => {
  const { register, handleSubmit, formState: { errors }, setError } = useForm();

  const navigate = useNavigate();
  const { t } = useTranslation();

  const onSubmit = async (data) => {
    try {
      await axios.post('http://127.0.0.1:8000/signup/v1/new', {
        email: data.email,
        username: data.email,
        password: data.password,
      });

      navigate('/login');
    } catch (error) {
      console.error(error);
      setError("apiError", {
        type: "manual",
        message: "Something went wrong with the API request.",
      });
    }
  };

  return (
    <form className="Signup" onSubmit={handleSubmit(onSubmit)}>
      <h2>{t("signUp.title")}</h2>

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

      <button type="submit">{t('signUp.title')}</button>
    </form>
  );
};

export default Signup;
