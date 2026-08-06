# Propoj CLI - Microsoft 365 Command Line Tool

Propoj CLI je moderní nástroj příkazového řádku pro interakci s Microsoft 365 službami včetně Outlooku (e-mailu), Kalendáře, SharePointu a OneDrive.

## Rychlé Nastavení (5 minut)

### Pro Linux/Mac:
```bash
bash setup.sh
```

### Pro Windows (PowerShell):
```powershell
.\setup.ps1
```

Skript tě provede celým nastavením! 🎉

---

## Instalace (Manuálně)

```bash
npm install
npm run build
npm start
```

Nebo přímo spusťte CLI:

```bash
node dist/cli.js
```

## Nastavení Azure (Detailní Návod)

👉 **Čti [SETUP_AZURE.md](./SETUP_AZURE.md)** pro krok za krokem instrukce

Nebo stručně:

### 1. Zaregistruj aplikaci v Azure

1. Jdi na [Azure Portal](https://portal.azure.com)
2. Vyber **Azure Active Directory** → **App registrations**
3. Klikni na **+ New registration**
4. Pojmenuj ji `ProPoj CLI` a zaregistruj
5. Zkopíruj **Application (client) ID** a **Directory (tenant) ID**

### 2. Přidej oprávnění (API Permissions)

Přidej tyto oprávnění pro Microsoft Graph:
- `Mail.Read`, `Mail.Send`
- `Calendar.Read`, `Calendar.ReadWrite`
- `Files.ReadWrite.All`
- `User.Read`

### 3. Nastav CLI

```bash
npx propoj auth setup --client-id "<YOUR_CLIENT_ID>" --tenant-id "<YOUR_TENANT_ID>"
```

### 4. Přihlaš se

```bash
npx propoj auth login
```

Otevře se prohlížeč pro přihlášení.

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
