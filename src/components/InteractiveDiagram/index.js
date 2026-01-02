import React, {useState, useEffect, useRef} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function InteractiveDiagram({
  children,
  title,
  description,
  diagramId,
}) {
  const [hoveredNode, setHoveredNode] = useState(null);
  const [clickedNode, setClickedNode] = useState(null);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const containerRef = useRef(null);

  useEffect(() => {
    // Initialize Mermaid if needed
    if (typeof window !== 'undefined' && !window.mermaidInitialized) {
      import('mermaid').then(mermaid => {
        mermaid.initialize({startOnLoad: false, theme: 'default'});
        window.mermaidInitialized = true;
      });
    }
  }, []);

  const handleNodeHover = (nodeId) => {
    setHoveredNode(nodeId);
  };

  const handleNodeClick = (nodeId) => {
    setClickedNode(nodeId === clickedNode ? null : nodeId);
  };

  const toggleFullscreen = () => {
    if (!document.fullscreenElement) {
      containerRef.current?.requestFullscreen();
      setIsFullscreen(true);
    } else {
      document.exitFullscreen();
      setIsFullscreen(false);
    }
  };

  return (
    <div className={styles.container} ref={containerRef}>
      <div className={styles.header}>
        <div className={styles.headerInfo}>
          <h4 className={styles.title}>{title}</h4>
          {description && <p className={styles.description}>{description}</p>}
        </div>
        <button
          className={styles.fullscreenBtn}
          onClick={toggleFullscreen}
          title={isFullscreen ? 'Exit fullscreen' : 'Fullscreen'}
        >
          {isFullscreen ? '⛶' : '⛶'}
        </button>
      </div>

      <div
        className={clsx(styles.diagramWrapper, {
          [styles.highlighted]: hoveredNode || clickedNode,
        })}
        onMouseLeave={() => {
          setHoveredNode(null);
        }}
      >
        {children}

        {(hoveredNode || clickedNode) && (
          <div className={styles.tooltip}>
            {clickedNode ? (
              <div className={styles.tooltipContent}>
                <strong>Clicked:</strong> {clickedNode}
              </div>
            ) : (
              <div className={styles.tooltipContent}>
                <strong>Hovered:</strong> {hoveredNode}
              </div>
            )}
          </div>
        )}
      </div>

      <div className={styles.legend}>
        <span className={styles.legendItem}>
          <span className={styles.legendDot} style={{background: hoveredNode || clickedNode ? '#667eea' : '#ccc'}} />
          Interactive
        </span>
        <span className={styles.legendItem}>
          <span className={styles.legendDot} style={{background: '#10b981'}} />
          Click for details
        </span>
      </div>
    </div>
  );
}
