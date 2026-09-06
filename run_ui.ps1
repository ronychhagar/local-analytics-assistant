$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

Write-Host "Starting Streamlit UI..."
Write-Host "Open http://localhost:8501 after startup"

$uvCmd = Get-Command uv -ErrorAction SilentlyContinue
if ($uvCmd) {
    & uv run streamlit run task_1/streamlit_app.py --server.port 8501 --server.headless true
    exit $LASTEXITCODE
}

$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    throw "Python is not installed or not available on PATH."
}

& python -m streamlit run task_1/streamlit_app.py --server.port 8501 --server.headless true
exit $LASTEXITCODE
