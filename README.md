# Disease Surveillance AI Agent System

## Overview

The Disease Surveillance AI Agent System is a revolutionary proactive disease outbreak detection platform that transforms healthcare from reactive to predictive. Built on Azure AI Agent Service and inspired by PandemicLLM's predictive capabilities, this multi-agent system continuously monitors multiple data streams to identify disease outbreak signals before they become widespread health crises.

Instead of waiting for doctors and hospitals to manually report cases, our AI agents actively hunt for the earliest possible signs of health threats by analyzing:

- *Patient Data* - Hospital visit patterns and treatment trends
- *Social Media* - Health-related discussions and symptom mentions
- *Environmental Data* - Air quality, water quality, and weather patterns
- *Pharmacy Data* - Prescription trends and over-the-counter medication sales
- *School & Workplace* - Absence rates and sick leave patterns
- *Emergency Services* - ER activity and ambulance dispatch patterns

## System Architecture

![Alt text](./data/public/architecture.jpg)


## Core Logic: LangGraph Multi-Agent Orchestration

The system leverages *LangGraph* - a state-based workflow orchestration framework - to coordinate multiple specialized AI agents. LangGraph provides robust agent coordination with conditional routing, state management, and transparent execution flow.

### Agent Architecture

The system implements *6 specialized agents*, each with distinct responsibilities:

#### 1. *DATA_COLLECTION_AGENT*
- *Purpose*: Multi-source intelligence gathering
- *Data Sources*:
  - Hospital patient visit patterns and treatment trends
  - Social media health discussions and symptom mentions  
  - Environmental data (air quality, water quality, weather)
  - Pharmacy prescription trends and OTC medication sales
  - School and workplace absence rates
  - Emergency room activity and ambulance dispatch patterns
- *Plugins*: DataCollectionPlugin
- *Output*: Aggregated surveillance data with quality metrics

#### 2. *ANOMALY_DETECTION_AGENT*
- *Purpose*: Statistical pattern recognition and ML-based anomaly detection
- *Capabilities*:
  - Identifies unusual patterns across multiple data streams
  - Applies machine learning models for early outbreak signals
  - Performs multi-source correlation analysis
  - Classifies anomalies by severity (Critical/High/Medium/Low)
- *Plugins*: AnomalyDetectionPlugin
- *Output*: Detected anomalies with confidence scores and geographic clustering

#### 3. *PREDICTION_AGENT*
- *Purpose*: Disease outbreak forecasting using PandemicLLM-inspired models
- *Capabilities*:
  - Epidemic forecasting (1-week, 2-week, 3-week predictions)
  - Geographic spread prediction with population density analysis
  - Healthcare capacity impact assessment
  - Resource allocation optimization
  - Scenario modeling (best/likely/worst case)
- *Plugins*: PredictionPlugin
- *Tools*: Bing Search for real-time epidemiological data
- *Output*: Outbreak predictions with confidence intervals

#### 4. *ALERT_AGENT*
- *Purpose*: Risk-based alert generation and communication
- *Target Audiences*:
  - Public health officials and hospital administrators
  - Healthcare providers (doctors, nurses, ER staff)
  - General public, schools, and workplaces
  - Media and press communications
- *Capabilities*:
  - Risk-based alert prioritization
  - Audience-specific message crafting
  - Multi-channel dissemination planning
- *Plugins*: AlertPlugin
- *Output*: Targeted alerts with actionable recommendations

#### 5. *REPORTING_AGENT*
- *Purpose*: Comprehensive outbreak assessment report generation
- *Capabilities*:
  - Consolidates data from all agents
  - Creates executive-level surveillance reports
  - Generates visualization-ready data
  - Provides actionable intervention recommendations
  - Archives reports with audit trail
- *Plugins*: ReportingPlugin
- *Output*: Complete surveillance report with data visualizations

#### 6. *ASSISTANT_AGENT*
- *Purpose*: General-purpose conversational interface
- *Capabilities*:
  - Handles simple queries without full workflow execution
  - Provides system information and guidance
  - Routes complex queries to specialized workflow
- *Plugins*: None (lightweight assistant)
- *Output*: Direct conversational responses

### LangGraph Workflow Execution

The system uses *conditional state graph routing* to dynamically determine agent execution paths based on query complexity:

#### Execution Flow Examples

*1. Simple Query*

Query: "What is this system about?"
Flow: Entry → Assistant Agent → END
Time: ~2-3 seconds


*2. Anomaly Detection*

Query: "Are there unusual health patterns in Mumbai?"
Flow: Entry → Data Collection → Anomaly Detection → Reporting → END
Time: ~15-20 seconds
Agents: 3


*3. Outbreak Prediction*

Query: "Predict influenza spread for next 3 weeks"
Flow: Entry → Data Collection → Anomaly Detection → Prediction → Reporting → END
Time: ~25-30 seconds
Agents: 4


*4. Full Surveillance Analysis*

Query: "Full outbreak risk assessment"
Flow: Entry → Data Collection → Anomaly Detection → Prediction → Alert → Reporting → END
Time: ~35-45 seconds
Agents: 5


### State Management

LangGraph maintains a comprehensive state object throughout workflow execution:

python
{
  "messages": [],              # Conversation history
  "session_id": "uuid",        # Session identifier
  "conversation_id": "uuid",   # Conversation identifier
  "current_agent": "string",   # Active agent name
  "user_query": "string",      # Original user query
  "data_collected": {},        # Data collection results
  "anomalies_found": [],       # Detected anomalies
  "predictions_made": {},      # Outbreak predictions
  "alerts_generated": [],      # Generated alerts
  "final_report": "string",    # Complete report
  "agents_executed": [],       # Execution trace
  "should_continue": boolean   # Workflow control
}


### Intelligent Routing Logic

The orchestrator uses query analysis to determine optimal execution path:

- *Simple keywords* ("what is", "hello", "help") → Assistant Agent
- *Prediction keywords* ("predict", "forecast") → Full prediction workflow
- *Alert requirements* → Include Alert Agent
- *Complex surveillance* → Complete multi-agent workflow

### Plugin Integration

Each agent is equipped with specialized plugins providing:

- *Database access* via database_utils.py
- *Data processing* via data_processing.py
- *Real-time search* via Bing Search API
- *Logging and audit* via logging_plugin.py
- *Report storage* via Azure Blob Storage

### Transparency & Explainability

Every agent documents its reasoning process:

- *Thinking stages* logged at each step
- *Complete audit trail* of all agent actions
- *Confidence scores* for predictions and anomalies
- *Data provenance* tracking for all sources
- *Decision explanations* for routing choices

## Key Features

### 🔍 Multi-Source Intelligence Gathering

- Real-time monitoring of healthcare facilities
- Social media sentiment analysis for health concerns
- Environmental and weather data correlation
- Pharmacy prescription trend analysis
- School and workplace absence tracking

### 🤖 Advanced ML Anomaly Detection

- Statistical pattern recognition across multiple data sources
- Machine learning models for early outbreak signals
- Integration with PandemicLLM's prediction capabilities
- Continuous baseline learning for normal patterns

### 📊 Predictive Disease Modeling

- Epidemic forecasting using advanced LLM models
- Geographic spread prediction with population density analysis
- Healthcare capacity impact assessment
- Resource allocation optimization

### ⚠ Intelligent Alert System

- Risk-based alert prioritization
- Targeted communications for different audiences
- Real-time notification delivery
- Actionable public health recommendations

### 📈 Interactive Dashboards

- Real-time disease surveillance maps
- Anomaly trend visualization
- Predictive model outputs
- Alert history and tracking

### 🔬 Transparent AI Reasoning

- Complete visibility into detection logic
- Source citation and data provenance
- Audit trail for all predictions
- Explainable AI decisions

## Business Impact

This system addresses critical public health challenges by:

- *Early Detection* - Identify outbreaks days or weeks before traditional reporting
- *Predictive Intelligence* - Forecast disease spread to enable proactive response
- *Resource Optimization* - Deploy medical resources efficiently based on predictions
- *Public Safety* - Provide early warnings to communities at risk
- *Healthcare Capacity* - Prevent system overload through advance planning
- *Data-Driven Policy* - Support evidence-based public health decisions

## Quick Start

### Prerequisites

- *Python 3.11+* - Backend runtime
- *Node.js 18+* - Frontend runtime
- *PostgreSQL/Supabase* - Database for surveillance data
- *Azure OpenAI* or *OpenAI API* - LLM for agent intelligence
- *Azure Blob Storage* (optional) - Report storage
- *Bing Search API* (optional) - Real-time data grounding

### Installation

bash
# Clone repository
git clone https://github.com/AaryaKhatate/disease-surveillance-ai-agents.git
cd disease-surveillance-ai-agents

# Backend setup
cd backend
python -m venv .venv
.venv\Scripts\activate  # On Windows
# or
source .venv/bin/activate  # On Linux/Mac

pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
# or
bun install  # If using Bun


### Environment Setup

Create backend/.env file (copy from .env.example):

env
# OpenAI Configuration (Required)
OPENAI_API_KEY=your_openai_api_key
OPENAI_MODEL=gpt-4-turbo-preview

# Database Configuration (Required)
DB_CONNECTION_STRING=postgresql://user:password@host:port/database
# For Supabase:
# DB_CONNECTION_STRING=postgresql://postgres:[password]@db.[project].supabase.co:5432/postgres

# Azure Storage (Optional - for report storage)
AZURE_STORAGE_CONNECTION_STRING=your_storage_connection_string

# Bing Search API (Optional - for real-time grounding)
BING_SEARCH_API_KEY=your_bing_search_api_key
BING_CONNECTION_NAME=your_bing_connection_name

# Azure AI Agent Service (Optional - if using Azure)
AZURE_AI_AGENT_PROJECT_CONNECTION_STRING=your_connection_string
AZURE_AI_AGENT_MODEL_DEPLOYMENT_NAME=your_model_deployment

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
LOG_LEVEL=INFO


Create frontend/.env.local file:

env
NEXT_PUBLIC_API_URL=http://localhost:8000


### Database Setup

Initialize the PostgreSQL database with surveillance tables:

bash
cd backend

# Run database setup scripts
psql -h your_host -U your_user -d your_database -f sql/create_surveillance_tables_postgresql.sql
psql -h your_host -U your_user -d your_database -f sql/create_stored_procedures_postgresql.sql

# (Optional) Load sample data for testing
psql -h your_host -U your_user -d your_database -f sql/insert_mock_data.sql


### Running the Application

#### Option 1: Using the provided script

bash
# From project root
cd backend
uv run uvicorn main:app --reload


#### Option 2: Manual startup

bash
# Terminal 1: Start backend API
cd backend
.venv\Scripts\activate  # Windows
# or
source .venv/bin/activate  # Linux/Mac

python -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --reload

# Terminal 2: Start frontend (in another terminal)
cd frontend
npm run dev
# or
bun dev


Access the application:
- *Frontend*: http://localhost:3000
- *API Documentation*: http://localhost:8000/docs
- *API Health Check*: http://localhost:8000/health

### Developer Mode

Run the Streamlit developer dashboard for testing and monitoring:

bash
cd backend
.venv\Scripts\activate  # Activate virtual environment
streamlit run streamlit_app.py


Access Streamlit dashboard at http://localhost:8501

### Testing the Installation

Test database connection:
bash
cd backend
python main.py --test-connection


Test plugin initialization:
bash
cd backend
python main.py --test-plugins


Test LangGraph orchestrator:
bash
cd backend
python agents/langgraph_orchestrator.py


### Common Issues & Solutions

*Issue*: Import errors or missing dependencies
bash
pip install -r requirements.txt --upgrade


*Issue*: Database connection fails
- Verify DB_CONNECTION_STRING in .env
- Check PostgreSQL/Supabase is running
- Test connection with psql command

*Issue*: Frontend can't connect to backend
- Ensure backend is running on port 8000
- Verify NEXT_PUBLIC_API_URL in frontend .env.local
- Check CORS settings in backend/api/app.py

*Issue*: OpenAI API errors
- Verify OPENAI_API_KEY is correct
- Check API quota and billing
- Ensure OPENAI_MODEL is accessible (gpt-4, gpt-4-turbo-preview, etc.)

## Tech Stack

### Backend Technologies

#### Core Framework
- *FastAPI* (0.122.0) - High-performance async REST API framework
- *Uvicorn* (0.38.0) - ASGI server for production deployment
- *Pydantic* (2.12.5) - Data validation and settings management

#### AI & Agent Orchestration
- *LangGraph* (≥0.0.20) - State-based multi-agent workflow orchestration
- *LangChain* (≥0.1.0) - LLM application framework
- *LangChain-OpenAI* (≥0.0.5) - OpenAI integration for LangChain
- *OpenAI* (≥1.10.0) - GPT-4 and embedding models
- *Semantic Kernel* - Azure AI Agent Service integration (optional)

#### Data Processing & ML
- *Pandas* (≥2.1.1) - Data manipulation and analysis
- *NumPy* (≥1.24.0) - Numerical computing
- *SciPy* (≥1.11.0) - Scientific computing
- *Scikit-learn* (≥1.7.2) - Machine learning for anomaly detection
- *PyTorch* (≥2.0.0) - Deep learning for prediction models

#### Database & Storage
- *PostgreSQL* - Primary database via psycopg2-binary (≥2.9.9)
- *Supabase* (2.24.0) - PostgreSQL with real-time capabilities
- *Azure Blob Storage* - Report archival and document storage

#### Visualization & Reporting
- *Plotly* (≥5.13.0) - Interactive data visualizations
- *Streamlit* (1.51.0) - Developer dashboard and testing interface
- *Python-DOCX* (≥0.8.11) - Word document generation
- *Markdown* (≥3.5.1) - Markdown report formatting

#### Utilities
- *Python-dotenv* (1.1.1) - Environment variable management
- *aiohttp* (≥3.9.0) - Async HTTP client
- *Requests* (≥2.31.0) - HTTP library
- *DuckDuckGo-Search* (≥4.0.0) - Web search integration
- *nest-asyncio* (≥1.5.8) - Async compatibility

### Frontend Technologies

#### Core Framework
- *React* (18.3.1) - UI component framework
- *Next.js* (15.3.1) - Full-stack React framework with App Router
- *TypeScript* (5.x) - Type-safe JavaScript
- *Next-Themes* (0.4.6) - Dark/light theme support

#### UI Components & Styling
- *Tailwind CSS* (3.4.1) - Utility-first CSS framework
- *Radix UI* - Accessible component primitives:
  - Dialog, Dropdown Menu, Tabs, Tooltip, Slider, etc.
- *Shadcn/ui* - Re-usable component collection
- *Lucide React* (0.503.0) - Icon library
- *Class Variance Authority* (0.7.1) - Component variant management
- *Tailwind Merge* (3.2.0) - Tailwind class merging
- *Framer Motion* (12.9.2) - Animation library

#### Data Visualization
- *Recharts* (2.14.1) - Composable charting library
- *Chart.js* (4.4.1) + React-ChartJS-2 (5.2.0) - Chart components
- *React Simple Maps* (3.0.0) - SVG geographic visualizations
- *React Tooltip* (5.28.1) - Interactive tooltips

#### Content & Display
- *React Markdown* (10.1.0) - Markdown rendering
- *Remark GFM* (4.0.1) - GitHub Flavored Markdown
- *React Code Blocks* (0.1.6) - Syntax-highlighted code display
- *@tanstack/react-table* (8.21.3) - Table component
- *Sonner* (2.0.3) - Toast notifications

#### Development Tools
- *ESLint* (9.x) - Code linting
- *PostCSS* (8.x) - CSS processing
- *@tailwindcss/typography* (0.5.16) - Typography plugin

### Infrastructure & Deployment

- *PostgreSQL/Supabase* - Database hosting
- *Azure OpenAI* or *OpenAI API* - LLM hosting
- *Azure Blob Storage* - Object storage
- *Bing Search API* - Web search grounding
- *Docker* (optional) - Containerization
- *Azure App Service* (optional) - Deployment platform

## Project Structure


disease-surveillance-ai-agents/
├── backend/
│   ├── .env.example               # Environment variables template
│   ├── agents/                    # Agent definitions and strategies
│   │   ├── agent_definitions.py   # Specialized agent instructions
│   │   ├── agent_manager.py       # Agent creation and management
│   │   ├── agent_strategies.py    # Selection and termination logic
│   │   └── langgraph_orchestrator.py # LangGraph agent orchestration
│   ├── api/                       # API components
│   │   ├── app.py                 # FastAPI application setup
│   │   ├── endpoints.py           # API route definitions
│   │   └── api_server.py          # API server
│   ├── config/                    # Configuration
│   │   └── settings.py            # Environment settings
│   ├── managers/                  # System managers
│   │   └── surveillance_manager.py # Disease surveillance orchestration
│   ├── models/                    # ML models
│   │   └── anomaly_detector.py    # Anomaly detection models
│   ├── plugins/                   # Semantic Kernel plugins
│   │   ├── data_collection_plugin.py
│   │   ├── anomaly_detection_plugin.py
│   │   ├── prediction_plugin.py
│   │   ├── alert_plugin.py
│   │   ├── reporting_plugin.py
│   │   └── logging_plugin.py
│   ├── utils/                     # Utility functions
│   │   ├── database_utils.py
│   │   ├── data_processing.py
│   │   ├── load_data_to_supabase.py
│   │   ├── load_pandemic_data.py
│   │   ├── query_helpers.py
│   │   ├── simple_data_loader.py
│   │   ├── supabase_data_loader.py
│   │   └── transform_pandemic_data.py
│   ├── sql/                       # Database schemas and scripts
│   │   ├── create_stored_procedures_postgresql.sql
│   │   ├── create_surveillance_tables_postgresql.sql
│   │   ├── insert_mock_data.sql
│   │   ├── insert_pandemic_llm_data.sql
│   │   └── sample_data.sql
│   ├── main.py                    # Main application entry point
│   ├── streamlit_app.py           # Streamlit developer dashboard
│   └── requirements.txt           # Python dependencies
├── data/                          # Data and documentation assets
│   ├── public/                    # Public assets
│   │   └── architecture.png       # System architecture diagram
│   ├── src/                       # Data processing notebooks
│   │   ├── generate_prompt.ipynb
│   │   ├── generate_target.ipynb
│   │   ├── genomic_data_preprocess.ipynb
│   │   ├── genomic_prompt.ipynb
│   │   ├── raw_data.zip           # Raw dataset archive
│   │   ├── raw_data_preprocessing.ipynb
│   │   └── trend_descrption_with_ChatGPT.ipynb
│   └── readme.md                  # Data documentation
├── frontend/
│   ├── app/                       # Next.js app directory
│   │   ├── dashboard/             # Main surveillance dashboard
│   │   ├── chat/                  # Chat interface
│   │   ├── alerts/                # Alert management
│   │   ├── anomalies/             # Anomaly detection views
│   │   ├── predictions/           # Prediction visualizations
│   │   ├── reports/               # Report management
│   │   ├── thinking-logs/         # Agent thinking logs
│   │   ├── api/                   # API routes
│   │   ├── layout.tsx             # Root layout
│   │   ├── page.tsx               # Home page
│   │   └── globals.css            # Global styles
│   ├── components/                # React components
│   │   ├── ui/                    # UI components
│   │   ├── site-header.tsx        # Site header component
│   │   └── theme-provider.tsx    # Theme provider component
│   ├── lib/                       # Utility libraries
│   ├── next.config.ts             # Next.js configuration
│   ├── tailwind.config.js         # Tailwind CSS configuration
│   ├── postcss.config.mjs         # PostCSS configuration
│   ├── components.json            # shadcn/ui component configuration
│   ├── tsconfig.json              # TypeScript configuration
│   ├── package.json               # Node dependencies
│   └── bun.lock                   # Bun package lock file
├── .git/                          # Git repository
├── .gitignore                     # Git ignore rules
├── README.md                      # Project documentation
└── SETUP.txt                      # Setup instructions
