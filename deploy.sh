#!/bin/bash

echo "🚀 NWN GFF API Service - Docker Deployment"
echo "=========================================="

# Check if Docker and Docker Compose are installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create logs directory
echo "📁 Creating logs directory..."
mkdir -p logs

# Build and start the NWN GFF API Service
echo "🏗️  Building NWN GFF API Service..."
docker-compose build

echo "🚀 Starting NWN GFF API Service..."
docker-compose up -d

# Wait for service to be ready
echo "⏳ Waiting for service to be ready..."
for i in {1..10}; do
    if curl -f http://localhost:8000/api/v1/health &>/dev/null; then
        echo "✅ Service is healthy"
        break
    fi
    echo "⏳ Waiting for service... (attempt $i/10)"
    sleep 10
done

# Final status
echo ""
echo "🎉 NWN GFF API Service is ready!"
echo "=================================="
echo "🌐 API: http://localhost:8000"
echo "📚 API Documentation: http://localhost:8000/docs"
echo "🔧 Health Check: http://localhost:8000/api/v1/health"
echo ""
echo "🛠️  To stop the service: docker-compose down"
echo "🔄 To restart: docker-compose restart"
echo ""
echo "📁 Logs are available in the ./logs directory"