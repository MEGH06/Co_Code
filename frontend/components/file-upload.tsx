'use client';

import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X } from 'lucide-react';
import { Progress } from '@/components/ui/progress';
import { saveFile } from '@/lib/db';
import { toast } from 'react-toastify';

export function FileUpload({ onUploadComplete }: { onUploadComplete?: () => void }) {
  const [uploading, setUploading] = useState(false);
  const [progress, setProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    setUploading(true);
    setProgress(0);

    try {
      for (let i = 0; i < acceptedFiles.length; i++) {
        const file = acceptedFiles[i];
        await saveFile(file);
        setProgress(((i + 1) / acceptedFiles.length) * 100);
      }
      toast.success(`${acceptedFiles.length} file(s) uploaded successfully`)
      // toast({
      //   title: 'Success',
      //   description: `${acceptedFiles.length} file(s) uploaded successfully`,
      // });

      onUploadComplete?.();
    } catch (error) {
      // toast({
      //   title: 'Error',
      //   description: 'Failed to upload files',
      //   variant: 'destructive',
      // });
    } finally {
      setUploading(false);
      setProgress(0);
    }
  }, [onUploadComplete, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.presentationml.presentation': ['.pptx'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
    },
  });

  return (
    <div
      {...getRootProps()}
      className={`border-2 border-dashed rounded-lg p-8 text-center transition-colors ${
        isDragActive ? 'border-primary bg-primary/5' : 'border-border'
      }`}
    >
      <input {...getInputProps()} />
      <div className="flex flex-col items-center gap-4">
        <div className="p-4 rounded-full bg-primary/10">
          <Upload className="w-8 h-8 text-primary" />
        </div>
        <div>
          <p className="text-lg font-medium">
            {isDragActive ? 'Drop files here' : 'Drag & drop files here'}
          </p>
          <p className="text-sm text-muted-foreground mt-1">
            or click to select files
          </p>
        </div>
        <p className="text-xs text-muted-foreground">
          Supports PDF, PPTX, and DOCX files
        </p>
      </div>
      {uploading && (
        <div className="mt-4 space-y-2">
          <Progress value={progress} />
          <p className="text-sm text-muted-foreground">
            Uploading... {Math.round(progress)}%
          </p>
        </div>
      )}
    </div>
  );
}