import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './AlertsList.css';

import useSessionStorage from './useSessionStorage';

const AlertsList = () => {
  const [alerts, setAlerts] = useState([]);
  const [sortBy, setSortBy] = useState('alphabetical');
  const [searchTerm, setSearchTerm] = useState('');
  const [filteredAlerts, setFilteredAlerts] = useState([]);

  const [access, setAccess] = useSessionStorage('access', '');
  const [refresh, setRefresh] = useSessionStorage('refresh', '');

  useEffect(() => {
    getAlerts();
    filterAlerts();
  }, [searchTerm, alerts]);

  const filterAlerts = () => {
    let filtered = alerts;
    if (searchTerm) {
      filtered = alerts.filter(
        (alert) =>
          alert.vehicle.manufacturer_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          alert.vehicle.model_name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          alert.vehicle.model_year.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }

    if (sortBy === 'newest') {
      filtered.sort((a, b) => new Date(b.created) - new Date(a.created));
    } else if (sortBy === 'oldest') {
      filtered.sort((a, b) => new Date(a.created) - new Date(b.created));
    } else {
      filtered.sort((a, b) => {
        const manufacturerA = a.vehicle.manufacturer_name.toLowerCase();
        const manufacturerB = b.vehicle.manufacturer_name.toLowerCase();
        if (manufacturerA < manufacturerB) return -1;
        if (manufacturerA > manufacturerB) return 1;
        return 0;
      });
    }
    setFilteredAlerts(filtered);
  };

  const getAlerts = async () => {
    try {
      const options = {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      };
      const response = await axios.get('http://127.0.0.1:8000/alerts/v1/get-alerts', options);
      setAlerts(response.data);
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
        const newOptions = {
          headers: {
            Authorization: `Bearer ${newAccess}`,
          },
        };
        const newResponse = await axios.get('http://127.0.0.1:8000/alerts/v1/get-alerts', newOptions);
        setAlerts(newResponse.data);
      } else {
        console.error(error);
      }
    }
  };

  const deleteAlert = async (id) => {
    try {
      const options = {
        headers: {
          Authorization: `Bearer ${access}`,
        },
      };
      await axios.delete(`http://127.0.0.1:8000/alerts/v1/delete-alert/${id}`, options);
      const updatedAlerts = alerts.filter((alert) => alert.id !== id);
      setAlerts(updatedAlerts);
    } catch (error) {
      console.error(error);
      if (error.response.status === 401) {
        const refreshResponse = await axios.post('http://127.0.0.1:8000/api/v1/token/refresh/', {
          refresh,
        });
        setAccess(refreshResponse.data.access);
        setRefresh(refreshResponse.data.refresh);
        deleteAlert(id);
      }
    }
  };


  const formatDate = (date) => {
    const dateObject = new Date(date);
    const options = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: 'numeric',
      minute: 'numeric',
    };
    return dateObject.toLocaleDateString('en-US', options);
  };

  return (
    <div className="AlertsList">

      <div className="sort-container">
      <input
        className="search-input"
        type="text"
        placeholder="Search..."
        value={searchTerm}
        onChange={(event) => setSearchTerm(event.target.value)}
      />
        <span className="sort-label">Sort by: </span>
        <select className="sort-select" value={sortBy} onChange={(e) => setSortBy(e.target.value)}>
          <option  value="newest">Newest</option>
          <option  value="oldest">Oldest</option>
          <option value="alphabetical">Alphabetical</option>
        </select>
      </div>
      {filteredAlerts.map((alert) => (
      <div className="Alert" key={alert.id}>
        <h3 className="Alert-Title">{alert.vehicle.manufacturer_name} {alert.vehicle.model_name} ({alert.vehicle.model_year})</h3>
        <p className="Alert-Date">Created: {formatDate(alert.created)}</p>
        <button className="delete-button" onClick={() => deleteAlert(alert.id)}>Delete</button>
      </div>
    ))}
    </div>
  );
};

export default AlertsList;
