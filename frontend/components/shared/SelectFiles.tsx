"use client"
import React, { memo } from 'react';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useFileSelect } from "@/hooks/useFileSelect";

interface SelectFilesProps {
  action?: boolean;
  actionText?: string;
  actionFunction?: () => Promise<void>;
  onSelectionChange?: (selectedIds: string[]) => void;
}

const SelectFiles: React.FC<SelectFilesProps> = memo(({
  action = false,
  actionText = "",
  actionFunction,
  onSelectionChange
}) => {
  const { selectedFiles, files, loading, actions } = useFileSelect();

  // Notify parent component of selection changes
  React.useEffect(() => {
    onSelectionChange?.(selectedFiles);
  }, [selectedFiles, onSelectionChange]);

  return (
    <div className="space-y-4">
      <label className="text-sm font-medium">Select Files</label>
      <Select onValueChange={actions.addFile}>
        <SelectTrigger>
          <SelectValue placeholder="Choose a file" />
        </SelectTrigger>
        <SelectContent>
          {files.map((file) => (
            <SelectItem 
              key={file.id} 
              value={file.id}
              disabled={selectedFiles.includes(file.id)}
            >
              <div className="flex items-center gap-2">
                <FileText className="w-4 h-4" />
                {file.name}
              </div>
            </SelectItem>
          ))}
        </SelectContent>
      </Select>

      {selectedFiles.length > 0 && (
        <div className="flex flex-wrap gap-2">
          {selectedFiles.map((fileId) => {
            const file = files.find((f) => f.id === fileId);
            return (
              <div
                key={fileId}
                className="flex items-center gap-2 bg-secondary p-2 rounded-md"
              >
                <FileText className="w-4 h-4" />
                <span>{file?.name}</span>
                <button
                  onClick={() => actions.removeFile(fileId)}
                  className="text-muted-foreground hover:text-destructive"
                >
                  ×
                </button>
              </div>
            );
          })}
          {selectedFiles.length > 1 && (
            <Button 
              variant="ghost" 
              size="sm"
              onClick={actions.clearSelection}
              className="text-muted-foreground hover:text-destructive"
            >
              Clear All
            </Button>
          )}
        </div>
      )}

      {action && actionFunction && (
        <Button 
          onClick={actionFunction}
          disabled={loading || selectedFiles.length === 0}
          className="w-full"
        >
          {actionText}
        </Button>
      )}
    </div>
  );
});

SelectFiles.displayName = 'SelectFiles';

export default SelectFiles;