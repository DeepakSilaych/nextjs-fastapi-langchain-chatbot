'use client';

import MessageBubble from './MessageBubble';
import { useChat } from '../hooks/useChat';

export default function ChatWindow() {
  const { messages } = useChat();

  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message, index) => (
        <MessageBubble 
          key={index}
          message={message.content}
          isUser={message.isUser}
        />
      ))}
    </div>
  );
}