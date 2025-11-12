# CAL - AI Phone Agent System - Setup Guide

Complete setup guide for deploying the AI Phone Agent Assistant System.

## Prerequisites

- Docker and Docker Compose installed
- Azure OpenAI account with GPT-4 Turbo deployment
- ElevenLabs API account
- Twilio account with phone number
- Domain name (for production)

## Step 1: Clone and Configure

```bash
git clone <your-repo-url>
cd cal
```

## Step 2: Environment Configuration

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and fill in all required values:

### Database Configuration
```
POSTGRES_USER=caluser
POSTGRES_PASSWORD=<generate-secure-password>
POSTGRES_DB=caldb
```

### JWT Secrets
Generate secure random strings (at least 32 characters each):
```bash
# On Linux/Mac:
openssl rand -hex 32

# On Windows PowerShell:
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

```
JWT_SECRET_KEY=<your-generated-secret>
JWT_REFRESH_SECRET_KEY=<your-generated-refresh-secret>
```

### Azure OpenAI
1. Go to Azure Portal → Azure OpenAI resource
2. Get your endpoint and key
3. Deploy GPT-4 Turbo model
4. Add to .env:

```
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_KEY=<your-key>
AZURE_OPENAI_DEPLOYMENT=gpt-4-turbo
```

### ElevenLabs
1. Go to https://elevenlabs.io/
2. Get your API key from settings
3. Add to .env:

```
ELEVENLABS_API_KEY=<your-elevenlabs-key>
```

### Twilio
1. Go to https://www.twilio.com/console
2. Get Account SID and Auth Token
3. Buy a phone number
4. Add to .env:

```
TWILIO_ACCOUNT_SID=<your-account-sid>
TWILIO_AUTH_TOKEN=<your-auth-token>
TWILIO_PHONE_NUMBER=+1234567890
```

## Step 3: Build and Start Services

```bash
docker-compose up -d --build
```

This will start:
- PostgreSQL database (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Background worker
- Frontend (port 3000)

## Step 4: Verify Installation

Check all services are running:
```bash
docker-compose ps
```

Expected output: All services should show "Up"

Test the API:
```bash
curl http://localhost:8000/health
```

Expected: `{"status":"healthy"}`

Test the frontend:
Open browser to http://localhost:3000

## Step 5: Configure Twilio Webhooks

1. Go to Twilio Console → Phone Numbers
2. Select your phone number
3. Configure webhooks:

**Voice & Fax → A Call Comes In:**
- URL: `https://your-domain.com/api/v1/twilio/incoming-call`
- HTTP Method: POST

**Voice & Fax → Call Status Changes:**
- URL: `https://your-domain.com/api/v1/twilio/call-status`
- HTTP Method: POST

Note: For local development, use ngrok:
```bash
ngrok http 8000
```
Then use the ngrok URL for webhooks.

## Step 6: Create Your First User

1. Go to http://localhost:3000/register
2. Fill in the registration form
3. Accept all GDPR consents
4. Click "Register"

## Step 7: Create Your First Agent

1. Login to the dashboard
2. Go to "Agents" → "Create New Agent"
3. Fill in:
   - Name: e.g., "Kundenservice Agent"
   - System Prompt: e.g., "Du bist ein freundlicher Kundenservice-Agent. Beantworte Fragen höflich auf Deutsch."
   - Greeting: e.g., "Guten Tag! Wie kann ich Ihnen helfen?"
   - Voice: Select from ElevenLabs voices
   - Language: de (German)
   - Tools: Configure any tools (transfer, API calls, etc.)
4. Save the agent

## Step 8: Assign Phone Number

1. Go to "Phone Numbers"
2. Add your Twilio phone number
3. Assign it to your agent
4. Save

## Step 9: Test the System

### Option A: Test in Browser
1. Go to your agent's detail page
2. Click "Test Agent"
3. Type messages to test the conversation flow

### Option B: Test with Real Phone Call
1. Call your Twilio phone number
2. The agent should answer with the greeting
3. Speak naturally - the agent will respond

## Troubleshooting

### Services won't start
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Restart services
docker-compose restart
```

### Database connection errors
```bash
# Ensure PostgreSQL is running
docker-compose ps postgres

# Check database logs
docker-compose logs postgres
```

### Twilio webhook errors
- Ensure webhooks are configured correctly
- Check backend is accessible from internet (use ngrok for local dev)
- Check backend logs: `docker-compose logs backend`

### ElevenLabs API errors
- Verify API key is correct
- Check you have credits in your ElevenLabs account
- Try a different voice ID

### Azure OpenAI errors
- Verify endpoint and key are correct
- Ensure deployment name matches
- Check you haven't exceeded quota

## Production Deployment

### Security Checklist
- [ ] Change all default passwords
- [ ] Use strong JWT secrets
- [ ] Enable HTTPS with SSL certificate
- [ ] Set up firewall rules
- [ ] Enable database backups
- [ ] Review CORS settings
- [ ] Set up monitoring and logging

### Recommended Infrastructure
- Docker Compose or Kubernetes
- Reverse proxy (Nginx) with SSL
- Managed PostgreSQL database
- Redis cluster for high availability
- Load balancer for multiple backend instances

### Environment Variables for Production
```
DEBUG=False
FRONTEND_URL=https://your-domain.com
DATA_RETENTION_DAYS=90
ANONYMIZATION_AFTER_DAYS=180
```

## GDPR Compliance

### User Rights Implementation
- ✅ Right to Access: `/settings` → "Export My Data"
- ✅ Right to Erasure: `/settings` → "Delete Account"
- ✅ Right to Rectification: Edit profile and data
- ✅ Consent Management: Registration requires explicit consent
- ✅ Data Retention: Automatic cleanup after 90 days
- ✅ Audit Logging: All data access is logged

### Privacy Policy
Update the privacy policy in:
- Backend: `app/api/v1/gdpr.py` → `get_privacy_policy()`
- Frontend: `src/pages/PrivacyPolicy.tsx`

Add your contact email and legal information.

## Monitoring

### Check System Health
```bash
# API health
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres psql -U caluser -d caldb -c "SELECT version();"

# Redis connection
docker-compose exec redis redis-cli ping
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f worker
```

### Metrics
The worker logs retention and anonymization activities:
```bash
docker-compose logs worker | grep "Cleaned up"
docker-compose logs worker | grep "Anonymized"
```

## Backup and Recovery

### Database Backup
```bash
docker-compose exec postgres pg_dump -U caluser caldb > backup.sql
```

### Restore Database
```bash
docker-compose exec -T postgres psql -U caluser caldb < backup.sql
```

## Support

For issues:
1. Check logs: `docker-compose logs`
2. Review this documentation
3. Check API docs: http://localhost:8000/docs
4. Open an issue on GitHub

## Updates

To update the system:
```bash
git pull
docker-compose down
docker-compose up -d --build
```

## Next Steps

1. Customize agent system prompts for your use case
2. Add custom tools for your business logic
3. Configure multiple agents for different purposes
4. Set up monitoring and alerting
5. Train your team on using the system
6. Test thoroughly before production deployment

---

For more information, see the main README.md file.
