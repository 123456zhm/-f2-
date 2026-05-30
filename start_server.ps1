$env:PYTHONPATH = "C:\Users\123\Desktop\f2-xiaohongshu-changes\f2"
Set-Location "C:\Users\123\Desktop\f2-xiaohongshu-changes\f2"

Write-Host "Starting backend server..."
Write-Host "Press Ctrl+C to stop the server"
Write-Host ""

$process = Start-Process -FilePath "python" -ArgumentList "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000" -PassThru -WindowStyle Normal

Write-Host "Server started with PID: $($process.Id)"
Write-Host "Waiting for server to be ready..."

Start-Sleep -Seconds 3

if (-not $process.HasExited) {
    Write-Host "Server is running on http://localhost:8000"
    Write-Host "Press Ctrl+C to stop the server"
    
    try {
        while (-not $process.HasExited) {
            Start-Sleep -Seconds 1
        }
    }
    finally {
        Write-Host "`nStopping server..."
        Stop-Process -Id $process.Id -Force -ErrorAction SilentlyContinue
        Write-Host "Server stopped."
    }
} else {
    Write-Host "Server failed to start!"
}