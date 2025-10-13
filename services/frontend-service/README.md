# Frontend Service

Streamlit frontend service for the PrepWise AI interview practice platform.

## Features

- **Streamlit Framework**: Modern, interactive web interface
- **Backend Integration**: Communicates with backend service via REST API
- **Real-time Updates**: Live conversation flow and instant feedback
- **Responsive Design**: Mobile-friendly interface
- **Session Management**: Interview session tracking and analytics

## Quick Start

### Using Docker Compose (Recommended)

The frontend service is included in the main PrepWise docker-compose setup:

```bash
# Start all services including frontend
./start.sh
```

The service will be available at `http://localhost:8501`

### Using Docker

1. Build the image:
   ```bash
   docker build -t frontend-service .
   ```

2. Run the container:
   ```bash
   docker run -p 8501:8501 frontend-service
   ```

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   streamlit run src/streamlit_app.py
   ```

## Features

### Interview Interface

- **Question Display**: Shows AI-generated interview questions
- **Answer Input**: Text area for user responses
- **Real-time Scoring**: Instant feedback and scoring
- **Progress Tracking**: Session statistics and metrics

### Configuration

- **Position Selection**: Choose target interview position
- **Personality Settings**: Select interviewer style
- **Question Types**: Filter by question categories
- **Difficulty Levels**: Adjust question difficulty

### User Experience

- **Welcome Screen**: Introduction and feature highlights
- **Session Management**: Start, pause, and end interviews
- **Tips & Feedback**: Contextual guidance and suggestions
- **Statistics**: Performance tracking and analytics

## Architecture

The frontend service is designed as a thin client that:

- **Communicates with Backend**: All business logic handled by backend service
- **Manages UI State**: Handles user interface and session state
- **Displays Data**: Renders interview questions, answers, and feedback
- **Handles User Input**: Captures user responses and configuration

## Backend Integration

The frontend communicates with the backend service through:

- **REST API Calls**: HTTP requests to backend endpoints
- **Shared Models**: Uses the same Pydantic models as backend
- **Error Handling**: Graceful handling of backend errors
- **Health Checks**: Monitors backend service availability

## Configuration

### Environment Variables

- `PYTHONPATH`: Python path (default: "/app")
- `STREAMLIT_SERVER_PORT`: Streamlit port (default: 8501)
- `STREAMLIT_SERVER_ADDRESS`: Streamlit address (default: 0.0.0.0)

### Backend Service URL

The frontend connects to the backend service at:
- **Docker**: `http://backend-service:8002`
- **Local**: `http://localhost:8002`

## Development

### Project Structure

```
frontend-service/
├── src/
│   └── streamlit_app.py # Streamlit application
├── logs/                # Log files (created at runtime)
├── requirements.txt     # Python dependencies
├── Dockerfile          # Container definition
└── README.md           # This file
```

### Key Components

- **BackendClient**: Handles communication with backend service
- **UI Components**: Modular Streamlit components
- **Session State**: Manages user session and conversation history
- **Error Handling**: User-friendly error messages

### Adding New Features

1. Modify `src/streamlit_app.py` to add new UI components
2. Update backend service if new API endpoints are needed
3. Update `requirements.txt` if new dependencies are needed
4. Rebuild the Docker image

## User Interface

### Main Sections

1. **Header**: Application title and branding
2. **Sidebar**: Configuration and controls
3. **Welcome Screen**: Introduction when no session is active
4. **Interview Interface**: Main conversation area
5. **Controls**: Question generation and session management
6. **Tips & Feedback**: Guidance and performance metrics

### Responsive Design

- **Wide Layout**: Optimized for desktop viewing
- **Mobile Friendly**: Responsive components for mobile devices
- **Sidebar**: Collapsible configuration panel
- **Columns**: Flexible layout for different screen sizes

## Integration with Other Services

The frontend service integrates with:

- **Backend Service**: Core interview functionality
- **Transcription Service**: Voice input capabilities (future)
- **Resume Parsing Service**: Resume analysis (future)

## License

This service is part of the PrepWise project.
