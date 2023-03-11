import React from 'react';
import { I18nextProvider } from 'react-i18next';
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import en from './locales/en/en.json';
import fr from './locales/fr/fr.json';

i18n
  .use(initReactI18next)
  .init({
    resources: {
      en: {
        translation: en,
      },
      fr: {
        translation: fr,
      },
    },
    lng: 'en',
    fallbackLng: 'en',
    debug: true, // TODO only in dev mode
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
