import React from 'react';
import './CreateAlert.css';
import axios from 'axios';
import useSessionStorage from './useSessionStorage';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

const CreateAlert = () => {
  const { register, handleSubmit, formState: { errors }, setError } = useForm();

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  const { t } = useTranslation();

  const navigate = useNavigate();

  const onSubmit = async (data) => {
    const body = {
      vehicle: {
        manufacturer_name: data.manufacturerName,
        model_name: data.modelName,
        model_year: data.modelYear,
      },
    };

    try {
      const options = {
        headers: {
          Authorization: `Bearer ${access}`,
          'Content-Type': 'application/json',
        },
      };
      await axios.post('http://127.0.0.1:8000/alerts/v1/create-alert', body, options);

      navigate('/dashboard');
    } catch (error) {
      if (error.response && error.response.status === 401) {
        const refreshResponse = await axios.post('http://127.0.0.1:8000/api/v1/token/refresh/', {
          "refresh": refresh,
        });

        const newAccess = refreshResponse.data.access;
        const newRefresh = refreshResponse.data.refresh;
        setAccess(newAccess);
        setRefresh(newRefresh);

        const retryOptions = {
          headers: {
            Authorization: `Bearer ${newAccess}`,
            'Content-Type': 'application/json',
          },
        };
        await axios.post('http://127.0.0.1:8000/alerts/v1/create-alert', body, retryOptions);
        navigate('/dashboard');
      } else {
        console.error(error);
        setError("apiError", {
          type: "manual",
          message: t('genericError.title'),
        });
      }
    }
  };

  return (
    <form className="CreateAlert" onSubmit={handleSubmit(onSubmit)}>
      <label>
        {t('manufacturer.title')}:
        <input
          type="text"
          {...register("manufacturerName", { required: true })}
        />
      </label>
      {errors.manufacturerName && <span>{t('requiredField.title')}</span>}
      <br />

      <label>
        {t('model.title')}:
        <input
          type="text"
          {...register("modelName", { required: true })}
        />
      </label>
      {errors.modelName && <span>{t('requiredField.title')}</span>}
      <br />

      <label>
        {t('year.title')}:
        <input
          type="text"
          {...register("modelYear", {
            required: t('requiredField.title'),
            pattern: {
              value: /^(19[0-9]{2}|20[0-9]{2}|2100)$/,
              message: t('validation.validYear')
            }
          })}
        />
      </label>
      {errors.modelYear && <span>{errors.modelYear.message}</span>}
      <br />

      {errors.apiError && <p className="error-message">{errors.apiError.message}</p>}

      <button type="submit">{t('createAlert.title')}</button>
    </form>
  );
};

export default CreateAlert;
