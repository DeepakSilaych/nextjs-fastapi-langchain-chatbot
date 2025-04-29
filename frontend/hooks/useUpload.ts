import { api } from '../utils/api';

export function useUpload() {
  const uploadFile = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append('file', file);
      
      const response = await api.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / (progressEvent.total || progressEvent.loaded)
          );
          console.log(`Upload Progress: ${percentCompleted}%`);
        }
      });
      
      return response.data;
    } catch (error) {
      console.error('Error uploading file:', error);
      return false;
    }
  };

  return {
    uploadFile,
  };
}