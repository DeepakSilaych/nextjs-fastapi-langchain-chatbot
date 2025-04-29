'use client';

import { useEffect, useRef } from 'react';
import MessageBubble from './MessageBubble';
import { useChat } from '../hooks/useChat';

export default function ChatWindow() {
  const { messages } = useChat();
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.length === 0 ? (
        <div className="flex items-center justify-center h-full">
          <p className="text-gray-500">No messages yet. Start a conversation!</p>
        </div>
      ) : (
        messages.map((message, index) => (
          <MessageBubble 
            key={message.id || index}
            message={message.content}
            isUser={message.isUser}
          />
        ))
      )}
      <div ref={messagesEndRef} />
    </div>
  );
}