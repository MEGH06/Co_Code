import { FileText, Bot, Brain } from 'lucide-react';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

export default function Home() {
  return (
    <div className="container mx-auto pt-16 space-y-12">
      {/* Hero Section */}
      <div className="text-center space-y-6">
        <h1 className="text-6xl font-bold">
          <span className="text-foreground">OOPS!</span>{' '}
          <span className="bg-gradient-to-r from-pink-500 to-purple-500 text-transparent bg-clip-text">
            I DIDN'T STUDY
          </span>
        </h1>
        <h2 className="text-4xl font-semibold text-foreground/80">
          BUT YOU CAN NOW!
        </h2>
        <Button
          size="lg"
          className="bg-gradient-to-r from-pink-500 to-purple-500 text-white hover:from-pink-600 hover:to-purple-600 transition-all duration-300"
          asChild
        >
          <Link href="/upload">Get Started</Link>
        </Button>
      </div>

      {/* Features Grid */}
      <div className="px-2 grid grid-cols-1 md:grid-cols-3 gap-8">
        {/* Panic Notes Card */}
        <Link href="/panic-notes" className="group">
          <div className="bg-pink-500 rounded-2xl p-2 h-80 flex flex-col items-center justify-center text-white transition-transform duration-300 group-hover:scale-105">
            <FileText className="w-16 h-16 mb-4" />
            <h3 className="text-2xl font-semibold text-center">
              Generate Your Panic Notes
            </h3>
          </div>
        </Link>

        {/* CramBot Card */}
        <Link href="/crambot" className="group">
          <div className="bg-purple-500 rounded-2xl p-2 h-80 flex flex-col items-center justify-center text-white transition-transform duration-300 group-hover:scale-105">
            <Bot className="w-16 h-16 mb-4" />
            <h3 className="text-2xl font-semibold text-center">
              Ask CramBot Anything
            </h3>
          </div>
        </Link>

        {/* Quizzard Card */}
        <Link href="/quizzard" className="group">
          <div className="bg-purple-500 rounded-2xl p-2 h-80 flex flex-col items-center justify-center text-white transition-transform duration-300 group-hover:scale-105">
            <Brain className="w-16 h-16 mb-4" />
            <h3 className="text-2xl font-semibold text-center">Quizzard</h3>
          </div>
        </Link>
      </div>
    </div>
  );
}