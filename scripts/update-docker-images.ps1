# HomelabWiki Docker Image Update Script
# This script helps keep Docker base images updated to address security vulnerabilities

param(
    [switch]$DryRun = $false,
    [switch]$Force = $false
)

Write-Host "HomelabWiki Docker Image Update Script" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Function to check if Docker is available
function Test-DockerAvailable {
    try {
        docker version | Out-Null
        return $true
    }
    catch {
        return $false
    }
}

# Function to get latest stable versions
function Get-LatestVersions {
    $versions = @{
        "python" = "3.12"  # Current stable
        "node" = "20"      # Current LTS
        "nginx" = "1.26"   # Current stable
    }
    return $versions
}

# Function to update Dockerfile
function Update-Dockerfile {
    param(
        [string]$FilePath,
        [string]$BaseImage,
        [string]$NewVersion
    )
    
    if (-not (Test-Path $FilePath)) {
        Write-Warning "Dockerfile not found: $FilePath"
        return
    }
    
    $content = Get-Content $FilePath -Raw
    $oldPattern = "FROM $BaseImage`:\d+[\.\d+]*[-\w]*"
    $newImage = "FROM $BaseImage`:$NewVersion"
    
    if ($content -match $oldPattern) {
        $oldImage = $Matches[0]
        Write-Host "Updating $FilePath" -ForegroundColor Yellow
        Write-Host "  Old: $oldImage" -ForegroundColor Red
        Write-Host "  New: $newImage" -ForegroundColor Green
        
        if (-not $DryRun) {
            $content = $content -replace $oldPattern, $newImage
            Set-Content $FilePath $content -NoNewline
            Write-Host "  Updated!" -ForegroundColor Green
        } else {
            Write-Host "  (Dry run - no changes made)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "No matching pattern found in $FilePath" -ForegroundColor Yellow
    }
}

# Function to run security scan
function Invoke-SecurityScan {
    param([string]$ImageName)
    
    if (Get-Command "docker" -ErrorAction SilentlyContinue) {
        Write-Host "Running security scan for $ImageName..." -ForegroundColor Yellow
        try {
            docker run --rm -v /var/run/docker.sock:/var/run/docker.sock `
                -v (Get-Location):/app aquasec/trivy image $ImageName
        }
        catch {
            Write-Warning "Security scan failed for $ImageName"
        }
    } else {
        Write-Warning "Docker not available for security scanning"
    }
}

# Main execution
if (-not (Test-DockerAvailable)) {
    Write-Error "Docker is not available. Please install Docker and try again."
    exit 1
}

Write-Host "Checking for Docker image updates..." -ForegroundColor Cyan

$versions = Get-LatestVersions
$backendDockerfile = "backend/Dockerfile"
$frontendDockerfile = "frontend/Dockerfile"

# Update backend Dockerfile
if (Test-Path $backendDockerfile) {
    Update-Dockerfile -FilePath $backendDockerfile -BaseImage "python" -NewVersion "$($versions.python)-slim"
} else {
    Write-Warning "Backend Dockerfile not found"
}

# Update frontend Dockerfile
if (Test-Path $frontendDockerfile) {
    Update-Dockerfile -FilePath $frontendDockerfile -BaseImage "node" -NewVersion "$($versions.node)-alpine"
    Update-Dockerfile -FilePath $frontendDockerfile -BaseImage "nginx" -NewVersion "$($versions.nginx)-alpine"
} else {
    Write-Warning "Frontend Dockerfile not found"
}

if ($DryRun) {
    Write-Host "`nDry run completed. No changes were made." -ForegroundColor Yellow
    Write-Host "Run without -DryRun to apply changes." -ForegroundColor Yellow
} else {
    Write-Host "`nDocker images updated successfully!" -ForegroundColor Green
    Write-Host "Remember to rebuild your containers:" -ForegroundColor Cyan
    Write-Host "  docker-compose build" -ForegroundColor White
    Write-Host "  docker-compose up -d" -ForegroundColor White
}

Write-Host "`nSecurity recommendations:" -ForegroundColor Cyan
Write-Host "1. Run security scans regularly" -ForegroundColor White
Write-Host "2. Keep base images updated" -ForegroundColor White
Write-Host "3. Use specific version tags (avoid 'latest')" -ForegroundColor White
Write-Host "4. Review and update dependencies" -ForegroundColor White
