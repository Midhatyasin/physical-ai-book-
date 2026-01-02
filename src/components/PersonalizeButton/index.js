import React, {useState, useEffect} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

const HARDWARE_PROFILES = {
  desktop: {
    label: 'Desktop Workstation',
    description: 'Full development environment with GPU',
    icon: '🖥️',
    recommended: ['ros2', 'gazebo', 'isaac'],
  },
  laptop: {
    label: 'Laptop',
    description: 'Portable development, may have integrated GPU',
    icon: '💻',
    recommended: ['ros2', 'gazebo'],
  },
  wsl: {
    label: 'WSL2 / Virtual Machine',
    description: 'Windows Subsystem for Linux',
    icon: '🐧',
    recommended: ['ros2', 'gazebo'],
  },
  cloud: {
    label: 'Cloud Instance',
    description: 'Remote development server',
    icon: '☁️',
    recommended: ['ros2', 'gazebo'],
  },
  none: {
    label: 'No Hardware Access',
    description: 'Learning only, no simulation capability',
    icon: '📚',
    recommended: [],
  },
};

export default function PersonalizeButton({onProfileChange, initialProfile = null}) {
  const [isOpen, setIsOpen] = useState(false);
  const [selectedProfile, setSelectedProfile] = useState(initialProfile || 'none');

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const saved = localStorage.getItem('physical-ai-profile');
      if (saved && HARDWARE_PROFILES[saved]) {
        setSelectedProfile(saved);
        onProfileChange?.(saved);
      }
    }
  }, [onProfileChange]);

  const handleSelect = (profileKey) => {
    setSelectedProfile(profileKey);
    if (typeof window !== 'undefined') {
      localStorage.setItem('physical-ai-profile', profileKey);
    }
    onProfileChange?.(profileKey);
    setIsOpen(false);
  };

  return (
    <div className={styles.container}>
      <button
        className={styles.trigger}
        onClick={() => setIsOpen(!isOpen)}
        aria-expanded={isOpen}
        aria-haspopup="listbox"
      >
        <span className={styles.icon}>⚙️</span>
        <span>Personalize Content</span>
        <span className={styles.arrow}>{isOpen ? '▲' : '▼'}</span>
      </button>

      {isOpen && (
        <div className={styles.dropdown} role="listbox">
          <div className={styles.dropdownHeader}>
            Select your development environment:
          </div>
          {Object.entries(HARDWARE_PROFILES).map(([key, profile]) => (
            <button
              key={key}
              className={clsx(styles.option, {
                [styles.selected]: selectedProfile === key,
              })}
              onClick={() => handleSelect(key)}
              role="option"
              aria-selected={selectedProfile === key}
            >
              <span className={styles.profileIcon}>{profile.icon}</span>
              <div className={styles.profileInfo}>
                <div className={styles.profileLabel}>{profile.label}</div>
                <div className={styles.profileDesc}>{profile.description}</div>
              </div>
              {selectedProfile === key && <span className={styles.check}>✓</span>}
            </button>
          ))}
        </div>
      )}

      {selectedProfile !== 'none' && (
        <div className={styles.recommendations}>
          <strong>Recommended tools:</strong>{' '}
          {HARDWARE_PROFILES[selectedProfile].recommended.join(', ')}
        </div>
      )}
    </div>
  );
}
