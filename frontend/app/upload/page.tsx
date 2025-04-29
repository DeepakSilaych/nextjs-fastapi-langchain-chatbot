'use client';

import FileUpload from '../../components/FileUpload';

export default function UploadPage() {
  return (
    <main className="flex min-h-screen flex-col items-center p-4 bg-gray-50 dark:bg-gray-900">
      <div className="w-full max-w-4xl space-y-4">
        <h1 className="text-2xl font-bold text-gray-800 dark:text-white">Upload Files</h1>
        <FileUpload />
      </div>
    </main>
  );
}