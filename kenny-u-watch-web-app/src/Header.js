import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import './Header.css';

const Header = () => {
    const location = useLocation();

    let accessToken = sessionStorage.getItem("access");
    const [isLoggedIn, setIsLoggedIn] = useState(!!accessToken);
    const { t, i18n } = useTranslation();
    const [currentLanguage, setCurrentLanguage] = useState(i18n.language);
    const navigate = useNavigate();

    const loginHref = '/login';

    useEffect(() => {
        // Check if ever the access token is set whenever the location of the app changes.
        accessToken = sessionStorage.getItem("access");
        setIsLoggedIn(!!accessToken);
      }, [location]);

    const changeLanguage = (language) => {
        i18n.changeLanguage(language);
        setCurrentLanguage(language);
    };

    const logout = () => {
        sessionStorage.removeItem("access");
        setIsLoggedIn(false);

        // Redirect to the login page.
        navigate(loginHref);
    };

    return (
      <header className="header">
        <h1 className="header-title">{t('header.title')}</h1>
        <nav>
          <ul className="header-menu">
            {isLoggedIn ? (
              <>
                <li className={`header-menu-item ${location.pathname === '/dashboard' ? 'active' : ''}`}>
                  <Link to="/dashboard">{t('dashboard.title')}</Link>
                </li>
                <li className={`header-menu-item ${location.pathname === '/create-alert' ? 'active' : ''}`}>
                  <Link to="/create-alert">{t('createAlert.title')}</Link>
                </li>
                <li className={`header-menu-item`}>
                  <button className="header-menu-item-button" onClick={() => logout()}>{t('logout.title')}</button>
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
            <li className="header-menu-item language-selector">
                {currentLanguage === 'en' ? (
                    <button className="header-menu-item-button" onClick={() => changeLanguage('fr')}>Français</button>
                ) : (
                    <button className="header-menu-item-button" onClick={() => changeLanguage('en')}>English</button>
                )}
            </li>
          </ul>
        </nav>
      </header>
    );
  };


export default Header;
