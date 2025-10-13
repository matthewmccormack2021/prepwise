# Backend Service

FastAPI backend service for the PrepWise AI interview practice platform.

## Features

- **FastAPI Framework**: Modern, fast web framework for building APIs
- **Agentic System**: AI-powered interview question generation and answer evaluation
- **Session Management**: Interview session tracking and analytics
- **RESTful API**: Clean API endpoints for frontend communication
- **Health Monitoring**: Built-in health checks and logging

## API Endpoints

### Core Endpoints

- `GET /` - Service information and status
- `GET /health` - Health check endpoint
- `GET /api/models` - Available AI models and configurations

### Interview Management

- `POST /api/interview/start` - Start a new interview session
- `POST /api/interview/question` - Generate a new question
- `POST /api/interview/answer` - Submit an answer for scoring
- `POST /api/interview/end` - End an interview session
- `GET /api/interview/session/{session_id}` - Get session information

## Quick Start

### Using Docker Compose (Recommended)

The backend service is included in the main PrepWise docker-compose setup:

```bash
# Start all services including backend
./start.sh
```

The service will be available at `http://localhost:8002`

### Using Docker

1. Build the image:
   ```bash
   docker build -t backend-service .
   ```

2. Run the container:
   ```bash
   docker run -p 8002:8002 backend-service
   ```

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python app/main.py
   ```

## API Usage Examples

### Start Interview

```bash
curl -X POST "http://localhost:8002/api/interview/start" \
     -H "Content-Type: application/json" \
     -d '{
       "position": "software_engineer",
       "personality": "professional_friendly"
     }'
```

### Generate Question

```bash
curl -X POST "http://localhost:8002/api/interview/question" \
     -H "Content-Type: application/json" \
     -d '{
       "session_id": "session-uuid-here"
     }'
```

### Submit Answer

```bash
curl -X POST "http://localhost:8002/api/interview/answer" \
     -H "Content-Type: application/json" \
     -d '{
       "session_id": "session-uuid-here",
       "question_id": "question-uuid-here",
       "answer_text": "My answer here..."
     }'
```

## Response Format

All endpoints return a standardized response format:

```json
{
  "success": true,
  "data": {
    "session": {...},
    "question": {...},
    "score": {...}
  },
  "error": null
}
```

## Architecture

The backend service implements a mock agentic system that can be extended with:

- **Real AI Models**: Integration with Google Gemini, OpenAI, or other LLMs
- **Agent Framework**: LangChain or LangGraph for complex agent workflows
- **Database**: Persistent storage for sessions and analytics
- **Caching**: Redis for improved performance
- **Queue System**: Celery for background processing

## Configuration

### Environment Variables

- `PYTHONPATH`: Python path (default: "/app")

### Future Integrations

- `GEMINI_API_KEY`: Google Gemini API key
- `OPENAI_API_KEY`: OpenAI API key
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection string

## Development

### Project Structure

```
backend-service/
├── app/
│   └── main.py          # FastAPI application
├── logs/                # Log files (created at runtime)
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition
└── README.md           # This file
```

### Adding New Features

1. Modify `app/main.py` to add new endpoints
2. Update `requirements.txt` if new dependencies are needed
3. Rebuild the Docker image
4. Update this README with new API documentation

## Integration with Frontend

The backend service is designed to work seamlessly with the frontend service:

- **CORS Enabled**: Allows cross-origin requests from the frontend
- **Shared Models**: Uses the same Pydantic models as the frontend
- **RESTful Design**: Clean API design for easy frontend integration
- **Error Handling**: Comprehensive error responses for frontend handling

## License

This service is part of the PrepWise project.
