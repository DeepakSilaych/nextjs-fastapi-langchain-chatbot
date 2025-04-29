'use client';

import { useState, useEffect } from 'react';
import { api, getChatHistory } from '../utils/api';

interface Message {
  id?: number;
  content: string;
  isUser: boolean;
  timestamp?: string;
}

export function useChat(sessionId?: string) {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Load chat history on mount
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await getChatHistory(sessionId);
        if (history && Array.isArray(history)) {
          setMessages(history.map(msg => ({
            id: msg.id,
            content: msg.message,
            isUser: msg.is_user,
            timestamp: msg.timestamp
          })));
        }
      } catch (error) {
        console.error('Failed to load chat history:', error);
        setError('Failed to load chat history');
      }
    };

    loadHistory();
  }, [sessionId]);

  const sendMessage = async (content: string, msgSessionId?: string) => {
    setIsLoading(true);
    setError(null);
    
    // Add user message immediately
    setMessages(prev => [...prev, { content, isUser: true }]);

    try {
      const useSessionId = msgSessionId || sessionId || 'default';
      const eventSource = new EventSource(
        `${api.defaults.baseURL}/chat/stream?message=${encodeURIComponent(content)}&session_id=${useSessionId}`
      );
      let currentResponse = '';

      eventSource.onmessage = (event) => {
        const data = JSON.parse(event.data);
        currentResponse += data.content;
        
        // Use a callback form of setMessages to ensure we're working with the latest state
        setMessages(prev => {
          const newMessages = [...prev];
          // Find the AI message if it exists
          const aiMessageIndex = newMessages.findIndex(m => !m.isUser && !m.id);
          
          if (aiMessageIndex === -1) {
            // If no AI message exists, add a new one
            return [...newMessages, { content: currentResponse, isUser: false }];
          } else {
            // Update existing AI message
            newMessages[aiMessageIndex] = { 
              ...newMessages[aiMessageIndex], 
              content: currentResponse 
            };
            return newMessages;
          }
        });
      };

      eventSource.onerror = (error) => {
        console.error('SSE Error:', error);
        eventSource.close();
        setError('Failed to get response from AI');
        setIsLoading(false);
      };

      eventSource.addEventListener('done', () => {
        eventSource.close();
        setIsLoading(false);
        
        // After stream is done, update the message with final content
        setMessages(prev => {
          const newMessages = [...prev];
          const aiMessageIndex = newMessages.findIndex(m => !m.isUser && !m.id);
          if (aiMessageIndex !== -1) {
            newMessages[aiMessageIndex] = {
              ...newMessages[aiMessageIndex],
              id: Date.now(), // Add an ID to mark it as final
              content: currentResponse
            };
          }
          return newMessages;
        });
      });
      
    } catch (error) {
      console.error('Failed to send message:', error);
      setError('Failed to send message');
      setIsLoading(false);
    }
  };

  return {
    messages,
    sendMessage,
    isLoading,
    error,
  };
}