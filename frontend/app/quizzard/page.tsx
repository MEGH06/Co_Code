"use client";

import { cn } from "@/lib/utils";
import { useState, useEffect } from "react";
import {
  Trophy,
  ArrowRight,
  ArrowLeft,
  Timer,
  Clock,
  CheckCircle,
  XCircle,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Progress } from "@/components/ui/progress";
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import QuizGenerator from "@/components/QuizGenerator";
import { dummyQuiz } from "@/lib/dummy";

// Custom tooltip with improved styling
const CustomTooltip = ({
  active,
  payload,
}: {
  active?: boolean;
  payload?: any[];
}) => {
  if (active && payload && payload.length > 0) {
    const data = payload[0].payload;

    return (
      <div className="bg-white p-3 border rounded-md shadow-lg">
        <p className="font-medium text-lg border-b pb-1 mb-2 text-black">{`Question ${data.questionNum}`}</p>
        <div className="grid grid-cols-2 gap-x-3 gap-y-1 text-sm">
          <span className="text-gray-600">Time:</span>
          <span className="text-black font-medium">{data.value} seconds</span>
          <span className="text-gray-600">Status:</span>
          <span
            className={`font-medium ${
              data.isCorrect ? "text-green-600" : "text-red-600"
            }`}
          >
            {data.isCorrect ? "Correct" : "Incorrect"}
          </span>
        </div>
      </div>
    );
  }
  return null;
};

interface QuizQuestion {
  id: number;
  question: string;
  options: string[];
  correctAnswer: number;
}

interface QuizAttempt {
  questionId: number;
  timeSpent: number;
  isCorrect: boolean;
  selectedAnswer: number;
}

export interface QuizParams {
  topic: string;
  fileid: string[];
  difficulty: string;
  numberOfQuestions: number;
}

export default function QuizPage() {
  const [quizState, setQuizState] = useState<QuizQuestion[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [selectedAnswer, setSelectedAnswer] = useState<number | null>(null);
  const [attempts, setAttempts] = useState<QuizAttempt[]>([]);
  const [showResults, setShowResults] = useState(false);
  const [questionStartTime, setQuestionStartTime] = useState<number>(
    Date.now()
  );
  const [isReview, setIsReview] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [quizStartTime, setQuizStartTime] = useState<number>(Date.now());

  // Timer effect
  useEffect(() => {
    if (!showResults && !isReview) {
      const timer = setInterval(() => {
        setCurrentTime(Math.round((Date.now() - questionStartTime) / 1000));
      }, 1000);
      return () => clearInterval(timer);
    }
  }, [questionStartTime, showResults, isReview]);

  const progress = ((currentQuestion + 1) / quizState.length) * 100;

  const handleGenerateQuiz = async (params: QuizParams) => {
    // Here you would make your API call
    // For now using dummy data
    console.log(params);

    setQuizState(dummyQuiz);
    resetQuiz();
  };

  const handleAnswerSelect = (optionIndex: number) => {
    setSelectedAnswer(optionIndex);
  };

  const handleNext = () => {
    if (selectedAnswer === null && !isReview) return;

    const timeSpent = currentTime;

    if (!isReview) {
      const isCorrect =
        selectedAnswer === quizState[currentQuestion].correctAnswer;
      setAttempts([
        ...attempts,
        {
          questionId: currentQuestion,
          timeSpent,
          isCorrect,
          selectedAnswer: selectedAnswer!,
        },
      ]);
    }

    if (currentQuestion + 1 < quizState.length) {
      setCurrentQuestion(currentQuestion + 1);
      setSelectedAnswer(null);
      setQuestionStartTime(Date.now());
      setCurrentTime(0);
    } else {
      setShowResults(true);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
      // In review mode, we don't update the selected answer
      if (!isReview) {
        setSelectedAnswer(
          attempts[currentQuestion - 1]?.selectedAnswer ?? null
        );
      }
    }
  };

  const resetQuiz = () => {
    setCurrentQuestion(0);
    setSelectedAnswer(null);
    setAttempts([]);
    setShowResults(false);
    setIsReview(false);
    setQuestionStartTime(Date.now());
    setQuizStartTime(Date.now());
    setCurrentTime(0);
  };

  const startNewQuiz = () => {
    setQuizState([]);
    resetQuiz();
  };

  const startReview = () => {
    setIsReview(true);
    setCurrentQuestion(0);
    setShowResults(false);
  };

  const getPieChartData = () => {
    return attempts.map((attempt, index) => ({
      name: `Question ${index + 1}`,
      value: attempt.timeSpent,
      questionNum: index + 1,
      isCorrect: attempt.isCorrect,
    }));
  };

  const calculateQuizStats = () => {
    const totalTime = attempts.reduce(
      (sum, attempt) => sum + attempt.timeSpent,
      0
    );
    const correctAnswers = attempts.filter((a) => a.isCorrect).length;
    const incorrectAnswers = attempts.length - correctAnswers;
    const accuracyRate = Math.round((correctAnswers / attempts.length) * 100);
    const averageTimePerQuestion = Math.round(totalTime / attempts.length);
    const fastestQuestion = [...attempts].sort(
      (a, b) => a.timeSpent - b.timeSpent
    )[0];
    const slowestQuestion = [...attempts].sort(
      (a, b) => b.timeSpent - a.timeSpent
    )[0];

    return {
      totalTime,
      correctAnswers,
      incorrectAnswers,
      accuracyRate,
      averageTimePerQuestion,
      fastestQuestion,
      slowestQuestion,
    };
  };

  if (quizState.length === 0) {
    return (
      <div className="flex min-h-screen pt-2 bg-background">
        <Card className="flex flex-col w-full max-w-3xl mx-auto my-4">
          <CardHeader>
            <CardTitle>Quiz Generator</CardTitle>
          </CardHeader>
          <CardContent>
            <QuizGenerator onGenerate={handleGenerateQuiz} />
          </CardContent>
        </Card>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen pt-2 bg-background">
      <Card className="flex flex-col w-full max-w-3xl mx-auto my-4">
        <CardHeader className="flex flex-row items-center justify-between p-4 border-b">
          <CardTitle className="text-2xl font-bold">
            {showResults
              ? "Quiz Results"
              : `Question ${currentQuestion + 1} of ${quizState.length}`}
          </CardTitle>
          {!showResults && !isReview && (
            <div className="flex items-center gap-2">
              <Timer className="w-4 h-4" />
              <span className="text-sm text-muted-foreground">
                Time: {currentTime}s
              </span>
            </div>
          )}
        </CardHeader>

        <CardContent className="flex-1 p-6">
          {!showResults ? (
            <div className="space-y-6">
              <Progress value={progress} className="h-2" />
              <div className="space-y-4">
                <h2 className="text-xl font-semibold">
                  {quizState[currentQuestion].question}
                </h2>
                <div className="grid gap-3">
                  {quizState[currentQuestion].options.map((option, index) => {
                    const isCorrect =
                      index === quizState[currentQuestion].correctAnswer;
                    const currentAttempt = attempts[currentQuestion];
                    const isSelected = isReview
                      ? currentAttempt?.selectedAnswer === index
                      : selectedAnswer === index;

                    return (
                      <Button
                        key={index}
                        variant={isSelected ? "default" : "outline"}
                        className={cn(
                          "justify-start h-auto py-4 px-6 text-left opacity-100",
                          isReview &&
                            isCorrect &&
                            "bg-green-100 border-green-500 text-green-800",
                          isReview &&
                            !isCorrect &&
                            isSelected &&
                            "bg-red-100 border-red-500 text-red-800"
                        )}
                        onClick={() => !isReview && handleAnswerSelect(index)}
                        disabled={isReview}
                      >
                        {option}
                        {isReview && (
                          <span className="ml-2">
                            {isSelected && (
                              <span className="ml-2 px-2 py-1 text-xs font-medium rounded-full bg-gray-200">
                                Your answer
                              </span>
                            )}
                            {isCorrect && (
                              <span className="ml-2 px-2 py-1 text-xs font-medium rounded-full bg-green-200 text-green-800">
                                Correct
                              </span>
                            )}
                          </span>
                        )}
                      </Button>
                    );
                  })}
                </div>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <div className="text-center">
                <Trophy className="w-16 h-16 mx-auto text-yellow-500" />
                <h2 className="text-2xl font-bold mt-4">Quiz Complete!</h2>
                <p className="text-xl mt-2">
                  You scored {attempts.filter((a) => a.isCorrect).length} out of{" "}
                  {quizState.length}
                </p>
              </div>

              {attempts.length > 0 && (
                <div className="mt-6 space-y-8">
                  <div>
                    <h3 className="text-lg font-semibold mb-4 text-center">
                      Time Distribution per Question
                    </h3>
                    <div className="h-72 w-full">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={getPieChartData()}
                            cx="50%"
                            cy="50%"
                            labelLine={false}
                            outerRadius={90}
                            innerRadius={40}
                            fill="#8884d8"
                            dataKey="value"
                            nameKey="name"
                            paddingAngle={4}
                            animationBegin={0}
                            animationDuration={1500}
                            animationEasing="ease-in-out"
                          >
                            {getPieChartData().map((entry, index) => (
                              <Cell
                                key={`cell-${index}`}
                                fill={entry.isCorrect ? "#4CAF50" : "#F44336"} // Green for correct, red for incorrect
                                stroke="#fff" // White border
                                strokeWidth={1} // Thin border (1px)
                              />
                            ))}
                          </Pie>
                          <Tooltip content={<CustomTooltip />} />
                          <Legend
                            layout="horizontal"
                            verticalAlign="bottom"
                            align="center"
                            payload={[
                              {
                                value: "Correct",
                                type: "square",
                                color: "green",
                              },
                              {
                                value: "Incorrect",
                                type: "square",
                                color: "red",
                              },
                            ]}
                          />
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  <div className="mt-6 bg-gray-50 dark:bg-gray-800 rounded-xl p-6 shadow-sm">
                    <h3 className="text-lg font-semibold mb-6 text-center">
                      Quiz Performance Summary
                    </h3>
                    <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <Clock className="w-6 h-6 text-blue-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Total Time
                        </p>
                        <p className="text-xl font-bold">
                          {calculateQuizStats().totalTime}s
                        </p>
                      </div>
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <CheckCircle className="w-6 h-6 text-green-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Accuracy
                        </p>
                        <p className="text-xl font-bold">
                          {calculateQuizStats().accuracyRate}%
                        </p>
                      </div>
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <Timer className="w-6 h-6 text-purple-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Avg. Time
                        </p>
                        <p className="text-xl font-bold">
                          {calculateQuizStats().averageTimePerQuestion}s
                        </p>
                      </div>
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <Trophy className="w-6 h-6 text-yellow-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Score
                        </p>
                        <p className="text-xl font-bold">
                          {calculateQuizStats().correctAnswers}/
                          {quizState.length}
                        </p>
                      </div>
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <ArrowRight className="w-6 h-6 text-teal-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Fastest Q
                        </p>
                        <p className="text-xl font-bold">
                          Q{calculateQuizStats().fastestQuestion.questionId + 1}
                        </p>
                      </div>
                      <div className="flex flex-col items-center p-3 bg-white dark:bg-gray-700 rounded-lg shadow-sm">
                        <XCircle className="w-6 h-6 text-red-500 mb-2" />
                        <p className="text-sm text-gray-500 dark:text-gray-300">
                          Incorrect
                        </p>
                        <p className="text-xl font-bold">
                          {calculateQuizStats().incorrectAnswers}
                        </p>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}
        </CardContent>

        <CardFooter className="p-4 border-t">
          <div className="flex w-full gap-2">
            {!showResults && (
              <>
                <Button
                  onClick={handlePrevious}
                  disabled={currentQuestion === 0}
                  variant="outline"
                >
                  <ArrowLeft className="w-4 h-4 mr-2" />
                  Previous
                </Button>
                <Button
                  onClick={handleNext}
                  disabled={!isReview && selectedAnswer === null}
                >
                  {currentQuestion + 1 === quizState.length ? "Finish" : "Next"}
                  <ArrowRight className="w-4 h-4 ml-2" />
                </Button>
              </>
            )}
            {showResults && (
              <div className="flex w-full gap-2">
                <Button onClick={startReview} variant="outline">
                  Review Answers
                </Button>
                <Button onClick={startNewQuiz}>Start New Quiz</Button>
              </div>
            )}
          </div>
        </CardFooter>
      </Card>
    </div>
  );
}
