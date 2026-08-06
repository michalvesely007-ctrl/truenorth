# Propoj CLI - Microsoft 365 Command Line Tool

Propoj CLI je moderní nástroj příkazového řádku pro interakci s Microsoft 365 službami včetně Outlooku (e-mailu), Kalendáře, SharePointu a OneDrive.

## Instalace

```bash
npm install
npm run build
npm start
```

Nebo přímo spusťte CLI:

```bash
node dist/cli.js
```

## Nastavení

### 1. Zaregistrujte aplikaci v Azure

1. Jděte na [Azure Portal](https://portal.azure.com)
2. Vyberte **Azure Active Directory** → **App registrations**
3. Klikněte na **New registration**
4. Zadejte název aplikace a zaregistrujte ji
5. Zkopírujte **Client ID** a **Tenant ID**

### 2. Nakonfigurujte CLI

```bash
propoj auth setup --client-id <YOUR_CLIENT_ID> --tenant-id <YOUR_TENANT_ID>
```

### 3. Přihlaste se

```bash
propoj auth login
```

## Příkazy

### E-mail (Mail)

**Zobrazit doručené zprávy:**
```bash
propoj mail inbox
propoj mail inbox --top 20  # Zobrazit posledních 20 e-mailů
```

**Poslat e-mail:**
```bash
propoj mail send --to user@example.com --subject "Předmět" --body "Obsah zprávy"
```

**Vyhledat e-maily:**
```bash
propoj mail search --query "klíčové slovo"
```

### Kalendář

**Zobrazit nadcházející události:**
```bash
propoj calendar events
propoj calendar events --days 30  # Zobrazit následujících 30 dní
```

**Vytvořit událost:**
```bash
propoj calendar create \
  --subject "Schůzka" \
  --start 2024-12-25T14:00:00 \
  --end 2024-12-25T15:00:00 \
  --attendees user1@example.com user2@example.com
```

### SharePoint & OneDrive

**Zobrazit SharePoint stránky:**
```bash
propoj sharepoint sites
```

**Zobrazit soubory:**
```bash
propoj sharepoint files --site <SITE_ID> --drive <DRIVE_ID>
```

**Nahrát soubor:**
```bash
propoj sharepoint upload --file ./local-file.pdf --drive <DRIVE_ID>
propoj sharepoint upload --file ./local-file.pdf --drive <DRIVE_ID> --name "remote-name.pdf"
```

### Ověření

**Zkontrolovat konfiguraci:**
```bash
propoj auth
```

**Provést nové přihlášení:**
```bash
propoj auth login
```

## Struktura projektu

```
.
├── src/
│   ├── cli.ts              # Hlavní CLI entry point
│   ├── auth.ts             # Správa ověření
│   ├── graph.ts            # Microsoft Graph API client
│   └── commands/
│       ├── auth.ts         # Ověřovací příkazy
│       ├── mail.ts         # E-mailové příkazy
│       ├── calendar.ts     # Kalendářové příkazy
│       └── sharepoint.ts   # SharePoint příkazy
├── dist/                   # Kompilovaný JavaScript
├── package.json
├── tsconfig.json
└── README.md
```

## Použité technologie

- **TypeScript** - Typově bezpečný JavaScript
- **Commander.js** - CLI framework
- **Microsoft Graph SDK** - Pro komunikaci s Microsoft 365
- **Azure Identity** - Ověřování
- **Chalk** - Barevný výstup
- **Ora** - Loading spinners
- **Table** - Formátování tabulek

## Licencia

MIT

## Autor

Michal Vesely
