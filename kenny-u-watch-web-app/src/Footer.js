import React from 'react';
import './Footer.css';
import { useTranslation } from 'react-i18next';


const Footer = () => {
    const { t } = useTranslation();

  return (
    <footer className="Footer">
      <p>
        {t('footer.title')}
      </p>
    </footer>
  );
};

export default Footer;
