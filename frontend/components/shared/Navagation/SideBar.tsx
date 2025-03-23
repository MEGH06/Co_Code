"use client";

import { Menu, Home, Upload, AlertCircle, Bot, Award } from "lucide-react";
import { ThemeToggle } from '@/components/theme-toggle';
import { useCallback, useState } from "react";
const SideBar = () => {
  const [showMenu, setShowMenu] = useState(false);

  const toggleMenue = useCallback(() => {
    setShowMenu((prev) => !prev);
  }, [showMenu]);
  return showMenu ? (
    <>
      <nav className="w-64 flex flex-col justify-between items-start bg-card/50 p-4 space-y-4">
        <div className="w-[100%]">
        <div className="flex justify-between items-center space-x-2 mb-8">
          <span className="font-bold text-lg">Menu</span>
          <span>
            <Menu className="w-6 h-6 cursor-pointer" onClick={toggleMenue} />
          </span>
        </div>
        <div className="space-y-2">
          <a
            href="/"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Home className="w-6 h-6" />
            </span>
            <span>Home</span>
          </a>
          <a
            href="/upload"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Upload className="w-6 h-6" />
            </span>
            <span>Upload Files</span>
          </a>
          <a
            href="/panic-notes"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <AlertCircle className="w-6 h-6" />
            </span>
            <span>Panic Notes</span>
          </a>
          <a
            href="/crambot"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Bot className="w-6 h-6" />
            </span>
            <span>CramBot</span>
          </a>
          <a
            href="/quizzard"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Award className="w-6 h-6" />
            </span>
            <span>Quizzard</span>
          </a>
        </div>
        </div>
        <ThemeToggle />
      </nav>
    </>
  ) : (
    <>
      <nav className="w-20 flex flex-col justify-between items-start bg-card/50 p-4 space-y-4">
        <div>
        <div className="flex justify-center items-center space-x-2 mb-8">
          <span>
            <Menu className="w-6 h-6 cursor-pointer" onClick={toggleMenue}/>
          </span>
        </div>
        <div className="space-y-2">
          <a
            href="/"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Home className="w-6 h-6" />
            </span>
          </a>
          <a
            href="/upload"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Upload className="w-6 h-6" />
            </span>
          </a>
          <a
            href="/panic-notes"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <AlertCircle className="w-6 h-6" />
            </span>
          </a>
          <a
            href="/crambot"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Bot className="w-6 h-6" />
            </span>
          </a>
          <a
            href="/quizzard"
            className="flex items-center space-x-2 p-2 rounded-lg hover:bg-accent transition-colors"
          >
            <span>
              <Award className="w-6 h-6" />
            </span>
          </a>
        </div>
        </div>
        <ThemeToggle />
      </nav>
    </>
  );
};

export default SideBar;
