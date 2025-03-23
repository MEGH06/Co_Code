"use client"

import { useState, useEffect, useCallback } from 'react';
import { toast } from "react-toastify";
import { FileData, getAllFiles } from "@/lib/db";

export const useFileSelect = () => {
  const [selectedFiles, setSelectedFiles] = useState<string[]>([]);
  const [files, setFiles] = useState<FileData[]>([]);
  const [loading, setLoading] = useState<boolean>(false);
  
  // Memoized file loading function
  const loadFiles = useCallback(async () => {
    try {
      const fetchedFiles = await getAllFiles();
      setFiles(fetchedFiles);
    } catch (error) {
      console.error('Error loading files:', error);
      toast.error("Failed to load files");
    }
  }, []);

  // Load files only once when component mounts
  useEffect(() => {
    loadFiles();
  }, [loadFiles]);

  // Memoized file selection handlers
  const addFile = useCallback((fileId: string) => {
    setSelectedFiles(prev => {
      if (prev.includes(fileId)) return prev;
      return [...prev, fileId];
    });
  }, []);

  const removeFile = useCallback((fileId: string) => {
    setSelectedFiles(prev => prev.filter(id => id !== fileId));
  }, []);

  const clearSelection = useCallback(() => {
    setSelectedFiles([]);
  }, []);

  // Return a stable object reference
  return {
    selectedFiles,
    files,
    loading,
    setLoading,
    actions: {
      addFile,
      removeFile,
      clearSelection
    }
  };
};

export default useFileSelect;