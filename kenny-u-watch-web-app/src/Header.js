import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
  const location = useLocation();

  return (
    <header className="header">
      <h1 className="header-title">Kenny U-Watch</h1>
      <nav>
        <ul className="header-menu">
        <li className={`header-menu-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>
            <Link to="/dashboard">Dashboard</Link>
          </li>
          <li className={`header-menu-item ${location.pathname === '/create-alert' ? 'active' : ''}`}>
            <Link to="/create-alert">Create Alert</Link>
          </li>
        </ul>
      </nav>
    </header>
  );
};

export default Header;
