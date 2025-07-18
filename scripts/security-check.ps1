# HomelabWiki Security Check (PowerShell)
# This script validates that your HomelabWiki deployment follows security best practices

param(
    [switch]$Verbose
)

# Colors for output
$Color = @{
    Green = "Green"
    Red = "Red"
    Yellow = "Yellow"
    Cyan = "Cyan"
}

function Write-Status {
    param(
        [string]$Status,
        [string]$Message
    )
    
    switch ($Status) {
        "OK" { Write-Host "✅ $Message" -ForegroundColor $Color.Green }
        "WARN" { Write-Host "⚠️  $Message" -ForegroundColor $Color.Yellow }
        "FAIL" { Write-Host "❌ $Message" -ForegroundColor $Color.Red }
    }
}

function Write-Header {
    param([string]$Title)
    Write-Host "`n=== $Title ===" -ForegroundColor $Color.Cyan
}

function Test-EnvFile {
    Write-Header "Environment File Security"
    
    if (-not (Test-Path ".env")) {
        Write-Status "FAIL" ".env file not found. Copy from config/env/.env.example"
        return $false
    }
    
    Write-Status "OK" ".env file exists"
    
    # Check file permissions (Windows)
    try {
        $acl = Get-Acl ".env"
        $accessRules = $acl.Access | Where-Object { $_.IdentityReference -eq $env:USERNAME }
        if ($accessRules) {
            Write-Status "OK" ".env file has user-specific permissions"
        } else {
            Write-Status "WARN" ".env file permissions should be restricted to current user"
        }
    } catch {
        Write-Status "WARN" "Could not check .env file permissions"
    }
    
    return $true
}

function Test-SecretKey {
    Write-Header "Secret Key Security"
    
    if (-not (Select-String -Path ".env" -Pattern "^SECRET_KEY=" -Quiet)) {
        Write-Status "FAIL" "SECRET_KEY not found in .env"
        return $false
    }
    
    $secretKey = (Select-String -Path ".env" -Pattern "^SECRET_KEY=(.*)$").Matches.Groups[1].Value
    
    if ($secretKey -eq "REPLACE_WITH_SECURE_32_CHAR_SECRET_KEY") {
        Write-Status "FAIL" "SECRET_KEY still contains placeholder value"
        return $false
    }
    
    if ($secretKey.Length -lt 32) {
        Write-Status "FAIL" "SECRET_KEY is too short ($($secretKey.Length) characters, minimum 32)"
        return $false
    }
    
    Write-Status "OK" "SECRET_KEY is properly configured ($($secretKey.Length) characters)"
    return $true
}

function Test-LdapPassword {
    Write-Header "LDAP Password Security"
    
    if (-not (Select-String -Path ".env" -Pattern "^LDAP_BIND_PASSWORD=" -Quiet)) {
        Write-Status "FAIL" "LDAP_BIND_PASSWORD not found in .env"
        return $false
    }
    
    $ldapPassword = (Select-String -Path ".env" -Pattern "^LDAP_BIND_PASSWORD=(.*)$").Matches.Groups[1].Value
    
    if ($ldapPassword -eq "REPLACE_WITH_ACTUAL_LDAP_PASSWORD") {
        Write-Status "FAIL" "LDAP_BIND_PASSWORD still contains placeholder value"
        return $false
    }
    
    if ($ldapPassword.Length -lt 8) {
        Write-Status "WARN" "LDAP_BIND_PASSWORD is shorter than 8 characters"
    } else {
        Write-Status "OK" "LDAP_BIND_PASSWORD is configured"
    }
    
    return $true
}

function Test-DatabasePassword {
    Write-Header "Database Password Security"
    
    if (Select-String -Path ".env" -Pattern "^POSTGRES_PASSWORD=" -Quiet) {
        $postgresPassword = (Select-String -Path ".env" -Pattern "^POSTGRES_PASSWORD=(.*)$").Matches.Groups[1].Value
        
        if ($postgresPassword -eq "REPLACE_WITH_SECURE_DB_PASSWORD") {
            Write-Status "FAIL" "POSTGRES_PASSWORD still contains placeholder value"
            return $false
        }
        
        if ($postgresPassword.Length -lt 8) {
            Write-Status "WARN" "POSTGRES_PASSWORD is shorter than 8 characters"
        } else {
            Write-Status "OK" "POSTGRES_PASSWORD is configured"
        }
    } else {
        Write-Status "OK" "Using SQLite (no PostgreSQL password required)"
    }
    
    return $true
}

function Test-DockerCompose {
    Write-Header "Docker Compose Security"
    
    if (-not (Test-Path "docker-compose.yml")) {
        Write-Status "FAIL" "docker-compose.yml not found"
        return $false
    }
    
    # Check for hardcoded passwords
    $content = Get-Content "docker-compose.yml" -Raw
    
    if ($content -like "*WikiService123!*") {
        Write-Status "FAIL" "Hardcoded password found in docker-compose.yml"
        return $false
    }
    
    if ($content -like "*change-this-in-production*") {
        Write-Status "FAIL" "Default secret key found in docker-compose.yml"
        return $false
    }
    
    if ($content -like "*wiki_password*") {
        Write-Status "FAIL" "Default database password found in docker-compose.yml"
        return $false
    }
    
    Write-Status "OK" "No hardcoded credentials found in docker-compose.yml"
    return $true
}

function Test-GitIgnore {
    Write-Header "Git Security"
    
    if (-not (Test-Path ".gitignore")) {
        Write-Status "WARN" ".gitignore file not found"
        return $false
    }
    
    if (Select-String -Path ".gitignore" -Pattern "^\.env$" -Quiet) {
        Write-Status "OK" ".env file is properly ignored by git"
    } else {
        Write-Status "FAIL" ".env file is NOT ignored by git (security risk!)"
        return $false
    }
    
    if (Select-String -Path ".gitignore" -Pattern "^.*\.env$" -Quiet) {
        Write-Status "OK" "All .env files are ignored by git"
    } else {
        Write-Status "WARN" "Consider adding *.env to .gitignore for additional protection"
    }
    
    return $true
}

function Test-Services {
    Write-Header "Service Security"
    
    if (Get-Command docker-compose -ErrorAction SilentlyContinue) {
        try {
            $services = docker-compose ps
            if ($services -match "Up") {
                Write-Status "OK" "Docker services are running"
                
                # Check if health endpoint is accessible
                try {
                    $response = Invoke-WebRequest -Uri "http://localhost:5000/health" -TimeoutSec 5
                    if ($response.StatusCode -eq 200) {
                        Write-Status "OK" "Backend health check passed"
                    } else {
                        Write-Status "WARN" "Backend health check failed (service may be starting)"
                    }
                } catch {
                    Write-Status "WARN" "Backend health check failed (service may be starting)"
                }
            } else {
                Write-Status "WARN" "Docker services are not running"
            }
        } catch {
            Write-Status "WARN" "Could not check Docker services"
        }
    } else {
        Write-Status "WARN" "docker-compose not found"
    }
}

function Show-Recommendations {
    Write-Header "Security Recommendations"
    
    Write-Host "1. Regularly rotate credentials (every 90 days)"
    Write-Host "2. Monitor authentication logs for suspicious activity"
    Write-Host "3. Use strong, unique passwords for all services"
    Write-Host "4. Keep .env file permissions restricted to current user"
    Write-Host "5. Never commit .env files to version control"
    Write-Host "6. Use HTTPS in production with reverse proxy"
    Write-Host "7. Regular security audits and updates"
    Write-Host "8. Implement network segmentation"
    Write-Host "9. Configure automated backups"
    Write-Host "10. Set up monitoring and alerting"
}

function Generate-SecretKey {
    Write-Header "Secret Key Generator"
    
    $bytes = New-Object byte[] 32
    $rng = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    $rng.GetBytes($bytes)
    $secretKey = [System.Convert]::ToBase64String($bytes)
    
    Write-Host "Generated Secret Key:" -ForegroundColor $Color.Cyan
    Write-Host $secretKey -ForegroundColor $Color.Green
    Write-Host "`nAdd this to your .env file:" -ForegroundColor $Color.Cyan
    Write-Host "SECRET_KEY=$secretKey" -ForegroundColor $Color.Green
}

# Main execution
function Main {
    Write-Host "HomelabWiki Security Validation" -ForegroundColor $Color.Green
    Write-Host "================================="
    
    $checksPassed = 0
    $totalChecks = 6
    
    # Run all security checks
    if (Test-EnvFile) { $checksPassed++ }
    if (Test-SecretKey) { $checksPassed++ }
    if (Test-LdapPassword) { $checksPassed++ }
    if (Test-DatabasePassword) { $checksPassed++ }
    if (Test-DockerCompose) { $checksPassed++ }
    if (Test-GitIgnore) { $checksPassed++ }
    
    # Optional service check (doesn't count toward total)
    Test-Services
    
    # Generate recommendations
    Show-Recommendations
    
    # Option to generate secret key
    if ($checksPassed -lt $totalChecks) {
        Write-Host "`nWould you like to generate a secure secret key? (y/n): " -NoNewline
        $response = Read-Host
        if ($response -eq "y" -or $response -eq "Y") {
            Generate-SecretKey
        }
    }
    
    # Final summary
    Write-Header "Security Summary"
    Write-Host "Checks passed: $checksPassed/$totalChecks"
    
    if ($checksPassed -eq $totalChecks) {
        Write-Status "OK" "All security checks passed! ✨"
        exit 0
    } else {
        Write-Status "FAIL" "Some security checks failed. Please review and fix issues above."
        exit 1
    }
}

# Run main function
Main
