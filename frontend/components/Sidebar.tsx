'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useEffect, useState } from 'react';
import { MessageSquare, Upload, Settings, History } from 'lucide-react';
import SettingsDialog from './SettingsDialog';
import { getChatSessions, type ChatSession } from '../utils/api';

export default function Sidebar() {
  const pathname = usePathname();
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [chats, setChats] = useState<ChatSession[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const loadSessions = async () => {
      try {
        const sessions = await getChatSessions();
        setChats(sessions);
      } catch (error) {
        console.error('Failed to load chat sessions:', error);
        setError('Failed to load chat sessions');
      } finally {
        setLoading(false);
      }
    };

    loadSessions();
  }, []);

  return (
    <div className="w-64 h-screen bg-white dark:bg-gray-800 border-r dark:border-gray-700 flex flex-col">
      {/* Logo */}
      <div className="p-4 border-b dark:border-gray-700">
        <Link href="/" className="flex items-center space-x-2"> 
          <span className="text-xl font-bold">AI Chat</span>
        </Link>
      </div>

      {/* Main Actions */}
      <div className="p-2 space-y-2">
        <Link
          href="/"
          className={`flex items-center space-x-2 p-2 rounded-lg transition-colors ${
            pathname === '/' 
              ? 'bg-blue-100 text-blue-600 dark:bg-gray-700 dark:text-blue-400' 
              : 'hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <MessageSquare size={20} />
          <span>New Chat</span>
        </Link>

        <Link
          href="/upload"
          className={`flex items-center space-x-2 p-2 rounded-lg transition-colors ${
            pathname === '/upload'
              ? 'bg-blue-100 text-blue-600 dark:bg-gray-700 dark:text-blue-400'
              : 'hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <Upload size={20} />
          <span>Upload Files</span>
        </Link>

        <Link
          href="/history"
          className={`flex items-center space-x-2 p-2 rounded-lg transition-colors ${
            pathname === '/history'
              ? 'bg-blue-100 text-blue-600 dark:bg-gray-700 dark:text-blue-400'
              : 'hover:bg-gray-100 dark:hover:bg-gray-700'
          }`}
        >
          <History size={20} />
          <span>All History</span>
        </Link>
      </div>

      {/* Chat History */}
      <div className="flex-1 overflow-y-auto p-2">
        <div className="text-sm font-medium text-gray-500 dark:text-gray-400 mb-2">Recent Chats</div>
        {loading ? (
          <div className="text-sm text-gray-500 dark:text-gray-400 p-2">Loading chats...</div>
        ) : error ? (
          <div className="text-sm text-red-500 dark:text-red-400 p-2">{error}</div>
        ) : chats.length === 0 ? (
          <div className="text-sm text-gray-500 dark:text-gray-400 p-2">No chat history</div>
        ) : (
          <div className="space-y-1">
            {chats.map((chat) => (
              <Link
                key={chat.id}
                href={`/chat/${chat.id}`}
                className="block p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-sm"
              >
                <div className="truncate">{chat.title}</div>
                <div className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                  {new Date(chat.timestamp).toLocaleString()}
                  <span className="ml-2">{chat.message_count} messages</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>

      {/* Settings */}
      <div className="p-2 border-t dark:border-gray-700">
        <button
          onClick={() => setIsSettingsOpen(true)}
          className="flex items-center space-x-2 w-full p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
        >
          <Settings size={20} />
          <span>Settings</span>
        </button>
      </div>

      <SettingsDialog
        isOpen={isSettingsOpen}
        onClose={() => setIsSettingsOpen(false)}
      />
    </div>
  );
}