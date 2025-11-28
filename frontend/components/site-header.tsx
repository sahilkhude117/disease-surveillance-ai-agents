'use client';

import Link from 'next/link';
import { Activity, Moon, Sun } from 'lucide-react';
import { Button } from './ui/button';
import { useTheme } from 'next-themes';
import { usePathname } from 'next/navigation';
import { cn } from '@/lib/utils';

export function SiteHeader() {
  const { setTheme, theme } = useTheme();
  const pathname = usePathname();

  const navLinks = [
    { href: '/chat', label: 'Chat', icon: '💬' },
    { href: '/dashboard', label: 'Dashboard', icon: '📊' },
    { href: '/alerts', label: 'Alerts', icon: '🚨' },
    { href: '/predictions', label: 'Predictions', icon: '📈' },
    { href: '/anomalies', label: 'Anomalies', icon: '🔍' },
    { href: '/reports', label: 'Reports', icon: '📄' },
    { href: '/thinking-logs', label: 'Thinking Logs', icon: '🧠' },
  ];

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
      <div className="container flex h-16 items-center justify-between px-6">
        <Link href="/chat" className="flex items-center gap-2 hover:opacity-80 transition-opacity" prefetch={false}>
          <Activity className="w-8 h-8 text-primary" />
          <div className="flex flex-col">
            <span className="font-bold text-lg text-primary">Disease Surveillance AI</span>
            <span className="text-xs text-muted-foreground">Proactive Outbreak Detection</span>
          </div>
        </Link>
        
        <nav className="hidden items-center gap-6 text-sm font-medium md:flex">
          {navLinks.map((link) => (
            <Link
              key={link.label}
              href={link.href}
              className={cn(
                'flex items-center gap-1.5 transition-colors hover:text-foreground/80',
                pathname === link.href
                  ? 'text-foreground font-semibold'
                  : 'text-muted-foreground'
              )}
              prefetch={false}
            >
              <span>{link.icon}</span>
              {link.label}
            </Link>
          ))}
        </nav>
        
        <div className="flex items-center gap-4">
          <Button variant="ghost" size="icon" onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}>
            <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
            <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  );
}
