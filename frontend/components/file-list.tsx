'use client';

import { useEffect, useState } from 'react';
import { FileText, Trash2, Edit2 } from 'lucide-react';
import { Button } from '@/components/ui/button';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table';
import { Input } from '@/components/ui/input';
import { getAllFiles, deleteFile, renameFile, FileData } from '@/lib/db';
import { toast} from "react-toastify";

export function FileList({ onFileChange }: { onFileChange?: () => void }) {
  const [files, setFiles] = useState<FileData[]>([]);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [newName, setNewName] = useState('');

  const loadFiles = async () => {
    const files = await getAllFiles();
    setFiles(files);
  };

  useEffect(() => {
    loadFiles();
  }, []);

  const handleDelete = async (id: string) => {
    try {
      await deleteFile(id);
      await loadFiles();
      onFileChange?.();
      toast.success("File deleted successfully");
    } catch (error) {
      toast.error("Failed to delete file")
    }
  };

  const handleRename = async (id: string) => {
    if (!newName.trim()) return;
    try {
      await renameFile(id, newName);
      await loadFiles();
      setEditingId(null);
      setNewName('');
      onFileChange?.();
      toast.success("File renamed successfully")
    } catch (error) {
      toast.error("Failed to rename file")
    }
  };

  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>File Name</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Uploaded</TableHead>
            <TableHead className="text-right">Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {files.map((file) => (
            <TableRow key={file.id}>
              <TableCell className="font-medium">
                {editingId === file.id ? (
                  <div className="flex items-center gap-2">
                    <Input
                      value={newName}
                      onChange={(e) => setNewName(e.target.value)}
                      className="h-8"
                    />
                    <Button
                      size="sm"
                      onClick={() => handleRename(file.id)}
                      className="h-8"
                    >
                      Save
                    </Button>
                  </div>
                ) : (
                  <div className="flex items-center gap-2">
                    <FileText className="w-4 h-4" />
                    {file.name}
                  </div>
                )}
              </TableCell>
              <TableCell>{file.type}</TableCell>
              <TableCell>
                {new Date(file.uploadedAt).toLocaleDateString()}
              </TableCell>
              <TableCell className="text-right">
                <div className="flex justify-end gap-2">
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => {
                      setEditingId(file.id);
                      setNewName(file.name);
                    }}
                  >
                    <Edit2 className="w-4 h-4" />
                  </Button>
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => handleDelete(file.id)}
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}