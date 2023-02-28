import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import reportWebVitals from './reportWebVitals';

import Login from './Login';
import Signup from './Signup';
import AlertsList from './AlertsList';
import CreateAlert from './CreateAlert';
import Footer from './Footer';
import Header from './Header';

import './i18n';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <div className="app">
    <Router>
      <Header />
      <div className="content">
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<AlertsList />} />
          <Route path="/create-alert" element={<CreateAlert />} />
        </Routes>
      </div>
    </Router>
    <Footer />
  </div>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
