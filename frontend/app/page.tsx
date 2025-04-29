'use client';

import ChatWindow from '../components/ChatWindow';
import InputBox from '../components/InputBox';

export default function Home() {
  return (
    <div className="h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      <main className="flex-1 overflow-hidden">
        <div className="h-full flex flex-col max-w-4xl mx-auto">
          <ChatWindow />
          <InputBox />
        </div>
      </main>
    </div>
  );
}
