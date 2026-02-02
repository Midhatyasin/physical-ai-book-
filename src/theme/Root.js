import React from 'react';
import ChatBot from '../components/ChatBot';

// This component wraps the entire Docusaurus app
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatBot />
    </>
  );
}