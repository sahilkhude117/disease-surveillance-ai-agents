'use client';

import { Poppins } from 'next/font/google';
import './globals.css';
import { useState, useEffect } from 'react';
import SidebarApp from '@/components/SidebarApp';
import { MessageCircle, X } from 'lucide-react';
import { usePathname } from 'next/navigation';

const poppins = Poppins({
  weight: ['400', '500', '600', '700'],
  display: 'swap',
  style: ['italic', 'normal'],
  subsets: ['latin'],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [chatOpen, setChatOpen] = useState(false);
  const [mounted, setMounted] = useState(false);
  const pathname = usePathname();

  useEffect(() => {
    setMounted(true);
  }, []);

  const toggleChat = () => {
    if (!chatOpen) {
      window.location.href = '/chat';
    }
  };

  return (
    <html lang="en" className={poppins.className}>
      <head>
        <title>Disease Surveillance AI - Proactive Outbreak Detection</title>
        <meta name="description" content="AI-powered proactive disease outbreak detection and prevention system" />
      </head>
      <body className="antialiased min-h-screen">
        <div className="flex h-screen bg-black overflow-hidden relative">
          {/* Mobile Overlay */}
          {sidebarOpen && (
            <div 
              className="fixed inset-0 bg-black/60 backdrop-blur-sm z-[45] lg:hidden"
              onClick={() => setSidebarOpen(false)}
            />
          )}

          {/* Sidebar */}
          <SidebarApp sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />

          {/* Main Content */}
          <div className="flex-1 flex flex-col min-w-0 ml-0">
            {/* Header */}
            <header className="h-14 md:h-16 bg-gradient-to-b from-gray-900/50 to-transparent backdrop-blur-xl border-b border-white/5 flex items-center justify-between px-3 md:px-6 relative flex-shrink-0">
              <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/[0.02] to-transparent pointer-events-none" />
              
              {/* Left Side - System Info */}
              <div className="flex items-center gap-1.5 md:gap-3 relative z-10">
                {mounted && (
                  <div className="bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl rounded-lg md:rounded-xl px-2 md:px-4 py-1.5 md:py-2 border border-white/10 hover:border-white/20 transition-all duration-200">
                    <div className="flex items-center gap-1 md:gap-2">
                      <div className="w-5 h-5 md:w-7 md:h-7 rounded-lg bg-gradient-to-br from-green-500/20 to-green-600/10 flex items-center justify-center flex-shrink-0">
                        <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse" />
                      </div>
                      <div className="min-w-0">
                        <div className="text-[7px] md:text-[9px] text-gray-500 uppercase tracking-wider leading-tight">Status</div>
                        <div className="text-[11px] md:text-sm font-bold text-white leading-tight">Active</div>
                      </div>
                    </div>
                  </div>
                )}
              </div>

              {/* Right Side - Chat Button */}
              <div className="flex items-center gap-1.5 md:gap-3 relative z-10">
                {mounted && pathname !== '/chat' && (
                  <button
                    onClick={toggleChat}
                    className="relative px-3 md:px-4 py-1.5 md:py-2 rounded-lg md:rounded-xl bg-gradient-to-br from-green-500/20 to-green-600/10 hover:from-green-500/30 hover:to-green-600/20 border border-green-500/20 flex items-center gap-2 transition-all duration-200 hover:scale-105 active:scale-95 group"
                    title="Open Chat"
                  >
                    <MessageCircle size={16} className="text-green-400 md:w-5 md:h-5 group-hover:scale-110 transition-transform flex-shrink-0" />
                    <span className="text-xs md:text-sm font-semibold text-green-400 group-hover:text-green-300 transition-colors">Chat</span>
                  </button>
                )}
              </div>
            </header>

            {/* Content */}
            <main className="flex-1 overflow-auto bg-black scrollbar-thin scrollbar-thumb-white/10 scrollbar-track-transparent">
              {children}
            </main>
          </div>
        </div>
      </body>
    </html>
  );
}
