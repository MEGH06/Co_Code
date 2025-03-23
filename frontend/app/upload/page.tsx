'use client';

import { FileUpload } from '@/components/file-upload';
import { FileList } from '@/components/file-list';
import { useState } from 'react';

export default function UploadPage() {
  const [refreshKey, setRefreshKey] = useState(0);

  const handleChange = () => {
    setRefreshKey((prev) => prev + 1);
  };

  return (
    <div className="container mx-auto pt-4 space-y-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2">Upload Your Study Materials</h1>
        <p className="text-muted-foreground">
          Upload your PDFs, PPTs, and DOCs to get started
        </p>
      </div>

      <div className="max-w-2xl mx-auto">
        <FileUpload onUploadComplete={handleChange} />
      </div>

      <div className="mt-8">
        <h2 className="text-2xl font-semibold mb-4">Your Files</h2>
        <FileList key={refreshKey} onFileChange={handleChange} />
      </div>
    </div>
  );
}