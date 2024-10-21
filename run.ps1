param(
  [int]$Port = 8001
)

Write-Host "Starting comment-system on port $Port"
python -m uvicorn app:app --host 0.0.0.0 --port $Port