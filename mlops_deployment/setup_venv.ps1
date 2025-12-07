# Setup script for creating virtual environment (Windows PowerShell)

Write-Host "Setting up virtual environment..." -ForegroundColor Green

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Upgrade pip and wheel
python -m pip install --upgrade pip wheel

# Install requirements using pre-built wheels (faster, no compilation)
Write-Host "Installing packages using pre-built wheels..." -ForegroundColor Yellow
pip install -r requirements.txt --only-binary :all: 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "Warning: Some packages couldn't be installed with --only-binary, trying without..." -ForegroundColor Yellow
    pip install -r requirements.txt
}

Write-Host "`n✅ Virtual environment created and dependencies installed!" -ForegroundColor Green
Write-Host ""
Write-Host "To activate the virtual environment, run:" -ForegroundColor Yellow
Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host ""
Write-Host "To deactivate, run:" -ForegroundColor Yellow
Write-Host "  deactivate" -ForegroundColor Cyan

