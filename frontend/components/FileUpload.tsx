'use client';

import { useState } from 'react';
import { useUpload } from '../hooks/useUpload';

export default function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const { uploadFile } = useUpload();

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === 'dragenter' || e.type === 'dragover') {
      setIsDragging(true);
    } else if (e.type === 'dragleave') {
      setIsDragging(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    for (const file of files) {
      await uploadFile(file);
    }
  };

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    for (const file of files) {
      await uploadFile(file);
    }
  };

  return (
    <div
      className={`p-6 border-2 border-dashed rounded-lg text-center ${
        isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'
      }`}
      onDragEnter={handleDrag}
      onDragLeave={handleDrag}
      onDragOver={handleDrag}
      onDrop={handleDrop}
    >
      <input
        type="file"
        onChange={handleFileInput}
        className="hidden"
        id="fileInput"
        multiple
      />
      <label
        htmlFor="fileInput"
        className="cursor-pointer text-gray-600 dark:text-gray-300"
      >
        <p>Drag and drop files here or click to select files</p>
      </label>
    </div>
  );
}