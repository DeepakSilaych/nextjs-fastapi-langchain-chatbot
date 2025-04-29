'use client';

import { useEffect, useState } from 'react';
import { getChatHistory } from '../../utils/api';
import MessageBubble from '../../components/MessageBubble';

interface ChatMessage {
  id: number;
  message: string;
  is_user: boolean;
  timestamp: string;
}

export default function HistoryPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadHistory = async () => {
      try {
        const history = await getChatHistory();
        setMessages(history);
        setLoading(false);
      } catch (error) {
        console.error('Failed to load history:', error);
        setError('Failed to load chat history');
        setLoading(false);
      }
    };

    loadHistory();
  }, []);

  if (loading) {
    return (
      <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-4xl">
          <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Loading chat history...</h1>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 dark:bg-gray-900">
        <div className="w-full max-w-4xl">
          <h1 className="text-2xl font-bold mb-4 text-red-600 dark:text-red-400">{error}</h1>
        </div>
      </main>
    );
  }

  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-4xl">
        <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Chat History</h1>
        <div className="space-y-4">
          {messages.length === 0 ? (
            <p className="text-gray-600 dark:text-gray-300">No chat history available.</p>
          ) : (
            messages.map((message) => (
              <div key={message.id} className="flex flex-col gap-1">
                <MessageBubble 
                  message={message.message} 
                  isUser={message.is_user} 
                />
                <span className="text-xs text-gray-500 dark:text-gray-400">
                  {new Date(message.timestamp).toLocaleString()}
                </span>
              </div>
            ))
          )}
        </div>
      </div>
    </main>
  );
}