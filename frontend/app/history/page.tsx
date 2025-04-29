'use client';

export default function HistoryPage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-4xl">
        <h1 className="text-2xl font-bold mb-4 text-gray-800 dark:text-white">Chat History</h1>
        <div className="space-y-4">
          {/* Chat history items will be added here */}
          <p className="text-gray-600 dark:text-gray-300">No chat history available.</p>
        </div>
      </div>
    </main>
  );
}