'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import { Activity, Send, Loader2, Copy, RefreshCw, User, Bot } from 'lucide-react';
import { useEffect, useRef, useState } from 'react';
import Markdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface ChatMessage {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  agents_involved?: string[];
  timestamp?: string;
}

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      role: 'assistant',
      content: '👋 Hello! I am your **Disease Surveillance AI Assistant**.\n\n' +
        'I can help you with:\n' +
        '- 📊 Analyzing disease surveillance data from multiple sources\n' +
        '- 🔍 Detecting anomalies in health patterns\n' +
        '- 📈 Predicting disease outbreaks\n' +
        '- 🚨 Generating alerts for health officials\n' +
        '- 📄 Creating comprehensive surveillance reports\n\n' +
        'How can I assist you today?',
    },
  ]);
  const [input, setInput] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [sessionId, setSessionId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isGenerating) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsGenerating(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: input.trim(),
          session_id: sessionId,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        if (data.session_id) {
          setSessionId(data.session_id);
        }

        const assistantMessage: ChatMessage = {
          id: data.session_id || Date.now().toString(),
          role: 'assistant',
          content: data.response || 'Sorry, I received an empty response.',
          agents_involved: data.agents_involved || [],
          timestamp: data.timestamp,
        };

        setMessages((prev) => [...prev, assistantMessage]);
      } else {
        throw new Error(data.error || 'Failed to get response');
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: Date.now().toString(),
        role: 'assistant',
        content: `❌ Error: ${error instanceof Error ? error.message : 'Failed to connect to the server. Please make sure the backend is running.'}`,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsGenerating(false);
    }
  };

  const copyMessage = (content: string) => {
    navigator.clipboard.writeText(content);
  };

  return (
    <div className="container mx-auto h-[calc(100vh-4rem)] flex flex-col p-4">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Activity className="w-6 h-6 text-primary" />
          <h1 className="text-2xl font-bold">Disease Surveillance Chat</h1>
        </div>
        {sessionId && (
          <Badge variant="outline" className="gap-2">
            Session: {sessionId.substring(0, 8)}...
            <Button
              variant="ghost"
              size="icon"
              className="h-4 w-4 hover:bg-primary/20"
              onClick={() => copyMessage(sessionId)}
            >
              <Copy className="h-3 w-3" />
            </Button>
          </Badge>
        )}
      </div>

      {/* Chat Messages */}
      <Card className="flex-1 flex flex-col">
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-4">
            {messages.map((message, index) => (
              <div
                key={message.id}
                className={`flex gap-3 ${message.role === 'user' ? 'flex-row-reverse' : 'flex-row'}`}
              >
                {/* Avatar */}
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-primary text-primary-foreground'
                      : 'bg-secondary text-secondary-foreground'
                  }`}
                >
                  {message.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
                </div>

                {/* Message Content */}
                <div className={`flex-1 max-w-[80%] ${message.role === 'user' ? 'items-end' : 'items-start'}`}>
                  <div
                    className={`rounded-lg p-4 ${
                      message.role === 'user'
                        ? 'bg-primary text-primary-foreground'
                        : 'bg-muted'
                    }`}
                  >
                    {message.role === 'user' ? (
                      <p className="whitespace-pre-wrap">{message.content}</p>
                    ) : (
                      <div className="prose prose-sm dark:prose-invert max-w-none">
                        <Markdown remarkPlugins={[remarkGfm]}>{message.content}</Markdown>
                      </div>
                    )}
                  </div>

                  {/* Metadata */}
                  <div className="flex items-center gap-2 mt-1 text-xs text-muted-foreground">
                    {message.timestamp && (
                      <span>{new Date(message.timestamp).toLocaleTimeString()}</span>
                    )}
                    {message.agents_involved && message.agents_involved.length > 0 && (
                      <Badge variant="secondary" className="text-xs">
                        {message.agents_involved.length} agent{message.agents_involved.length > 1 ? 's' : ''} involved
                      </Badge>
                    )}
                  </div>

                  {/* Actions */}
                  {message.role === 'assistant' && (
                    <div className="flex gap-1 mt-2">
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-6 w-6"
                        onClick={() => copyMessage(message.content)}
                      >
                        <Copy className="h-3 w-3" />
                      </Button>
                    </div>
                  )}
                </div>
              </div>
            ))}

            {isGenerating && (
              <div className="flex gap-3">
                <div className="flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center bg-secondary text-secondary-foreground">
                  <Bot className="w-4 h-4" />
                </div>
                <div className="flex-1 max-w-[80%]">
                  <div className="rounded-lg p-4 bg-muted">
                    <div className="flex items-center gap-2">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">AI agents are analyzing...</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </ScrollArea>

        {/* Input Form */}
        <CardContent className="border-t p-4">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <Input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Ask about disease surveillance, anomalies, predictions..."
              disabled={isGenerating}
              className="flex-1"
            />
            <Button type="submit" disabled={isGenerating || !input.trim()}>
              {isGenerating ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <>
                  <Send className="w-4 h-4 mr-2" />
                  Send
                </>
              )}
            </Button>
          </form>
          <p className="text-xs text-muted-foreground mt-2 text-center">
            💡 Try: "Analyze current surveillance data" or "Run full outbreak prediction analysis"
          </p>
        </CardContent>
      </Card>
    </div>
  );
}
