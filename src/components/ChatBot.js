import React, { useState } from 'react';
import styles from './ChatBot.module.css';

const ChatBot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      type: 'bot',
      content: 'Hello! I\'m your Physical AI Book Assistant. Ask me anything about the book content, or select text and ask questions about it.',
      timestamp: new Date()
    }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = {
      type: 'user',
      content: inputValue,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Get selected text if any
      const selectedText = window.getSelection().toString();
      
      const response = await fetch('http://localhost:8000/api/v1/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          selected_text: selectedText || null,
          mode: selectedText ? 'selected-text' : 'full-book'
        }),
      });

      const data = await response.json();

      const botMessage = {
        type: 'bot',
        content: data.answer,
        sources: data.sources,
        mode: data.mode,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      const errorMessage = {
        type: 'bot',
        content: 'Sorry, I encountered an error processing your question. Please make sure the API server is running on port 8000.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
    setInputValue('');
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <>
      {/* Chat Toggle Button */}
      <div className={styles.chatToggle}>
        <button
          onClick={() => setIsOpen(!isOpen)}
          className={styles.toggleButton}
          title="Open AI Assistant"
        >
          🤖
        </button>
      </div>

      {/* Chat Window */}
      {isOpen && (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <h3>Physical AI Assistant</h3>
            <button
              onClick={() => setIsOpen(false)}
              className={styles.closeButton}
            >
              ×
            </button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map((message, index) => (
              <div
                key={index}
                className={`${styles.message} ${styles[message.type]}`}
              >
                <div className={styles.messageContent}>
                  {message.content}
                  {message.sources && message.sources.length > 0 && (
                    <div className={styles.sources}>
                      <small>
                        <strong>Mode:</strong> {message.mode} | 
                        <strong> Sources:</strong> {message.sources.map(s => s.source).join(', ')}
                      </small>
                    </div>
                  )}
                </div>
                <div className={styles.timestamp}>
                  {message.timestamp.toLocaleTimeString()}
                </div>
              </div>
            ))}
            {isLoading && (
              <div className={`${styles.message} ${styles.bot}`}>
                <div className={styles.messageContent}>
                  <div className={styles.typing}>Thinking...</div>
                </div>
              </div>
            )}
          </div>

          <div className={styles.chatInput}>
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book content, or select text first..."
              className={styles.inputField}
              rows="2"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>

          <div className={styles.chatFooter}>
            <small>
              💡 <strong>Tip:</strong> Select any text on the page and ask questions about it for focused answers!
            </small>
          </div>
        </div>
      )}
    </>
  );
};

export default ChatBot;