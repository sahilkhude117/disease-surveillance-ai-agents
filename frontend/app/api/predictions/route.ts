import { NextRequest, NextResponse } from 'next/server';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function GET(request: NextRequest) {
  try {
    const { searchParams } = new URL(request.url);
    const disease = searchParams.get('disease');
    const region = searchParams.get('region');
    const days = searchParams.get('days') || '30';

    const params = new URLSearchParams();
    if (disease) params.append('disease', disease);
    if (region) params.append('region', region);
    params.append('days', days);

    const response = await fetch(`${API_URL}/api/predictions?${params.toString()}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    });

    if (!response.ok) {
      throw new Error('Failed to fetch predictions');
    }

    const data = await response.json();
    return NextResponse.json(data);
  } catch (error) {
    console.error('Predictions API error:', error);
    return NextResponse.json(
      { error: 'Failed to fetch predictions' },
      { status: 500 }
    );
  }
}
