import './globals.css';
import type { Metadata } from 'next';
import { Inter } from 'next/font/google';
import { Providers } from './providers';
import SideBar from '@/components/shared/Navagation/SideBar';
import { ToastContainer} from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

const inter = Inter({ subsets: ['latin'] });

export const metadata: Metadata = {
  title: 'OOPS! I DIDNT STUDY',
  description: 'Your ultimate study companion',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} min-h-screen bg-background`}>
        <Providers>
          <div className="flex min-h-screen">
            {/* Sidebar */}
            <SideBar />
            {/* Main Content */}
            <main className="flex-1 px-2 custom-scrollbar overflow-y-auto max-h-screen">
              <div className="flex justify-end">
              </div>
              {children}
            </main>
          </div>
          <ToastContainer 
        position="bottom-right" 
        theme="dark"
        autoClose={3000}
        hideProgressBar={true}
        limit={2}
      />
        </Providers>
      </body>
    </html>
  );
}