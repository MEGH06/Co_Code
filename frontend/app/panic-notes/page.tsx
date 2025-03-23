"use client";

import { useState, useCallback } from "react";
import { Download, Copy, FileText } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Progress } from "@/components/ui/progress";
import { toast } from "react-toastify";
import useFileSelect from "@/hooks/useFileSelect";
import SelectFiles from "@/components/shared/SelectFiles";
import { 
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger 
} from "@/components/ui/dropdown-menu";
import jsPDF from 'jspdf';


export default function PanicNotesPage() {
  const [generating, setGenerating] = useState(false);
  const [progress, setProgress] = useState(0);
  const [notes, setNotes] = useState<string>("");

  const { files, loading, setLoading } = useFileSelect();

  // Track selected files from the SelectFiles component
  const [currentSelection, setCurrentSelection] = useState<string[]>([]);

  const handleSelectionChange = useCallback((selectedIds: string[]) => {
    setCurrentSelection(selectedIds);
  }, []);

  const generateNotes = useCallback(async () => {
    setLoading(true);

    if (currentSelection.length === 0) {
      toast.error("Please select at least one file");
      setLoading(false);
      return;
    }

    setGenerating(true);
    setProgress(0);

    try {
      const selectedFileData = files.filter((file) =>
        currentSelection.includes(file.id)
      );
      let generatedNotes = "";

      for (let i = 0; i < selectedFileData.length; i++) {
        const file = selectedFileData[i];
        // Simulate processing delay
        await new Promise((resolve) => setTimeout(resolve, 1000));

        generatedNotes += `# Notes from ${file.name}\n\n`;
        generatedNotes += `## Key Points\n`;
        generatedNotes += `- Important concept 1 from ${file.name}\n`;
        generatedNotes += `- Critical information about the topic\n`;
        generatedNotes += `- Key takeaway from this section\n\n`;

        setProgress(((i + 1) / selectedFileData.length) * 100);
      }

      setNotes(generatedNotes);
      toast.success("Notes generated successfully");
    } catch (error) {
      console.error("Error generating notes:", error);
      toast.error("Failed to generate notes");
    } finally {
      setGenerating(false);
      setProgress(0);
      setLoading(false);
    }
  }, [currentSelection, files, setLoading]);

  const copyToClipboard = useCallback(async () => {
    try {
      await navigator.clipboard.writeText(notes);
      toast.success("Notes copied to clipboard");
    } catch (error) {
      console.error("Error copying to clipboard:", error);
      toast.error("Failed to copy notes");
    }
  }, [notes]);

  // const downloadNotes = useCallback(() => {
  //   try {
  //     const blob = new Blob([notes], { type: "text/plain" });
  //     const url = URL.createObjectURL(blob);
  //     const a = document.createElement("a");
  //     a.href = url;
  //     a.download = "panic-notes.txt";
  //     document.body.appendChild(a);
  //     a.click();
  //     document.body.removeChild(a);
  //     URL.revokeObjectURL(url);

  //     toast.success("Notes downloaded successfully");
  //   } catch (error) {
  //     console.error("Error downloading notes:", error);
  //     toast.error("Failed to download notes");
  //   }
  // }, [notes]);


  const downloadPDF = useCallback(() => {
    try {
      const pdf = new jsPDF();
      
      // Split notes into lines and add to PDF
      const lines = notes.split('\n');
      let yPosition = 10;
      
      lines.forEach(line => {
        // Handle headers
        if (line.startsWith('# ')) {
          pdf.setFontSize(16);
          pdf.setFont('helvetica', 'bold');
        } else if (line.startsWith('## ')) {
          pdf.setFontSize(14);
          pdf.setFont('helvetica', 'bold');
        } else {
          pdf.setFontSize(12);
          pdf.setFont('helvetica', 'normal');
        }
        
        if (line.trim()) {
          pdf.text(line.replace(/^#+ /, ''), 10, yPosition);
          yPosition += 7;
        }
      });

      pdf.save('panic-notes.pdf');
      toast.success("PDF downloaded successfully");
    } catch (error) {
      console.error('Error downloading PDF:', error);
      toast.error("Failed to download PDF");
    }
  }, [notes]);

  const downloadAsText = useCallback(() => {
    try {
      const blob = new Blob([notes], { type: 'text/plain' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = 'panic-notes.txt';
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      
      toast.success("Text file downloaded successfully");
    } catch (error) {
      console.error('Error downloading text:', error);
      toast.error("Failed to download text file");
    }
  }, [notes]);


  return (
    <div className="container mx-auto pt-2 space-y-8 p-8">
      <div className="text-center">
        <h1 className="text-4xl font-bold mb-2">Generate Panic Notes</h1>
        <p className="text-muted-foreground">
          Select your files and we'll create concise study notes
        </p>
      </div>

      <div className="max-w-2xl mx-auto space-y-6">
        <SelectFiles
          action={true}
          actionFunction={generateNotes}
          actionText="Generate Notes"
          onSelectionChange={handleSelectionChange}
        />

        {generating && (
          <div className="space-y-2">
            <Progress value={progress} />
            <p className="text-sm text-muted-foreground text-center">
              Generating notes... {Math.round(progress)}%
            </p>
          </div>
        )}

        {notes && (
          <div className="space-y-4">
            <div className="flex justify-end gap-2">
              <Button
                variant="outline"
                size="sm"
                onClick={copyToClipboard}
                disabled={loading}
              >
                <Copy className="w-4 h-4 mr-2" />
                Copy
              </Button>
              <DropdownMenu>
                <DropdownMenuTrigger asChild>
                  <Button variant="outline" size="sm" disabled={loading}>
                    <Download className="w-4 h-4 mr-2" />
                    Download
                  </Button>
                </DropdownMenuTrigger>
                <DropdownMenuContent>
                  <DropdownMenuItem onClick={downloadAsText}>
                    <FileText className="w-4 h-4 mr-2" />
                    Download as Text
                  </DropdownMenuItem>
                  <DropdownMenuItem onClick={downloadPDF}>
                    <FileText className="w-4 h-4 mr-2" />
                    Download as PDF
                  </DropdownMenuItem>
                </DropdownMenuContent>
              </DropdownMenu>
            </div>
            <div className="bg-card p-6 rounded-lg">
              <pre className="whitespace-pre-wrap font-mono text-sm">
                {notes}
              </pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
