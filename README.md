# PrepWise - AI Interview Practice Platform (Simplified)

A minimal viable product for AI-powered interview practice using Streamlit frontend and FastAPI backend with specialized agents.

## Features

- **Simple Chat Interface**: Clean, minimal interface for interview practice
- **AI-Powered Questions**: Uses specialized agents for behavioral and technical questions
- **Real-time Feedback**: Get responses from AI interviewer agents
- **Position-Specific Practice**: Choose from different job positions
- **Interviewer Personalities**: Select different interviewer styles

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Ollama running locally on port 11434 with llama3.2 model

### Start Ollama (Required)

```bash
# Install Ollama if you haven't already
# Then pull the required model
ollama pull llama3.2

# Start Ollama server
ollama serve
```

### Start the Application

```bash
# Clone and navigate to the project
cd prepwise

# Start all services
docker-compose up

# Or start services individually
docker-compose up backend-service
docker-compose up frontend-service
```

### Access the Application

- **Frontend**: http://localhost:8501
- **Backend API**: http://localhost:8002
- **Transcription Service**: http://localhost:9000

## Testing

Run the integration test to verify everything is working:

```bash
python test_integration.py
```

## Architecture

### Backend Service (`backend-service`)
- **FastAPI** application running on port 8002
- **Single `/chat` endpoint** that routes to specialized agents
- **Agent Orchestrator** that selects appropriate tools based on user input
- **Specialized Agents**:
  - Introduction Assistant
  - Behavioral Question Assistant  
  - Technical Question Assistant

### Frontend Service (`frontend-service`)
- **Streamlit** application running on port 8501
- **Simplified UI** with chat interface
- **Profile Management** for user preferences
- **Real-time Communication** with backend via REST API

### Shared Models (`shared/`)
- **Pydantic Models** for data validation
- **Enums** for interview positions, question types, and personalities
- **Shared between frontend and backend**

## Usage

1. **Configure Settings**: Set your target position, interviewer style, and question preferences in the sidebar
2. **Save Profile**: Enter your name and experience level
3. **Start Interview**: Click "Start Interview" to begin
4. **Chat**: Respond to AI questions and ask for new questions as needed
5. **End Interview**: Click "End Interview" when finished

## API Endpoints

### Backend Service

- `GET /health` - Health check
- `GET /` - Service information
- `POST /chat` - Send chat message to AI agents

### Example Chat Request

```json
{
  "query": "Hello, I want to start an interview for a software engineer position."
}
```

### Example Chat Response

```json
{
  "status": "success",
  "service": "backend",
  "timestamp": "2024-01-01T12:00:00",
  "query": "Hello, I want to start an interview...",
  "response": "Hello! I'm excited to conduct your software engineer interview..."
}
```

## Development

### Project Structure

```
prepwise/
├── services/
│   ├── backend-service/
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   └── agents/
│   │   │       ├── orchestrator.py
│   │   │       └── specialized_agents.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   └── frontend-service/
│       ├── app/
│       │   └── streamlit_app.py
│       ├── Dockerfile
│       └── requirements.txt
├── shared/
│   └── __init__.py
├── docker-compose.yml
└── test_integration.py
```

### Adding New Features

1. **New Agent Types**: Add tools to `specialized_agents.py`
2. **New UI Components**: Modify `streamlit_app.py`
3. **New Data Models**: Update `shared/__init__.py`
4. **New API Endpoints**: Add routes to `main.py`

## Troubleshooting

### Backend Issues
- Ensure Ollama is running: `ollama serve`
- Check Ollama model: `ollama list` (should include llama3.2)
- Verify backend logs: `docker-compose logs backend-service`

### Frontend Issues
- Check frontend logs: `docker-compose logs frontend-service`
- Verify backend connectivity: Visit http://localhost:8002/health

### Common Issues
- **"Backend service not available"**: Start backend service first
- **"Failed to send chat message"**: Check Ollama connection
- **Import errors**: Ensure shared models are properly copied to containers

## Next Steps

This is a minimal viable product. Future enhancements could include:

- Voice input/output capabilities
- Resume parsing and analysis
- Advanced scoring and feedback
- Interview session persistence
- Multiple interview formats
- Integration with job boards
- Analytics and progress tracking