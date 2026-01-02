import React, {useState, useEffect} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function TranslateButton({contentSelector = '.markdown', label = 'Translate to Urdu'}) {
  const [isTranslating, setIsTranslating] = useState(false);
  const [currentLang, setCurrentLang] = useState('en');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('physical-ai-lang') || 'en';
      setCurrentLang(saved);
    }
  }, []);

  const handleTranslate = async () => {
    if (currentLang === 'ur') {
      // Switch back to English
      setCurrentLang('en');
      localStorage.setItem('physical-ai-lang', 'en');
      document.documentElement.lang = 'en';
      document.documentElement.dir = 'ltr';
      return;
    }

    setIsTranslating(true);

    // Simulate translation delay (in real implementation, this would call a translation API)
    await new Promise(resolve => setTimeout(resolve, 1000));

    setCurrentLang('ur');
    localStorage.setItem('physical-ai-lang', 'ur');
    document.documentElement.lang = 'ur';
    document.documentElement.dir = 'rtl';

    setIsTranslating(false);
  };

  return (
    <button
      className={clsx(styles.button, {
        [styles.translated]: currentLang === 'ur',
      })}
      onClick={handleTranslate}
      disabled={isTranslating}
      aria-pressed={currentLang === 'ur'}
    >
      <span className={styles.icon}>{isTranslating ? '⏳' : '🌐'}</span>
      <span className={styles.text}>
        {isTranslating ? 'Translating...' : currentLang === 'ur' ? 'English میں دکھائیں' : label}
      </span>
    </button>
  );
}
