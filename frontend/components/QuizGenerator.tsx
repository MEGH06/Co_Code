"use client";

// import {
//   Card,
//   CardContent,
//   CardFooter,
//   CardHeader,
//   CardTitle,
// } from "@/components/ui/card";
// import { Button } from "@/ui/button";

// const QuizGenerator = () => {
//   return (
//     <div className="flex h-full pt-2 max-h-screen bg-background">
//     <Card className="flex flex-col h-full w-full max-w-3xl mx-auto rounded-xl shadow-lg ">
//       <CardHeader className="flex flex-row items-center justify-between space-y-0 p-4">
//         <CardTitle className="text-2xl font-bold">Select File for quizes</CardTitle>
//       </CardHeader>
//       <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
//         <SelectFiles />
//       </CardContent>
//       <CardFooter className="p-4 pt-2">
//         <Button>
//           Start Quiz
//         </Button>
//       </CardFooter>
//     </Card>
//   </div>
//   )
// }

import { useCallback, useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { QuizParams } from "@/app/quizzard/page";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import SelectFiles from "./shared/SelectFiles";
import { toast } from "react-toastify";
interface QuizGeneratorProps {
  onGenerate: (params: QuizParams) => void;
}

const QuizGenerator: React.FC<QuizGeneratorProps> = ({ onGenerate }) => {
  const [params, setParams] = useState<QuizParams>({
    topic: "",
    fileid: [],
    difficulty: "easy",
    numberOfQuestions: 10,
  });

  const questionCounts = ["10", "20", "30", "40", "50"];
  const difficultys = ["easy", "medium", "hard", "extrem"];
  const handleGenerate = () => {
    onGenerate(params);
  };
  
  const handleSelectionChange = useCallback((selectedIds: string[]) => {
    setParams({...params,fileid : selectedIds});
  }, []);

  return (
    <div className="space-y-4">
      <SelectFiles onSelectionChange={handleSelectionChange}/>
      <div className="space-y-2">
        <label className="text-sm font-medium">Question count</label>
        <Select value={params.numberOfQuestions.toString()}
          onValueChange={(value) =>
            setParams({ ...params, numberOfQuestions: parseInt(value) })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="choose a count" />
          </SelectTrigger>
          <SelectContent>
            {questionCounts.map((count) => (
              <SelectItem key={count} value={count}>
                <div className="flex items-center gap-2">{count}</div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-2">
        <label className="text-sm font-medium">Select Difficulty</label>
        <Select value={params.difficulty}
          onValueChange={(value) =>
            setParams({ ...params, difficulty: value })
          }
        >
          <SelectTrigger>
            <SelectValue placeholder="Choose a difficulty" />
          </SelectTrigger>
          <SelectContent>
            {difficultys.map((difficulty) => (
              <SelectItem key={difficulty} value={difficulty}>
                <div className="flex items-center gap-2">{difficulty}</div>
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="space-y-2">
        <Label>Specfic topic</Label>
        <Input
          value={params.topic}
          onChange={(e) => setParams({ ...params, topic: e.target.value })}
          placeholder="Enter specfic topic"
        />
      </div>
      <Button onClick={() => {
        if (!(params.fileid && params.topic)){
          toast.warning("Please select all fields")
          return;
        } 
        handleGenerate()
      }} className="w-full">
        Generate Quiz
      </Button>
    </div>
  );
};

export default QuizGenerator;
