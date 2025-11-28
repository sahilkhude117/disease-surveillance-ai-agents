'use client';

import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Brain, Search } from 'lucide-react';
import { useState } from 'react';

interface ThinkingLog {
  thinking_id: string;
  agent_name: string;
  thinking_stage: string;
  thought_content: string;
  thinking_stage_output: string;
  agent_output: string;
  conversation_id: string;
  user_query: string;
  status: string;
  created_date: string;
}

export default function ThinkingLogsPage() {
  const [sessionId, setSessionId] = useState('');
  const [logs, setLogs] = useState<ThinkingLog[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const fetchLogs = async () => {
    if (!sessionId.trim()) {
      setError('Please enter a session ID');
      return;
    }

    setLoading(true);
    setError('');
    try {
      const response = await fetch(`/api/thinking-logs/${sessionId}`);
      if (!response.ok) throw new Error('Failed to fetch logs');
      const data = await response.json();
      setLogs(data.thinking_logs || []);
    } catch (err) {
      setError('Failed to load thinking logs. Please check the session ID.');
      setLogs([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-6 space-y-6">
      <div>
        <h1 className="text-3xl font-bold flex items-center gap-2">
          <Brain className="h-8 w-8 text-primary" />
          Agent Thinking Logs
        </h1>
        <p className="text-muted-foreground">
          Transparent view of AI agent reasoning and decision-making
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Search Logs by Session ID</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="flex gap-2">
            <Input
              placeholder="Enter session ID..."
              value={sessionId}
              onChange={(e) => setSessionId(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && fetchLogs()}
            />
            <Button onClick={fetchLogs} disabled={loading}>
              <Search className="h-4 w-4 mr-2" />
              {loading ? 'Loading...' : 'Search'}
            </Button>
          </div>
          {error && <p className="text-destructive text-sm mt-2">{error}</p>}
        </CardContent>
      </Card>

      {logs.length > 0 && (
        <div className="space-y-4">
          {logs.map((log) => (
            <Card key={log.thinking_id}>
              <CardHeader>
                <div className="flex items-start justify-between">
                  <div>
                    <CardTitle className="text-lg">{log.agent_name}</CardTitle>
                    <p className="text-sm text-muted-foreground mt-1">
                      Stage: {log.thinking_stage}
                    </p>
                  </div>
                  <Badge variant="outline">
                    {new Date(log.created_date).toLocaleTimeString()}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-3">
                <div>
                  <p className="text-sm font-medium text-muted-foreground">Thought Process:</p>
                  <p className="text-sm mt-1">{log.thought_content}</p>
                </div>
                {log.thinking_stage_output && (
                  <div>
                    <p className="text-sm font-medium text-muted-foreground">Stage Output:</p>
                    <pre className="text-xs mt-1 bg-muted p-3 rounded-lg overflow-x-auto">
                      {log.thinking_stage_output}
                    </pre>
                  </div>
                )}
              </CardContent>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
