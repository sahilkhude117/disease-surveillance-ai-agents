import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const sessionId = searchParams.get('session_id');
    const reportType = searchParams.get('report_type');
    const days = searchParams.get('days') || '30';

    const params = new URLSearchParams();
    if (sessionId) params.append('session_id', sessionId);
    if (reportType) params.append('report_type', reportType);
    params.append('days', days);

    const response = await fetch(`${API_URL}/api/reports?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch reports');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Reports API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch reports' },
      { status: 500 }
    );
  }
}
