'use client';

import { useState } from 'react';
import { useParams } from 'next/navigation';
import { useChat } from '../hooks/useChat';

export default function InputBox() {
  const [input, setInput] = useState('');
  const params = useParams();
  const sessionId = params?.id as string;
  const { sendMessage, isLoading } = useChat();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      sendMessage(input, sessionId);
      setInput('');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="p-4 border-t dark:border-gray-700">
      <div className="flex space-x-4">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-lg border dark:border-gray-700 dark:bg-gray-800 dark:text-white"
          disabled={isLoading}
        />
        <button
          type="submit"
          className={`px-4 py-2 rounded-lg text-white ${
            isLoading 
              ? 'bg-blue-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
          }`}
          disabled={isLoading}
        >
          {isLoading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </form>
  );
}