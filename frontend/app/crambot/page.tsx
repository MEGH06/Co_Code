"use client";

// import { useChat } from "@ai-sdk/react";
import { Send, Trash2 } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import useChat from "@/hooks/useChat";

export default function ChatPage() {
  // const { messages, input, handleInputChange, handleSubmit, reload } = useChat()
  const { messages, input, setInput, handleSubmit, loading } = useChat();

  return (
    <div className="flex h-full pt-2 max-h-screen bg-background">
      <Card className="flex flex-col h-full w-full max-w-3xl mx-auto rounded-xl shadow-lg ">
        <CardHeader className="flex flex-row items-center justify-between space-y-0 p-4">
          <CardTitle className="text-2xl font-bold">CramBot</CardTitle>
          <div className="flex items-center gap-2">
            <Button variant="ghost" size="icon" className="rounded-full">
              <Trash2 className="h-5 w-5" />
              <span className="sr-only">Clear chat</span>
            </Button>
          </div>
        </CardHeader>
        <CardContent className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={cn(
                "flex w-max max-w-[80%] flex-col gap-2 rounded-lg px-4 py-2 text-sm",
                message.type === "user"
                  ? "ml-auto bg-primary text-primary-foreground"
                  : "bg-muted"
              )}
            >
              {message.message}
            </div>
          ))}
          {loading && (
            <div className="flex w-max max-w-[80%] flex-col gap-2 rounded-lg px-4 py-2 text-sm bg-muted">
              <div className="flex space-x-2">
                <div className="w-2 h-2 rounded-full bg-foreground/30 animate-bounce" />
                <div className="w-2 h-2 rounded-full bg-foreground/30 animate-bounce [animation-delay:0.2s]" />
                <div className="w-2 h-2 rounded-full bg-foreground/30 animate-bounce [animation-delay:0.4s]" />
              </div>
            </div>
          )}
        </CardContent>
        <CardFooter className="p-4 pt-2">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSubmit();
            }}
            className="flex w-full gap-2"
          >
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask CramBot anything..."
              className="flex-1"
            />
            <Button type="submit" size="icon" disabled={false || !input}>
              <Send className="h-5 w-5" />
              <span className="sr-only">Send message</span>
            </Button>
          </form>
        </CardFooter>
      </Card>
    </div>
  );
}
