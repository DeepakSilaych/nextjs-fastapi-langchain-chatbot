'use client';

import { useState } from 'react';

interface Message {
  content: string;
  isUser: boolean;
}

export function useChat() {
  const [messages, setMessages] = useState<Message[]>([]);

  const sendMessage = async (content: string) => {
    // Add user message
    setMessages(prev => [...prev, { content, isUser: true }]);
    
    try {
      // TODO: Implement API call
      // Temporary mock response
      const response = "This is a mock response. API integration pending.";
      setMessages(prev => [...prev, { content: response, isUser: false }]);
    } catch (error) {
      console.error('Failed to send message:', error);
    }
  };

  return {
    messages,
    sendMessage,
  };
}