'use client';

import { useState } from 'react';
import { useUpload } from '../hooks/useUpload';

export default function FileUpload() {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedFiles, setUploadedFiles] = useState<string[]>([]);
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

  const handleUpload = async (file: File) => {
    setError(null);
    setIsUploading(true);
    try {
      const result = await uploadFile(file);
      if (result) {
        setUploadedFiles(prev => [...prev, file.name]);
      } else {
        setError(`Failed to upload ${file.name}`);
      }
    } catch (err) {
      setError(`Error uploading ${file.name}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = Array.from(e.dataTransfer.files);
    for (const file of files) {
      await handleUpload(file);
    }
  };

  const handleFileInput = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    for (const file of files) {
      await handleUpload(file);
    }
  };

  return (
    <div className="space-y-4">
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
          <div className="space-y-2">
            <p>Drag and drop files here or click to select files</p>
            {isUploading && <p className="text-blue-500">Uploading...</p>}
          </div>
        </label>
      </div>

      {error && (
        <div className="p-4 bg-red-50 text-red-500 rounded-lg">
          {error}
        </div>
      )}

      {uploadedFiles.length > 0 && (
        <div className="p-4 bg-green-50 text-green-700 rounded-lg">
          <h3 className="font-semibold mb-2">Uploaded Files:</h3>
          <ul className="list-disc list-inside">
            {uploadedFiles.map((fileName, index) => (
              <li key={index}>{fileName}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}