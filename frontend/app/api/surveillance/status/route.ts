import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const response = await fetch(`${API_URL}/api/surveillance/status`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch surveillance status');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Surveillance status API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch surveillance status' },
      { status: 500 }
    );
  }
}
