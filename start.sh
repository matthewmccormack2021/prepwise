#!/bin/bash
# PrepWise Startup Script
# This script starts both the transcription service and the main agentic system

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    print_status "Checking if Docker is running..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker first."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if ports are available
check_ports() {
    print_status "Checking if required ports are available..."
    
    if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 8000 is already in use. Transcription service may not start properly."
    fi
    
    if lsof -Pi :8501 -sTCP:LISTEN -t >/dev/null 2>&1; then
        print_warning "Port 8501 is already in use. Main app may not start properly."
    fi
    
    print_success "Port check completed"
}

# Function to build and start services
start_services() {
    print_status "Building and starting PrepWise services..."
    
    # Build and start all services
    docker-compose up --build -d
    
    print_success "Services started successfully"
}

# Function to wait for services to be ready
wait_for_services() {
    print_status "Waiting for services to be ready..."
    
    # Wait for transcription service
    print_status "Waiting for transcription service..."
    for i in {1..30}; do
        if curl -f http://localhost:8000/health > /dev/null 2>&1; then
            print_success "Transcription service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Transcription service may not be ready yet"
        fi
        sleep 2
    done
    
    # Wait for backend service
    print_status "Waiting for backend service..."
    for i in {1..30}; do
        if curl -f http://localhost:8002/health > /dev/null 2>&1; then
            print_success "Backend service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Backend service may not be ready yet"
        fi
        sleep 2
    done
    
    # Wait for frontend service
    print_status "Waiting for frontend service..."
    for i in {1..30}; do
        if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
            print_success "Frontend service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Frontend service may not be ready yet"
        fi
        sleep 2
    done
    
    # Wait for resume parsing service
    print_status "Waiting for resume parsing service..."
    for i in {1..30}; do
        if curl -f http://localhost:8001/health > /dev/null 2>&1; then
            print_success "Resume parsing service is ready"
            break
        fi
        if [ $i -eq 30 ]; then
            print_warning "Resume parsing service may not be ready yet"
        fi
        sleep 2
    done
}

# Function to test services
test_services() {
    print_status "Testing services..."
    
    # Test transcription service
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        print_success "Transcription service health check passed"
    else
        print_warning "Transcription service health check failed"
    fi
    
    # Test backend service
    if curl -f http://localhost:8002/health > /dev/null 2>&1; then
        print_success "Backend service health check passed"
    else
        print_warning "Backend service health check failed"
    fi
    
    # Test frontend service
    if curl -f http://localhost:8501/_stcore/health > /dev/null 2>&1; then
        print_success "Frontend service health check passed"
    else
        print_warning "Frontend service health check failed"
    fi
    
    # Test resume parsing service
    if curl -f http://localhost:8001/health > /dev/null 2>&1; then
        print_success "Resume parsing service health check passed"
    else
        print_warning "Resume parsing service health check failed"
    fi
}

# Function to show service information
show_service_info() {
    echo ""
    print_success "🎉 PrepWise is running successfully!"
    echo ""
    echo "📱 Frontend Service:"
    echo "   URL: http://localhost:8501"
    echo "   Status: $(docker-compose ps frontend-service --format 'table {{.Status}}' | tail -n +2)"
    echo ""
    echo "🔧 Backend Service:"
    echo "   URL: http://localhost:8002"
    echo "   API Docs: http://localhost:8002/docs"
    echo "   Status: $(docker-compose ps backend-service --format 'table {{.Status}}' | tail -n +2)"
    echo ""
    echo "🎤 Transcription Service:"
    echo "   URL: http://localhost:8000"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   Status: $(docker-compose ps transcription-service --format 'table {{.Status}}' | tail -n +2)"
    echo ""
    echo "📄 Resume Parsing Service:"
    echo "   URL: http://localhost:8001"
    echo "   API Docs: http://localhost:8001/docs"
    echo "   Status: $(docker-compose ps resume-parsing-service --format 'table {{.Status}}' | tail -n +2)"
    echo ""
    echo "🔧 Management Commands:"
    echo "   View logs: docker-compose logs -f"
    echo "   Stop services: docker-compose down"
    echo "   Restart services: docker-compose restart"
    echo "   View service status: docker-compose ps"
    echo ""
}

# Function to handle cleanup on exit
cleanup() {
    echo ""
    print_status "Shutting down services..."
    docker-compose down
    print_success "Services stopped"
}

# Set up signal handlers
trap cleanup EXIT INT TERM

# Main execution
main() {
    echo "🚀 Starting PrepWise - AI Interview Practice Platform"
    echo "=================================================="
    echo ""
    
    # Pre-flight checks
    check_docker
    check_ports
    
    # Start services
    start_services
    
    # Wait for services to be ready
    wait_for_services
    
    # Test services
    test_services
    
    # Show service information
    show_service_info
    
    # Keep script running and show logs
    print_status "Press Ctrl+C to stop all services"
    print_status "Viewing logs (press Ctrl+C to stop)..."
    echo ""
    
    # Follow logs
    docker-compose logs -f
}

# Parse command line arguments
case "${1:-}" in
    "stop")
        print_status "Stopping PrepWise services..."
        docker-compose down
        print_success "Services stopped"
        exit 0
        ;;
    "restart")
        print_status "Restarting PrepWise services..."
        docker-compose restart
        print_success "Services restarted"
        exit 0
        ;;
    "status")
        print_status "PrepWise service status:"
        docker-compose ps
        exit 0
        ;;
    "logs")
        print_status "Showing PrepWise logs..."
        docker-compose logs -f
        exit 0
        ;;
    "build")
        print_status "Building PrepWise services..."
        docker-compose build
        print_success "Services built successfully"
        exit 0
        ;;
    "help"|"-h"|"--help")
        echo "PrepWise Startup Script"
        echo ""
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  (no args)  Start all services and follow logs"
        echo "  stop       Stop all services"
        echo "  restart    Restart all services"
        echo "  status     Show service status"
        echo "  logs       Show service logs"
        echo "  build      Build all services"
        echo "  help       Show this help message"
        echo ""
        exit 0
        ;;
    "")
        # No arguments, run main function
        main
        ;;
    *)
        print_error "Unknown command: $1"
        echo "Use '$0 help' for usage information"
        exit 1
        ;;
esac
