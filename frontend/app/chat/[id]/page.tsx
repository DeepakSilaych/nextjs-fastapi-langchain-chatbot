'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import ChatWindow from '@/components/ChatWindow';
import InputBox from '@/components/InputBox';
import { getChatHistory } from '@/utils/api';

interface ChatMessage {
  id: number;
  message: string;
  is_user: boolean;
  timestamp: string;
}

export default function ChatSessionPage() {
  const params = useParams();
  const sessionId = params.id as string;
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadMessages = async () => {
      try {
        const history = await getChatHistory();
        setMessages(history);
        setLoading(false);
      } catch (error) {
        console.error('Failed to load messages:', error);
        setError('Failed to load chat messages');
        setLoading(false);
      }
    };

    if (sessionId) {
      loadMessages();
    }
  }, [sessionId]);

  if (loading) {
    return (
      <main className="flex flex-col h-screen">
        <div className="flex-1 flex items-center justify-center">
          <p className="text-gray-600 dark:text-gray-300">Loading chat history...</p>
        </div>
      </main>
    );
  }

  if (error) {
    return (
      <main className="flex flex-col h-screen">
        <div className="flex-1 flex items-center justify-center">
          <p className="text-red-600 dark:text-red-400">{error}</p>
        </div>
      </main>
    );
  }

  return (
    <main className="flex flex-col h-screen">
      <ChatWindow />
      <InputBox />
    </main>
  );
}