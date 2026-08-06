Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     ProPoj CLI - Interaktivní Nastavení Azure              ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# Kontrola Node.js
if (-not (Get-Command node -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Node.js není nainstalován" -ForegroundColor Red
    Write-Host "Stáhni Node.js z https://nodejs.org" -ForegroundColor Yellow
    exit 1
}

# Kontrola npm balíčků
if (-not (Test-Path "node_modules")) {
    Write-Host "📦 Instaluji npm balíčky..." -ForegroundColor Yellow
    npm install
}

# Kontrola TypeScript build
if (-not (Test-Path "dist")) {
    Write-Host "🔨 Kompiluji TypeScript projekt..." -ForegroundColor Yellow
    npm run build
}

Write-Host "`n📋 Máš otevřenou stránku Azure Portal s tvou aplikací?" -ForegroundColor Cyan
Write-Host "Pokud ne, jdi na: https://portal.azure.com" -ForegroundColor Gray
Write-Host "Azure Active Directory → App registrations → Tvá aplikace`n" -ForegroundColor Gray

# Client ID
Write-Host "1️⃣  Zkopíruj 'Application (client) ID' a vklej zde:" -ForegroundColor Cyan
$CLIENT_ID = Read-Host "   Client ID"

if ([string]::IsNullOrEmpty($CLIENT_ID)) {
    Write-Host "❌ Client ID je povinný" -ForegroundColor Red
    exit 1
}

# Tenant ID
Write-Host "`n2️⃣  Zkopíruj 'Directory (tenant) ID' a vklej zde:" -ForegroundColor Cyan
$TENANT_ID = Read-Host "   Tenant ID"

if ([string]::IsNullOrEmpty($TENANT_ID)) {
    Write-Host "❌ Tenant ID je povinný" -ForegroundColor Red
    exit 1
}

Write-Host "`n⏳ Nastavuji ProPoj CLI..." -ForegroundColor Yellow

# Nastavení credentials
& node dist/cli.js auth setup --client-id $CLIENT_ID --tenant-id $TENANT_ID

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║           ✅ Azure Credentials Nastaveny!                  ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝`n" -ForegroundColor Green

    Write-Host "🎉 Nyní můžeš používat ProPoj CLI!`n" -ForegroundColor Green

    Write-Host "Příští krok - Přihlášení:" -ForegroundColor Cyan
    Write-Host "   npm start auth login`n" -ForegroundColor Gray

    Write-Host "Nebo zkus rovnou příkazy:" -ForegroundColor Cyan
    Write-Host "   npm start mail inbox" -ForegroundColor Gray
    Write-Host "   npm start calendar events" -ForegroundColor Gray
    Write-Host "   npm start sharepoint sites`n" -ForegroundColor Gray

    Write-Host "💡 Více pomocí:" -ForegroundColor Cyan
    Write-Host "   npm start --help" -ForegroundColor Gray
} else {
    Write-Host "`n❌ Chyba při nastavování Azure credentials" -ForegroundColor Red
    exit 1
}
