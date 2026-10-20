# FairLens Master PowerShell Entry Point (run.ps1)
# Usage:
#   .\run.ps1 test       - Run all unit and integration tests
#   .\run.ps1 demo       - Run end-to-end reproducible offline demonstration
#   .\run.ps1 api-check  - Run zero-cost OpenRouter API connectivity / configuration check
#   .\run.ps1 audit      - Run dataset representation gap audit

param (
    [Parameter(Position = 0)]
    [string]$Command = "help",

    [Parameter(ValueFromRemainingArguments = $true)]
    [string[]]$RemainingArgs
)

$ErrorActionPreference = "Stop"
$env:PYTHONPATH = "src"

function Show-Help {
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host "  FairLens: Automated Dataset & Model Fairness Framework  " -ForegroundColor Cyan
    Write-Host "  M.Tech Project (MASET697) | VIT Vellore                 " -ForegroundColor Cyan
    Write-Host "==========================================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Commands:" -ForegroundColor Yellow
    Write-Host "  .\run.ps1 test             Run all unit and integration test suites"
    Write-Host "  .\run.ps1 demo             Run complete offline end-to-end demonstration"
    Write-Host "  .\run.ps1 api-check        Verify OpenRouter API config and dry-run pricing"
    Write-Host "  .\run.ps1 audit <args>     Run Phase 4 representation-gap audit on a dataset"
    Write-Host "  .\run.ps1 discovery <args> Run Phase 3 dataset discovery search"
    Write-Host "  .\run.ps1 help             Show this help menu"
    Write-Host ""
}

switch ($Command.ToLower()) {
    "test" {
        Write-Host "--> Running FairLens Test Suite..." -ForegroundColor Green
        python -m unittest discover -s tests -p "test_*.py" -v
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Tests failed with exit code $LASTEXITCODE" -ForegroundColor Red
            exit $LASTEXITCODE
        }
        Write-Host "--> All tests passed successfully." -ForegroundColor Green
    }

    "api-check" {
        Write-Host "--> Verifying FairLens Configuration & Pricing..." -ForegroundColor Green
        python -c "
import sys
from fairlens.config.settings import get_settings
from fairlens.api.pricing import CostEstimator

s = get_settings()
print('=== FairLens System Configuration ===')
print(repr(s))
print('\n=== OpenRouter Target Model Info ===')
estimator = CostEstimator(
    default_input_price_per_m=s.input_price_per_m,
    default_output_price_per_m=s.output_price_per_m,
    max_spend_usd=s.max_spend_usd
)
info = estimator.get_pricing_info(s.openrouter_model)
for k, v in info.items():
    print(f'  {k}: {v}')

print('\n=== Sample Audit Cost Projection (1,000 Questions) ===')
est = estimator.estimate(
    total_requests=1000,
    avg_input_tokens=600,
    avg_output_tokens=250,
    model=s.openrouter_model,
    use_free_tier=True
)
print(est.format_summary())
"
    }

    "demo" {
        Write-Host "--> Executing FairLens Offline End-to-End Demo..." -ForegroundColor Green
        python -m fairlens.demo
    }

    "audit" {
        Write-Host "--> Running FairLens Dataset Representation Audit..." -ForegroundColor Green
        python -m fairlens.auditing.cli @RemainingArgs
    }

    "discovery" {
        Write-Host "--> Running FairLens Dataset Discovery Engine..." -ForegroundColor Green
        python -m fairlens.discovery.cli @RemainingArgs
    }

    default {
        Show-Help
    }
}
