#!/bin/bash

echo "╔════════════════════════════════════════════════════════════╗"
echo "║     ProPoj CLI - Interaktivní Nastavení Azure              ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Kontrola, jestli je Node.js nainstalován
if ! command -v node &> /dev/null; then
    echo "❌ Node.js není nainstalován"
    echo "Stáhni Node.js z https://nodejs.org"
    exit 1
fi

# Kontrola, jestli jsou npm balíčky nainstalovány
if [ ! -d "node_modules" ]; then
    echo "📦 Instaluji npm balíčky..."
    npm install
fi

# Kontrola, jestli je projekt zkompilovaný
if [ ! -d "dist" ]; then
    echo "🔨 Kompiluji TypeScript projekt..."
    npm run build
fi

echo ""
echo "📋 Máš otevřenou stránku Azure Portal s tvou aplikací?"
echo "Pokud ne, jdi na: https://portal.azure.com"
echo "Azure Active Directory → App registrations → Tvá aplikace"
echo ""

# Čtení Client ID
echo "1️⃣  Zkopíruj 'Application (client) ID' a vklej zde:"
read -p "   Client ID: " CLIENT_ID

# Validace Client ID
if [ -z "$CLIENT_ID" ]; then
    echo "❌ Client ID je povinný"
    exit 1
fi

echo ""

# Čtení Tenant ID
echo "2️⃣  Zkopíruj 'Directory (tenant) ID' a vklej zde:"
read -p "   Tenant ID: " TENANT_ID

# Validace Tenant ID
if [ -z "$TENANT_ID" ]; then
    echo "❌ Tenant ID je povinný"
    exit 1
fi

echo ""
echo "⏳ Nastavuji ProPoj CLI..."

# Nastavení credentials
node dist/cli.js auth setup \
    --client-id "$CLIENT_ID" \
    --tenant-id "$TENANT_ID"

if [ $? -eq 0 ]; then
    echo ""
    echo "╔════════════════════════════════════════════════════════════╗"
    echo "║           ✅ Azure Credentials Nastaveny!                  ║"
    echo "╚════════════════════════════════════════════════════════════╝"
    echo ""
    echo "🎉 Nyní můžeš používat ProPoj CLI!"
    echo ""
    echo "Příští krok - Přihlášení:"
    echo "   npm start auth login"
    echo ""
    echo "Nebo zkus rovnou příkazy:"
    echo "   npm start mail inbox"
    echo "   npm start calendar events"
    echo "   npm start sharepoint sites"
    echo ""
    echo "💡 Více pomocí:"
    echo "   npm start --help"
else
    echo "❌ Chyba při nastavování Azure credentials"
    exit 1
fi
