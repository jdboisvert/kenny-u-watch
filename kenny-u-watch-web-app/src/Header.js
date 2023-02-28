import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import './Header.css';

const Header = () => {
    const location = useLocation();

    let accessToken = sessionStorage.getItem("access");
    const [isLoggedIn, setIsLoggedIn] = useState(!!accessToken);

    useEffect(() => {
        // Check if ever the access token is set whenever the location of the app changes.
        accessToken = sessionStorage.getItem("access");
        setIsLoggedIn(!!accessToken);
      }, [location]);

    return (
      <header className="header">
        <h1 className="header-title">Kenny U-Watch</h1>
        <nav>
          <ul className="header-menu">
            {isLoggedIn ? (
              <>
                <li className={`header-menu-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>
                  <Link to="/dashboard">Dashboard</Link>
                </li>
                <li className={`header-menu-item ${location.pathname === '/create-alert' ? 'active' : ''}`}>
                  <Link to="/create-alert">Create Alert</Link>
                </li>
              </>
            ) : (
              <>
                <li className={`header-menu-item ${location.pathname === '/login' ? 'active' : ''}`}>
                  <Link to="/login">Login</Link>
                </li>
                <li className={`header-menu-item ${location.pathname === '/signup' ? 'active' : ''}`}>
                  <Link to="/signup">Signup</Link>
                </li>
              </>
            )}
          </ul>
        </nav>
      </header>
    );
  };


export default Header;
