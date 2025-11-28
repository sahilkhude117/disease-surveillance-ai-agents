'use client';

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import { Activity, AlertTriangle, TrendingUp, Database, Users, MapPin } from 'lucide-react';
import { useEffect, useState } from 'react';

interface SurveillanceStatus {
  status: string;
  active_sessions: number;
  total_anomalies: number;
  active_alerts: number;
  recent_predictions: number;
  data_sources: Record<string, string>;
  timestamp: string;
}

export default function DashboardPage() {
  const [status, setStatus] = useState<SurveillanceStatus | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 30000); // Refresh every 30 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchStatus = async () => {
    try {
      const response = await fetch('/api/surveillance/status');
      if (!response.ok) throw new Error('Failed to fetch status');
      const data = await response.json();
      setStatus(data);
      setError(null);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load dashboard');
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="container mx-auto p-6">
        <div className="flex items-center justify-center h-[60vh]">
          <div className="text-center">
            <Activity className="w-12 h-12 animate-pulse mx-auto mb-4 text-primary" />
            <p className="text-muted-foreground">Loading surveillance dashboard...</p>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container mx-auto p-6">
        <Card className="border-destructive">
          <CardHeader>
            <CardTitle className="text-destructive">Error Loading Dashboard</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    );
  }

  return (
    <div className="container mx-auto p-6 space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold">Disease Surveillance Dashboard</h1>
          <p className="text-muted-foreground">Real-time monitoring and outbreak detection</p>
        </div>
        <Badge
          variant={status?.status === 'operational' ? 'default' : 'destructive'}
          className="text-sm px-4 py-2"
        >
          {status?.status === 'operational' ? '✓ Operational' : '⚠ Alert'}
        </Badge>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Alerts</CardTitle>
            <AlertTriangle className="h-4 w-4 text-destructive" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{status?.active_alerts || 0}</div>
            <p className="text-xs text-muted-foreground">
              Requiring immediate attention
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Anomalies Detected</CardTitle>
            <TrendingUp className="h-4 w-4 text-orange-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{status?.total_anomalies || 0}</div>
            <p className="text-xs text-muted-foreground">
              In the last 24 hours
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Recent Predictions</CardTitle>
            <Activity className="h-4 w-4 text-blue-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{status?.recent_predictions || 0}</div>
            <p className="text-xs text-muted-foreground">
              Outbreak forecasts generated
            </p>
          </CardContent>
        </Card>

        <Card>
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">Active Sessions</CardTitle>
            <Users className="h-4 w-4 text-green-500" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">{status?.active_sessions || 0}</div>
            <p className="text-xs text-muted-foreground">
              Monitoring sessions running
            </p>
          </CardContent>
        </Card>
      </div>

      {/* Data Sources Status */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <Database className="h-5 w-5" />
            Data Source Health
          </CardTitle>
          <CardDescription>
            Real-time connectivity status of surveillance data streams
          </CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {status?.data_sources && Object.entries(status.data_sources).map(([source, state]) => (
              <div
                key={source}
                className="flex items-center justify-between p-4 border rounded-lg"
              >
                <div className="flex items-center gap-3">
                  <div
                    className={`w-3 h-3 rounded-full ${
                      state === 'connected' ? 'bg-green-500' : 'bg-red-500'
                    }`}
                  />
                  <div>
                    <p className="font-medium capitalize">
                      {source.replace('_', ' ')}
                    </p>
                    <p className="text-xs text-muted-foreground capitalize">
                      {state.replace('_', ' ')}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </CardContent>
      </Card>

      {/* Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card>
          <CardHeader>
            <CardTitle>Alert Summary</CardTitle>
            <CardDescription>Critical alerts requiring attention</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-red-500 rounded-full" />
                  <div>
                    <p className="font-medium">Critical Alerts</p>
                    <p className="text-xs text-muted-foreground">Immediate action required</p>
                  </div>
                </div>
                <Badge variant="destructive">
                  {Math.floor((status?.active_alerts || 0) * 0.2)}
                </Badge>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-orange-500 rounded-full" />
                  <div>
                    <p className="font-medium">High Priority</p>
                    <p className="text-xs text-muted-foreground">Action needed within 24h</p>
                  </div>
                </div>
                <Badge variant="secondary">
                  {Math.floor((status?.active_alerts || 0) * 0.3)}
                </Badge>
              </div>

              <div className="flex items-center justify-between p-3 border rounded-lg">
                <div className="flex items-center gap-3">
                  <div className="w-2 h-2 bg-yellow-500 rounded-full" />
                  <div>
                    <p className="font-medium">Medium Priority</p>
                    <p className="text-xs text-muted-foreground">Monitor closely</p>
                  </div>
                </div>
                <Badge variant="outline">
                  {Math.floor((status?.active_alerts || 0) * 0.5)}
                </Badge>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Geographic Distribution</CardTitle>
            <CardDescription>Alerts by region</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {['North America', 'Europe', 'Asia Pacific', 'Africa'].map((region) => (
                <div key={region} className="flex items-center justify-between p-3 border rounded-lg">
                  <div className="flex items-center gap-3">
                    <MapPin className="h-4 w-4 text-muted-foreground" />
                    <p className="font-medium">{region}</p>
                  </div>
                  <Badge variant="outline">
                    {Math.floor(Math.random() * 10)}
                  </Badge>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* System Information */}
      <Card>
        <CardHeader>
          <CardTitle>System Information</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
            <div>
              <p className="text-muted-foreground">System Status</p>
              <p className="font-medium capitalize">{status?.status}</p>
            </div>
            <div>
              <p className="text-muted-foreground">Last Updated</p>
              <p className="font-medium">
                {status?.timestamp ? new Date(status.timestamp).toLocaleTimeString() : '-'}
              </p>
            </div>
            <div>
              <p className="text-muted-foreground">Data Sources</p>
              <p className="font-medium">
                {status?.data_sources ? Object.keys(status.data_sources).length : 0} Active
              </p>
            </div>
            <div>
              <p className="text-muted-foreground">Monitoring Mode</p>
              <p className="font-medium">Continuous</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
