import React, {useState} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function CollapsibleCode({
  children,
  title,
  language = 'python',
  defaultExpanded = false,
  showLineNumbers = true,
}) {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);

  const toggleExpand = () => {
    setIsExpanded(!isExpanded);
  };

  const lines = React.Children.toArray(children).filter(
    child => typeof child === 'string' && child.trim()
  );

  return (
    <div className={styles.container}>
      <button
        className={styles.header}
        onClick={toggleExpand}
        aria-expanded={isExpanded}
      >
        <div className={styles.headerLeft}>
          <span className={styles.icon}>
            {isExpanded ? '📂' : '📄'}
          </span>
          <span className={styles.title}>{title || `Code (${language})`}</span>
          <span className={styles.langBadge}>{language}</span>
        </div>
        <span className={styles.toggleIcon}>
          {isExpanded ? '▲' : '▼'}
        </span>
      </button>

      {isExpanded && (
        <div className={styles.content}>
          <div className={styles.codeContainer}>
            <pre className={styles.code}>
              {showLineNumbers && (
                <div className={styles.lineNumbers}>
                  {lines.map((_, i) => (
                    <span key={i} className={styles.lineNumber}>{i + 1}</span>
                  ))}
                </div>
              )}
              <code className={`language-${language}`}>
                {children}
              </code>
            </pre>
            <button
              className={styles.copyButton}
              onClick={() => navigator.clipboard.writeText(children)}
              title="Copy to clipboard"
            >
              📋
            </button>
          </div>
        </div>
      )}

      {!isExpanded && (
        <div className={styles.collapsedPreview}>
          <code>{lines[0]?.trim().substring(0, 80)}...</code>
          <span className={styles.expandHint}>Click to expand</span>
        </div>
      )}
    </div>
  );
}
