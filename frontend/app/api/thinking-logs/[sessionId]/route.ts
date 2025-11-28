import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(
  request: NextRequest,
  { params }: { params: { sessionId: string } }
) {
  try {
    const sessionId = params.sessionId;

    const response = await fetch(`${API_URL}/api/thinking-logs/${sessionId}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch thinking logs');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Thinking logs API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch thinking logs' },
      { status: 500 }
    );
  }
}
