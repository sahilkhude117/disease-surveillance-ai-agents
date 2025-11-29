# Disease Surveillance AI Agent System - Complete Project Documentation

## Executive Summary

The **Disease Surveillance AI Agent System** is a sophisticated multi-agent AI platform designed for proactive disease outbreak detection and prediction. Instead of waiting for manual disease reporting, the system continuously monitors multiple data streams using specialized AI agents to identify health threats before they become widespread crises. The platform uses advanced machine learning and natural language processing to transform healthcare from reactive to predictive.

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Folder and File Structure](#folder-and-file-structure)
3. [Technology Stack](#technology-stack)
4. [System Architecture](#system-architecture)
5. [Workflow and Data Flow](#workflow-and-data-flow)
6. [Key Features](#key-features)
7. [Database Schema](#database-schema)
8. [API Endpoints](#api-endpoints)
9. [Deployment](#deployment)

---

## Project Overview

### Purpose

The system aims to revolutionize public health by enabling early detection of disease outbreaks through continuous monitoring of diverse data sources including hospital records, social media, environmental data, pharmacy trends, and workplace/school absence patterns.

### Key Objectives

- **Early Detection**: Identify disease outbreak signals before widespread health crises
- **Multi-Source Intelligence**: Aggregate data from hospitals, social media, environmental sensors, pharmacies, schools, and emergency services
- **Predictive Analytics**: Forecast disease spread and anticipate healthcare capacity needs
- **Intelligent Alerts**: Generate risk-based alerts for health officials and the public
- **Transparent AI**: Provide explainable AI decisions with complete audit trails

---

## Folder and File Structure

```
disease-surveillance-ai-agents/
├── README.md                           # Project overview
├── SETUP.txt                           # Comprehensive setup guide
├── PROJECT_DOCUMENTATION.md            # This file
│
├── backend/                            # Python FastAPI backend
│   ├── main.py                         # Application entry point
│   ├── requirements.txt                # Python dependencies
│   ├── streamlit_app.py                # Developer dashboard (Streamlit)
│   │
│   ├── agents/                         # AI agent orchestration
│   │   ├── __init__.py
│   │   ├── agent_definitions.py        # Agent instructions and prompts
│   │   ├── agent_manager.py            # Agent lifecycle management
│   │   ├── agent_strategies.py         # Agent routing strategies
│   │   └── langgraph_orchestrator.py   # LangGraph multi-agent orchestrator
│   │
│   ├── api/                            # REST API endpoints
│   │   ├── __init__.py
│   │   ├── app.py                      # FastAPI application setup
│   │   ├── api_server.py               # Uvicorn server startup
│   │   └── endpoints.py                # API route definitions
│   │
│   ├── config/                         # Configuration management
│   │   ├── __init__.py
│   │   └── settings.py                 # Settings, environment variables
│   │
│   ├── managers/                       # Business logic managers
│   │   ├── __init__.py
│   │   └── surveillance_manager.py     # Main orchestration manager
│   │
│   ├── models/                         # ML models
│   │   ├── __init__.py
│   │   └── anomaly_detector.py         # Anomaly detection model
│   │
│   ├── plugins/                        # Extensible plugins
│   │   ├── __init__.py
│   │   ├── data_collection_plugin.py   # Data gathering plugin
│   │   ├── anomaly_detection_plugin.py # Anomaly analysis plugin
│   │   ├── prediction_plugin.py        # Disease prediction plugin
│   │   ├── alert_plugin.py             # Alert generation plugin
│   │   ├── reporting_plugin.py         # Report generation plugin
│   │   └── logging_plugin.py           # Agent thinking logs plugin
│   │
│   ├── sql/                            # Database schemas & migrations
│   │   ├── create_surveillance_tables_postgresql.sql
│   │   ├── create_stored_procedures_postgresql.sql
│   │   └── sample_data.sql
│   │
│   └── utils/                          # Utility functions
│       ├── __init__.py
│       ├── data_processing.py          # Data transformation utilities
│       └── database_utils.py           # Database helper functions
│
├── frontend/                           # Next.js React frontend
│   ├── package.json                    # npm dependencies
│   ├── tsconfig.json                   # TypeScript configuration
│   ├── next.config.ts                  # Next.js configuration
│   ├── tailwind.config.js              # Tailwind CSS configuration
│   ├── postcss.config.mjs              # PostCSS configuration
│   ├── components.json                 # Shadcn UI components config
│   │
│   ├── app/                            # Next.js App Router
│   │   ├── globals.css                 # Global styles
│   │   ├── layout.tsx                  # Root layout component
│   │   ├── page.tsx                    # Home page (redirects to chat)
│   │   │
│   │   ├── dashboard/                  # Dashboard page
│   │   │   └── page.tsx                # Real-time metrics dashboard
│   │   │
│   │   ├── chat/                       # Chat interface
│   │   │   └── page.tsx                # Main AI chat page
│   │   │
│   │   ├── alerts/                     # Alerts management
│   │   │   └── page.tsx                # Alerts history & details
│   │   │
│   │   ├── anomalies/                  # Anomalies detection
│   │   │   └── page.tsx                # Anomalies analysis page
│   │   │
│   │   ├── predictions/                # Predictions display
│   │   │   └── page.tsx                # Disease spread predictions
│   │   │
│   │   ├── reports/                    # Reports management
│   │   │   └── page.tsx                # Report generation & viewing
│   │   │
│   │   ├── thinking-logs/              # AI reasoning transparency
│   │   │   └── page.tsx                # Agent thinking logs viewer
│   │   │   └── [sessionId]/route.ts    # Session-specific thinking logs
│   │   │
│   │   └── api/                        # Next.js API routes (proxy)
│   │       ├── alerts/route.ts
│   │       ├── anomalies/route.ts
│   │       ├── chat/route.ts
│   │       ├── data-sources/route.ts
│   │       ├── predictions/route.ts
│   │       ├── reports/route.ts
│   │       ├── surveillance/status/route.ts
│   │       └── thinking-logs/[sessionId]/route.ts
│   │
│   ├── components/                     # React components
│   │   ├── site-header.tsx             # Navigation header
│   │   ├── theme-provider.tsx          # Dark/light theme provider
│   │   └── ui/                         # Shadcn UI components
│   │       ├── badge.tsx
│   │       ├── button.tsx
│   │       ├── card.tsx
│   │       ├── input.tsx
│   │       ├── scroll-area.tsx
│   │       └── textarea.tsx
│   │
│   └── lib/                            # Frontend utilities
│       └── utils.ts                    # Helper functions

```

---

## Technology Stack

### Backend Technologies

#### Core Framework & API

- **FastAPI** (v0.122.0) - High-performance REST API framework
- **Uvicorn** (v0.38.0) - ASGI web server
- **Python 3.11+** - Programming language

#### AI & LLM Integration

- **OpenAI API** - LLM for natural language understanding and report generation
- **LangGraph** (v0.0.20) - Multi-agent orchestration framework (replaces Azure AI Agent Service)
- **LangChain** (v0.1.0+) - LLM framework and tools integration
- **Langchain-OpenAI** - OpenAI integration for LangChain

#### Data Processing & ML

- **Pandas** (v2.1.1) - Data manipulation and analysis
- **NumPy** (v1.24.0) - Numerical computing
- **Scikit-Learn** (v1.7.2) - Machine learning models
- **SciPy** (v1.11.0) - Scientific computing
- **PyTorch** (v2.0.0) - Deep learning framework

#### Database & ORM

- **Supabase** (v2.24.0) - PostgreSQL backend and real-time database
- **psycopg2-binary** (v2.9.9+) - PostgreSQL adapter for Python
- **Pydantic** (v2.12.5) - Data validation using Python type annotations

#### Visualization & Reporting

- **Plotly** (v5.13.0) - Interactive data visualization
- **Python-docx** (v0.8.11) - Word document generation
- **Markdown** (v3.5.1) - Markdown processing

#### Utilities

- **python-dotenv** (v1.1.1) - Environment variable management
- **Requests** (v2.31.0) - HTTP client library
- **aiohttp** (v3.9.0+) - Async HTTP client
- **DuckDuckGo-Search** (v4.0.0) - Web search integration
- **nest-asyncio** (v1.5.8+) - Async event loop utilities

#### Developer Tools

- **Streamlit** (v1.51.0) - Developer dashboard for monitoring and testing

### Frontend Technologies

#### Framework & Build

- **Next.js** (v15.3.1) - React framework with file-based routing
- **React** (v18.3.1) - UI library
- **TypeScript** (v5) - Type-safe JavaScript
- **Tailwind CSS** (v3.4.1) - Utility-first CSS framework

#### UI Components & Styling

- **Radix UI** - Unstyled accessible component library
  - React Avatar, Checkbox, Collapsible, Dialog, Dropdown Menu
  - Label, Navigation Menu, Scroll Area, Separator, Slider, Tabs
  - Toggle, Tooltip
- **Shadcn/ui** - High-quality React components built on Radix UI
- **Lucide React** (v0.503.0) - Icon library
- **Framer Motion** (v12.9.2) - Animation library

#### Data Visualization

- **Recharts** (v2.14.1) - React charting library
- **Chart.js** (v4.4.1) - JavaScript charting library
- **react-chartjs-2** (v5.2.0) - React wrapper for Chart.js
- **React-Simple-Maps** (v3.0.0) - Geospatial visualization

#### Utilities

- **Markdown Processing**
  - react-markdown - React markdown renderer
  - remark-gfm - GitHub flavored markdown plugin
- **react-code-blocks** - Code highlighting
- **react-tooltip** (v5.28.1) - Tooltip component
- **sonner** (v2.0.3) - Toast notifications
- **next-themes** (v0.4.6) - Theme management
- **clsx** (v2.1.1) & **tailwind-merge** (v3.2.0) - CSS utility merging
- **@tanstack/react-table** (v8.21.3) - Headless table component

### Infrastructure & Deployment

#### Originally Designed For (Azure)

- Azure AI Foundry Hub & Projects
- Azure OpenAI Service
- Azure SQL Database
- Azure Blob Storage
- Azure Bing Search API

#### Currently Using

- **Supabase** - PostgreSQL database with real-time capabilities
- **OpenAI Direct API** - LLM services
- **DuckDuckGo Search** - Web search functionality
- **Local/Cloud Storage** - Report storage

---

## System Architecture

### High-Level Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          Frontend (Next.js/React)                       │
│  Dashboard │ Chat │ Alerts │ Anomalies │ Predictions │ Reports │ Logs  │
└────────────────────────┬────────────────────────────────────────────────┘
                         │ REST API (Next.js Routes)
┌─────────────────────────┴────────────────────────────────────────────────┐
│                        Backend API (FastAPI)                             │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                    FastAPI Application                           │   │
│  │  • /api/chat - Chat interface                                    │   │
│  │  • /api/alerts - Alert management                               │   │
│  │  • /api/anomalies - Anomaly queries                             │   │
│  │  • /api/predictions - Disease predictions                       │   │
│  │  • /api/reports - Report management                             │   │
│  │  • /api/surveillance/status - System status                     │   │
│  │  • /api/thinking-logs - AI reasoning transparency               │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                         │                                                │
└─────────────────────────┼────────────────────────────────────────────────┘
                          │ Process Queries
┌─────────────────────────┴────────────────────────────────────────────────┐
│              Multi-Agent Orchestration (LangGraph)                       │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │          Surveillance Manager & Agent Orchestrator               │   │
│  │                                                                   │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ Agent 1: Data Collection Agent                          │   │   │
│  │  │ → Gathers from hospitals, social media, environment     │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                            ↓                                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ Agent 2: Anomaly Detection Agent                        │   │   │
│  │  │ → Identifies unusual patterns using ML models           │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                            ↓                                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ Agent 3: Prediction Agent                              │   │   │
│  │  │ → Forecasts disease spread (3-week horizon)            │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                            ↓                                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ Agent 4: Alert Agent                                   │   │   │
│  │  │ → Generates risk-based alerts                          │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                            ↓                                     │   │
│  │  ┌─────────────────────────────────────────────────────────┐   │   │
│  │  │ Agent 5: Reporting Agent                               │   │   │
│  │  │ → Creates comprehensive outbreak assessments           │   │   │
│  │  └─────────────────────────────────────────────────────────┘   │   │
│  │                                                                   │   │
│  │  + Assistant Agent: Handles general queries                      │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                         │                                                │
│  ┌──────────────────────┴──────────────────────────────────────────┐   │
│  │                   Plugins (Extensible)                          │   │
│  │  • Data Collection Plugin - Data source integration             │   │
│  │  • Anomaly Detection Plugin - ML anomaly scoring                │   │
│  │  • Prediction Plugin - Disease spread forecasting               │   │
│  │  • Alert Plugin - Alert generation & storage                    │   │
│  │  • Reporting Plugin - Report generation & export                │   │
│  │  • Logging Plugin - Agent thinking & decision logs              │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└────────────────────────┬──────────────────────────────────────────────────┘
                         │
┌────────────────────────┴──────────────────────────────────────────────────┐
│                    Data Layer (Supabase PostgreSQL)                       │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ Hospital Data │ Social Media Data │ Environmental Data │ Pharmacy│   │
│  │ School/Workplace │ Emergency Services │ Alerts │ Predictions    │   │
│  │ Reports │ Agent Thinking Logs │ Chat History                    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────────────┘
```

### Agent Architecture

#### Multi-Agent Workflow Strategies

**1. General Queries**

```
User Query: "What's the current disease surveillance status?"
     ↓
ASSISTANT_AGENT (Answer from current data)
     ↓
Response
```

**2. Anomaly Detection Queries**

```
User Query: "Are there any unusual health patterns?"
     ↓
DATA_COLLECTION_AGENT (Gather data)
     ↓
ANOMALY_DETECTION_AGENT (Analyze patterns)
     ↓
REPORTING_AGENT (Generate insights)
     ↓
Response with Anomalies
```

**3. Outbreak Prediction Queries**

```
User Query: "Predict disease spread for the next 3 weeks"
     ↓
DATA_COLLECTION_AGENT (Gather current data)
     ↓
ANOMALY_DETECTION_AGENT (Identify trends)
     ↓
PREDICTION_AGENT (Forecast spread)
     ↓
REPORTING_AGENT (Structure predictions)
     ↓
Response with Forecasts
```

**4. Comprehensive Surveillance**

```
User Query: "Full outbreak risk assessment"
     ↓
DATA_COLLECTION_AGENT (Gather from all sources)
     ↓
ANOMALY_DETECTION_AGENT (Find anomalies)
     ↓
PREDICTION_AGENT (Predict spread)
     ↓
ALERT_AGENT (Generate alerts)
     ↓
REPORTING_AGENT (Create report)
     ↓
Complete Assessment
```

### Agent Definitions

| Agent                       | Role                   | Responsibilities                                                                                 |
| --------------------------- | ---------------------- | ------------------------------------------------------------------------------------------------ |
| **DATA_COLLECTION_AGENT**   | Intelligence Gatherer  | Monitors hospitals, social media, environmental sensors, pharmacies, schools, emergency services |
| **ANOMALY_DETECTION_AGENT** | Pattern Analyst        | Identifies statistical anomalies using ML models and baseline learning                           |
| **PREDICTION_AGENT**        | Forecaster             | Predicts disease spread using epidemic models and geographic analysis                            |
| **ALERT_AGENT**             | Alert Coordinator      | Generates risk-based alerts for different audiences                                              |
| **REPORTING_AGENT**         | Analyst & Communicator | Creates comprehensive outbreak reports with recommendations                                      |
| **ASSISTANT_AGENT**         | General Responder      | Handles general queries and provides surveillance status                                         |

---

## Workflow and Data Flow

### Request Flow

```
1. USER INTERACTION
   └─> Frontend (Chat, Dashboard, etc.)

2. API LAYER
   └─> Next.js Routes → FastAPI Backend
       ├─> Receive user query
       └─> Convert to surveillance request

3. ROUTING
   └─> SurveillanceManager
       ├─> Analyze query intent
       ├─> Select appropriate agent workflow
       └─> Initialize session context

4. AGENT ORCHESTRATION (LangGraph)
   ├─> Create state graph
   ├─> Initialize agents with instructions
   ├─> Activate plugins
   └─> Execute workflow based on query type

5. AGENT EXECUTION
   ├─> Call agent functions
   ├─> Agent uses tools (plugins) to:
   │   ├─> Collect data
   │   ├─> Analyze anomalies
   │   ├─> Generate predictions
   │   ├─> Create alerts
   │   └─> Produce reports
   └─> Log thinking at each stage

6. DATA PERSISTENCE
   ├─> Store results in database
   ├─> Save agent reasoning logs
   ├─> Cache alerts and predictions
   └─> Generate reports

7. RESPONSE DELIVERY
   ├─> Format response
   ├─> Include AI reasoning transparency
   └─> Return to frontend

8. FRONTEND DISPLAY
   └─> Visualize results on appropriate page
```

### Plugin Architecture

Plugins provide extensible functionality:

```python
# Plugin Interface (Abstract)
class Plugin:
    def __init__(self, connection_string: str)
    def initialize(self)
    def execute(self, *args, **kwargs) -> dict
    def validate_result(self, result: dict) -> bool
```

#### Plugin Details

**Data Collection Plugin**

- Gathers data from multiple sources
- Normalizes data formats
- Performs quality checks
- Returns structured surveillance data

**Anomaly Detection Plugin**

- Statistical analysis (z-score, IQR)
- ML model inference (isolation forest, LSTM)
- Baseline learning and adaptation
- Confidence scoring

**Prediction Plugin**

- Epidemic modeling (SIR, SEIR models)
- Time series forecasting
- Geographic spread simulation
- Healthcare capacity projection

**Alert Plugin**

- Risk threshold evaluation
- Alert prioritization
- Notification routing
- Recipient targeting

**Reporting Plugin**

- Executive summary generation
- Data visualization
- PDF/DOCX document creation
- Historical trend analysis

**Logging Plugin**

- Agent thinking documentation
- Decision tree recording
- Tool usage tracking
- Performance metrics collection

---

## Database Schema

### Core Tables

#### 1. Hospital Surveillance Data

```sql
hospital_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ region
├─ facility_name
├─ symptom_type
├─ patient_count
├─ age_group
├─ severity_level
├─ diagnosis
└─ created_date
```

#### 2. Social Media Surveillance Data

```sql
social_media_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ region
├─ platform
├─ mention_count
├─ symptom_keywords
├─ sentiment_score
├─ language
├─ post_content
└─ created_date
```

#### 3. Environmental Surveillance Data

```sql
environmental_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ region
├─ air_quality_index
├─ water_quality_index
├─ temperature
├─ humidity
├─ pollution_level
├─ weather_conditions
└─ created_date
```

#### 4. Pharmacy Surveillance Data

```sql
pharmacy_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ region
├─ pharmacy_name
├─ medication_name
├─ medication_category
├─ prescription_count
├─ is_otc
└─ created_date
```

#### 5. School/Workplace Data

```sql
school_workplace_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ institution_type
├─ absence_rate
├─ sick_leave_count
├─ institution_name
└─ created_date
```

#### 6. Emergency Services Data

```sql
emergency_services_surveillance_data
├─ record_id (PK)
├─ timestamp
├─ location
├─ er_activity_level
├─ ambulance_dispatch_count
├─ facility_name
└─ created_date
```

#### 7. Alerts Table

```sql
alerts
├─ alert_id (PK)
├─ timestamp
├─ risk_level (HIGH/MEDIUM/LOW)
├─ disease_type
├─ location
├─ description
├─ recommended_actions
├─ status (ACTIVE/RESOLVED)
└─ created_date
```

#### 8. Predictions Table

```sql
predictions
├─ prediction_id (PK)
├─ timestamp
├─ disease_type
├─ location
├─ forecast_period
├─ predicted_cases
├─ confidence_score
├─ prediction_model
└─ created_date
```

#### 9. Reports Table

```sql
reports
├─ report_id (PK)
├─ timestamp
├─ report_type
├─ content
├─ generated_by_agent
├─ storage_path
├─ status
└─ created_date
```

#### 10. Agent Thinking Logs

```sql
agent_thinking_logs
├─ log_id (PK)
├─ session_id
├─ conversation_id
├─ agent_name
├─ thinking_stage
├─ thought_content
├─ thinking_stage_output
├─ agent_output
├─ timestamp
└─ thread_id
```

#### 11. Chat History

```sql
chat_history
├─ message_id (PK)
├─ session_id
├─ user_message
├─ agent_response
├─ timestamp
└─ created_date
```

---

## API Endpoints

### Chat Interface

```
POST /api/chat
├─ Request: { query: string, session_id?: string }
└─ Response: { response: string, thinking_logs: [], suggestions: [] }
```

### Alerts Management

```
GET /api/alerts
├─ Query params: { limit?, offset?, risk_level?, status? }
└─ Response: { alerts: Alert[], total: number }

POST /api/alerts
├─ Request: { alert_data: AlertPayload }
└─ Response: { alert_id: string, created_at: timestamp }

GET /api/alerts/{alertId}
└─ Response: { alert: Alert }
```

### Anomalies Detection

```
GET /api/anomalies
├─ Query params: { location?, time_range?, data_source? }
└─ Response: { anomalies: Anomaly[], total: number }

POST /api/anomalies/analyze
├─ Request: { data: [], analysis_type: string }
└─ Response: { anomalies_found: [], confidence: number }
```

### Predictions

```
GET /api/predictions
├─ Query params: { location?, disease_type?, horizon? }
└─ Response: { predictions: Prediction[], confidence_range: [min, max] }

POST /api/predictions/generate
├─ Request: { disease_type: string, location: string, weeks: number }
└─ Response: { prediction_id: string, forecast: {} }
```

### Reports

```
GET /api/reports
├─ Query params: { limit?, offset?, report_type? }
└─ Response: { reports: Report[], total: number }

POST /api/reports/generate
├─ Request: { report_type: string, data_scope: {} }
└─ Response: { report_id: string, url: string }

GET /api/reports/{reportId}
└─ Response: { report: Report, content: string }
```

### Data Sources

```
GET /api/data-sources
└─ Response: { sources: { hospital, social_media, environmental, ... } }

GET /api/data-sources/{source}
├─ Query params: { location?, time_range? }
└─ Response: { data: [], metadata: {} }
```

### Surveillance Status

```
GET /api/surveillance/status
└─ Response: {
    system_health: {},
    active_alerts: number,
    last_update: timestamp,
    monitored_regions: [],
    data_sources_active: []
}
```

### Thinking Logs

```
GET /api/thinking-logs/{sessionId}
└─ Response: { logs: AgentThinkingLog[], session_metadata: {} }
```

---

## Key Features

### 🔍 Multi-Source Intelligence Gathering

**Data Sources Monitored:**

1. **Hospital Data** - Patient visit patterns, symptom types, severity levels
2. **Social Media** - Health-related discussions, symptom mentions, sentiment
3. **Environmental Data** - Air quality, water quality, temperature, weather
4. **Pharmacy Data** - Prescription trends, OTC medication sales
5. **School & Workplace** - Absence rates, sick leave patterns
6. **Emergency Services** - ER activity, ambulance dispatch patterns

**Integration Method:**

- Real-time API connections
- Scheduled data collection (hourly/daily)
- Event-driven updates
- Data normalization pipeline

### 🤖 Advanced ML Anomaly Detection

**Techniques:**

- Statistical methods (Z-score, IQR, Isolation Forest)
- Time series analysis
- Baseline learning with seasonal adjustment
- Deep learning models (LSTM for temporal patterns)
- Multivariate anomaly detection

**Outputs:**

- Anomaly scores (0-1)
- Confidence levels
- Contributing factors
- Historical trend comparison

### 📊 Predictive Disease Modeling

**Models:**

- SIR/SEIR epidemiological models
- ARIMA time series forecasting
- Geographic spread simulation
- Healthcare capacity projection

**Predictions Include:**

- Case forecasts (3-week horizon)
- Geographic spread patterns
- Severity distribution
- Resource requirements
- Peak timing estimates

### ⚠️ Intelligent Alert System

**Alert Types:**

- **HIGH RISK** - Threshold > 0.8
- **MEDIUM RISK** - Threshold 0.5-0.8
- **LOW RISK** - Threshold < 0.5

**Alert Features:**

- Automatic prioritization
- Audience targeting (public, officials, healthcare)
- Actionable recommendations
- Real-time notification delivery
- Alert history tracking

### 📈 Interactive Dashboards

**Dashboard Capabilities:**

- Real-time disease surveillance maps
- Anomaly trend visualization
- Prediction timeline charts
- Alert status overview
- Regional risk heatmaps
- Data source health monitoring

### 🔬 Transparent AI Reasoning

**Transparency Features:**

- Complete agent thinking logs
- Decision tree visualization
- Source citation and data provenance
- Tool usage tracking
- Confidence scores on all outputs
- Audit trail for compliance

---

## Deployment

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL/Supabase
- OpenAI API key
- 4GB RAM minimum

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py --test-connection
python main.py --test-agents
```

### Frontend Setup

```bash
cd frontend
npm install
npm run build
npm start
```

### Environment Configuration

```bash
# .env file
OPENAI_API_KEY=sk-...
OPENAI_MODEL=gpt-4-turbo-preview
DB_CONNECTION_STRING=postgresql://...
SUPABASE_URL=https://...
SUPABASE_ANON_KEY=...
SUPABASE_SERVICE_KEY=...
API_HOST=0.0.0.0
API_PORT=8000
```

### Running the Application

```bash
# Terminal 1 - Backend API
cd backend
python main.py

# Terminal 2 - Frontend Dev Server
cd frontend
npm run dev

# Access at http://localhost:3000
```

---

## System Configuration

### Performance Settings

```python
# Agent Configuration
AGENT_TIMEOUT = 300  # seconds
MAX_RETRIES = 3

# Data Collection
DATA_COLLECTION_INTERVAL = 3600  # 1 hour
ANOMALY_DETECTION_THRESHOLD = 0.75

# Prediction
PREDICTION_HORIZON_WEEKS = 3

# Alert Thresholds
ALERT_HIGH_RISK_THRESHOLD = 0.8
ALERT_MEDIUM_RISK_THRESHOLD = 0.5
ALERT_LOW_RISK_THRESHOLD = 0.3
```

### Monitoring & Logging

- **Log Level**: INFO (configurable)
- **Log Format**: Timestamp, Module, Level, Message
- **Log Output**: Console + File (`surveillance_api.log`)
- **Agent Logs**: Stored in database with session tracking

---

## Migration Notes

### From Azure to Open-Source Stack

The system was originally designed for Azure but has been migrated to use:

- **LangGraph** instead of Azure AI Agent Service
- **OpenAI API** instead of Azure OpenAI
- **Supabase/PostgreSQL** instead of Azure SQL Database
- **DuckDuckGo Search** instead of Azure Bing Search
- Local/Supabase storage instead of Azure Blob Storage

This migration maintains full functionality while reducing infrastructure dependencies.

---

## Security Considerations

1. **API Authentication** - Implement JWT tokens for API endpoints
2. **Database Encryption** - Use SSL/TLS for database connections
3. **Environment Secrets** - Store sensitive keys in .env or vault
4. **Rate Limiting** - Implement request throttling to prevent abuse
5. **Data Privacy** - Ensure HIPAA compliance for health data
6. **Audit Logging** - Track all data access and modifications

---

## Future Enhancements

1. **Real-time Data Streaming** - WebSocket integration for live updates
2. **Advanced Visualizations** - 3D maps, network graphs
3. **Mobile App** - Native iOS/Android application
4. **Federated Learning** - Distributed model training across regions
5. **Multi-language Support** - Global deployment capability
6. **Enhanced Explainability** - More detailed reasoning transparency
7. **Integration Marketplace** - Plugin ecosystem for third-party tools
8. **Automated Testing** - Comprehensive test suite and CI/CD

---

## Conclusion

The Disease Surveillance AI Agent System represents a comprehensive approach to proactive disease outbreak detection. By combining advanced AI agents, machine learning models, and real-time data from multiple sources, it transforms healthcare from reactive to predictive. The modular architecture allows for easy extension and customization, while the transparent AI reasoning ensures trust and compliance in critical health applications.
