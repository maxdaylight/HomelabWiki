#!/usr/bin/env pwsh

# HomelabWiki Docker Security Scanner
# This script scans Docker images for vulnerabilities using multiple security tools

param(
    [string]$Image = "all",
    [switch]$Detailed = $false,
    [switch]$JsonOutput = $false,
    [string]$OutputFile = "",
    [switch]$FailOnVulnerabilities = $false
)

# Color output functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = "White"
    )
    
    switch ($Color) {
        "Red" { Write-Host $Message -ForegroundColor Red }
        "Green" { Write-Host $Message -ForegroundColor Green }
        "Yellow" { Write-Host $Message -ForegroundColor Yellow }
        "Cyan" { Write-Host $Message -ForegroundColor Cyan }
        "Blue" { Write-Host $Message -ForegroundColor Blue }
        "Magenta" { Write-Host $Message -ForegroundColor Magenta }
        default { Write-Host $Message }
    }
}

function Test-CommandExists {
    param([string]$Command)
    return (Get-Command $Command -ErrorAction SilentlyContinue) -ne $null
}

function Scan-WithTrivy {
    param(
        [string]$ImageName,
        [string]$OutputFormat = "table"
    )
    
    Write-ColorOutput "🔍 Scanning $ImageName with Trivy..." "Cyan"
    
    $trivyArgs = @(
        "image",
        "--security-checks", "vuln",
        "--format", $OutputFormat
    )
    
    if ($Detailed) {
        $trivyArgs += "--severity", "UNKNOWN,LOW,MEDIUM,HIGH,CRITICAL"
    } else {
        $trivyArgs += "--severity", "HIGH,CRITICAL"
    }
    
    $trivyArgs += $ImageName
    
    try {
        $result = docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
            -v "${PWD}:/app" aquasec/trivy @trivyArgs
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Trivy scan completed for $ImageName" "Green"
            return $result
        } else {
            Write-ColorOutput "❌ Trivy scan failed for $ImageName" "Red"
            return $null
        }
    } catch {
        Write-ColorOutput "❌ Error running Trivy scan: $($_.Exception.Message)" "Red"
        return $null
    }
}

function Scan-WithSnyk {
    param([string]$ImageName)
    
    if (-not (Test-CommandExists "snyk")) {
        Write-ColorOutput "⚠️ Snyk CLI not found. Skipping Snyk scan." "Yellow"
        return $null
    }
    
    Write-ColorOutput "🔍 Scanning $ImageName with Snyk..." "Cyan"
    
    try {
        $result = snyk container test $ImageName --severity-threshold=high
        
        if ($LASTEXITCODE -eq 0) {
            Write-ColorOutput "✅ Snyk scan completed for $ImageName" "Green"
            return $result
        } else {
            Write-ColorOutput "❌ Snyk scan found vulnerabilities in $ImageName" "Red"
            return $result
        }
    } catch {
        Write-ColorOutput "❌ Error running Snyk scan: $($_.Exception.Message)" "Red"
        return $null
    }
}

function Get-ImageVulnerabilities {
    param([string]$ImageName)
    
    $results = @{
        "ImageName" = $ImageName
        "Trivy" = $null
        "Snyk" = $null
        "Timestamp" = Get-Date
    }
    
    # Scan with Trivy
    if (Test-CommandExists "docker") {
        $results.Trivy = Scan-WithTrivy -ImageName $ImageName
    } else {
        Write-ColorOutput "⚠️ Docker not found. Cannot run Trivy scan." "Yellow"
    }
    
    # Scan with Snyk
    $results.Snyk = Scan-WithSnyk -ImageName $ImageName
    
    return $results
}

function Get-ProjectImages {
    $images = @()
    
    # Check if docker-compose.yml exists
    if (Test-Path "docker-compose.yml") {
        Write-ColorOutput "📋 Finding images from docker-compose.yml..." "Cyan"
        
        try {
            $composeImages = docker-compose config --services | ForEach-Object {
                "homelabwiki-$_"
            }
            $images += $composeImages
        } catch {
            Write-ColorOutput "⚠️ Could not parse docker-compose.yml" "Yellow"
        }
    }
    
    # Add common image names
    $images += @(
        "homelabwiki-backend",
        "homelabwiki-frontend",
        "homelabwiki_backend",
        "homelabwiki_frontend"
    )
    
    # Filter to only existing images
    $existingImages = @()
    foreach ($img in $images) {
        try {
            docker image inspect $img | Out-Null
            $existingImages += $img
        } catch {
            # Image doesn't exist, skip
        }
    }
    
    return $existingImages
}

function Export-Results {
    param(
        [array]$Results,
        [string]$FilePath
    )
    
    if ($JsonOutput) {
        $Results | ConvertTo-Json -Depth 10 | Out-File -FilePath $FilePath
        Write-ColorOutput "📄 Results exported to $FilePath (JSON)" "Green"
    } else {
        $Results | Out-File -FilePath $FilePath
        Write-ColorOutput "📄 Results exported to $FilePath (Text)" "Green"
    }
}

# Main execution
Write-ColorOutput "🚀 HomelabWiki Docker Security Scanner" "Green"
Write-ColorOutput "====================================" "Green"

# Check prerequisites
if (-not (Test-CommandExists "docker")) {
    Write-ColorOutput "❌ Docker is not installed or not in PATH" "Red"
    exit 1
}

# Determine images to scan
$imagesToScan = @()

if ($Image -eq "all") {
    $imagesToScan = Get-ProjectImages
    if ($imagesToScan.Count -eq 0) {
        Write-ColorOutput "⚠️ No HomelabWiki images found. Build your images first with 'docker-compose build'" "Yellow"
        exit 1
    }
} else {
    $imagesToScan = @($Image)
}

Write-ColorOutput "🎯 Scanning images: $($imagesToScan -join ', ')" "Cyan"

# Perform scans
$allResults = @()
$hasVulnerabilities = $false

foreach ($img in $imagesToScan) {
    Write-ColorOutput "`n" + "="*50 "Blue"
    Write-ColorOutput "🔍 Scanning: $img" "Blue"
    Write-ColorOutput "="*50 "Blue"
    
    $result = Get-ImageVulnerabilities -ImageName $img
    $allResults += $result
    
    # Check if vulnerabilities were found
    if ($result.Trivy -and $result.Trivy -match "(HIGH|CRITICAL)") {
        $hasVulnerabilities = $true
    }
}

# Export results if requested
if ($OutputFile -ne "") {
    Export-Results -Results $allResults -FilePath $OutputFile
}

# Summary
Write-ColorOutput "`n" + "="*50 "Green"
Write-ColorOutput "📊 SCAN SUMMARY" "Green"
Write-ColorOutput "="*50 "Green"
Write-ColorOutput "Images scanned: $($imagesToScan.Count)" "Cyan"
Write-ColorOutput "Timestamp: $(Get-Date)" "Cyan"

if ($hasVulnerabilities) {
    Write-ColorOutput "⚠️ Vulnerabilities found in one or more images" "Red"
    Write-ColorOutput "📋 Recommended actions:" "Yellow"
    Write-ColorOutput "  1. Update base images to latest versions" "White"
    Write-ColorOutput "  2. Run: ./scripts/update-docker-images.ps1" "White"
    Write-ColorOutput "  3. Rebuild images: docker-compose build" "White"
    Write-ColorOutput "  4. Re-run security scan" "White"
    
    if ($FailOnVulnerabilities) {
        Write-ColorOutput "❌ Exiting with error due to vulnerabilities" "Red"
        exit 1
    }
} else {
    Write-ColorOutput "✅ No high or critical vulnerabilities found" "Green"
}

Write-ColorOutput "`n🔐 Security Tips:" "Blue"
Write-ColorOutput "  • Run scans regularly (weekly/monthly)" "White"
Write-ColorOutput "  • Subscribe to security advisories" "White"
Write-ColorOutput "  • Use specific image tags (avoid 'latest')" "White"
Write-ColorOutput "  • Keep dependencies updated" "White"
Write-ColorOutput "  • Monitor CVE databases" "White"
