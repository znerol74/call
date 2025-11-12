# CAL - AI Phone Agent Assistant System

A multi-tenant, GDPR-compliant AI phone agent system with real-time voice interaction capabilities.

## Features

- 🤖 **Multi-Tenant AI Agents**: Create and manage multiple AI phone agents
- 📞 **Twilio Integration**: Inbound and outbound call support
- 🎤 **Voice AI**: ElevenLabs Conversational AI (150ms v2) with streaming
- 🧠 **LLM Integration**: Azure OpenAI with streaming responses
- 🔐 **Authentication**: JWT-based secure authentication
- 🛡️ **GDPR Compliant**: Full data protection compliance with German focus
- 🧰 **Custom Tools**: Define custom tools for agents (API calls, transfers, etc.)
- 📊 **Analytics**: Call logs, transcripts, and statistics
- 🧪 **Live Testing**: Test agents directly in the browser

## Tech Stack

- **Frontend**: React + TypeScript + TailwindCSS
- **Backend**: Python FastAPI + WebSocket
- **Database**: PostgreSQL
- **Cache**: Redis
- **Voice**: ElevenLabs + Twilio
- **LLM**: Azure OpenAI
- **Deployment**: Docker Compose

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Azure OpenAI account
- ElevenLabs API account
- Twilio account

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cal
```

2. Copy environment variables:
```bash
cp .env.example .env
```

3. Edit `.env` and add your API keys and credentials

4. Start the services:
```bash
docker-compose up -d
```

5. Access the application:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### First Time Setup

1. Register a new account at http://localhost:3000/register
2. Accept GDPR consent and terms
3. Create your first AI agent
4. Configure a phone number
5. Test the agent in the browser

## Project Structure

```
cal/
├── backend/
│   ├── app/
│   │   ├── api/          # API routes
│   │   ├── models/       # Database models
│   │   ├── services/     # Business logic
│   │   ├── core/         # Configuration
│   │   └── utils/        # Utilities
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/   # React components
│   │   ├── pages/        # Page components
│   │   ├── services/     # API services
│   │   └── hooks/        # Custom hooks
│   ├── Dockerfile
│   └── package.json
├── docker-compose.yml
└── .env.example
```

## GDPR Compliance

This system is built with GDPR compliance in mind:

- ✅ Right to Access (data export)
- ✅ Right to Erasure (account deletion)
- ✅ Right to Rectification (data editing)
- ✅ Data Minimization
- ✅ Consent Management
- ✅ Audit Logging
- ✅ Data Retention Policies
- ✅ Encryption at rest and in transit

## Development

### Backend Development

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development

```bash
cd frontend
npm install
npm start
```

## API Documentation

Once the backend is running, visit http://localhost:8000/docs for interactive API documentation.

## License

[Your License Here]

## Support

For issues and questions, please open an issue on GitHub.
