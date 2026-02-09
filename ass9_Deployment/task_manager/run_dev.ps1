# Stop any running python/streamlit processes (Optional, but helps with port conflicts)
Write-Host "Stopping any orphan python processes..."
taskkill /IM python.exe /F 2>$null
taskkill /IM streamlit.exe /F 2>$null

# Start MongoDB using Docker
Write-Host "Starting MongoDB..."
docker-compose -f mongodb.yaml up -d mongo

# Wait for Mongo to be ready
Start-Sleep -Seconds 5

# Start Backend in new window
Write-Host "Starting Backend on Port 8000..."
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn main:app --reload --port 8000" -WorkingDirectory "backend"

# Start Frontend in new window
Write-Host "Starting Frontend on Port 8501..."
Start-Process -NoNewWindow -FilePath "streamlit" -ArgumentList "run app.py --server.port 8501" -WorkingDirectory "frontend"

Write-Host "Apps started! Backend: http://localhost:8000, Frontend: http://localhost:8501"
