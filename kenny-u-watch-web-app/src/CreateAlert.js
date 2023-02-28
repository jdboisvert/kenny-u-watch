import React, { useState } from 'react';
import axios from 'axios';

import useSessionStorage from './useSessionStorage';

import {useNavigate} from 'react-router-dom';

import './CreateAlert.css';

const CreateAlert = () => {
  const [manufacturerName, setManufacturerName] = useState('');
  const [modelName, setModelName] = useState('');
  const [modelYear, setModelYear] = useState('');

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const options = {
        headers: {
          Authorization: `Bearer ${access}`,
          'Content-Type': 'application/json',
        },
      };
      const body = {
        vehicle: {
          manufacturer_name: manufacturerName,
          model_name: modelName,
          model_year: modelYear,
        },
      };
      await axios.post('http://127.0.0.1:8000/alerts/v1/create-alert', body, options);

      navigate('/dashboard');
    } catch (error) {
        if (error.response && error.response.status === 401) {
            // If the request fails with a 401, refresh the token
            const refreshResponse = await axios.post('http://127.0.0.1:8000/api/v1/token/refresh/', {
                "refresh": refresh,
            });
            const newAccess = refreshResponse.data.access;
            const newRefresh = refreshResponse.data.refresh;
            setAccess(newAccess);
            setRefresh(newRefresh);

            // Try the request again with the new access token
            const options = {
                headers: {
                  Authorization: `Bearer ${newAccess}`,
                  'Content-Type': 'application/json',
                },
              };
              const body = {
                vehicle: {
                  manufacturer_name: manufacturerName,
                  model_name: modelName,
                  model_year: modelYear,
                },
              };
              await axios.post('http://127.0.0.1:8000/alerts/v1/create-alert', body, options);

              navigate('/dashboard');
          } else {
            console.error(error);

            // TODO show error to the user
          }
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <label>
        Manufacturer Name:
        <input
          type="text"
          value={manufacturerName}
          onChange={(event) => setManufacturerName(event.target.value)}
        />
      </label>
      <br />
      <label>
        Model Name:
        <input
          type="text"
          value={modelName}
          onChange={(event) => setModelName(event.target.value)}
        />
      </label>
      <br />
      <label>
        Model Year:
        <input
          type="text"
          value={modelYear}
          onChange={(event) => setModelYear(event.target.value)}
        />
      </label>
      <br />
      <button type="submit">Create Alert</button>
    </form>
  );
};

export default CreateAlert;
