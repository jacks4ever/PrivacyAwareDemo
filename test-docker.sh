#!/bin/bash

# Test script to verify Docker configuration
echo "Testing Docker configuration for Morning Sky Website..."

echo "1. Checking if all required files exist:"
files=("index.html" "style.css" "script.js" "server.py" "Dockerfile.website" "docker-compose.yml")

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
    fi
done

echo ""
echo "2. Docker commands to run the website:"
echo "   docker-compose build website"
echo "   docker-compose up website"
echo ""
echo "3. Expected result:"
echo "   Website should be accessible at http://localhost:12000"
echo "   Features: Morning gradient sky, wispy clouds, pink hot air balloon, interactive button"
echo ""
echo "4. To run both services:"
echo "   docker-compose up --build"
echo "   Privacy demo: http://localhost:12001"
echo "   Morning sky website: http://localhost:12000"