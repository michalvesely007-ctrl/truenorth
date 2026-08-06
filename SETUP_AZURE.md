# Nastavení Azure Credentials - Krok za Krokem

## Část 1: Registrace aplikace v Azure

### 1. Jdi na Azure Portal
Otevři https://portal.azure.com v prohlížeči a přihlaš se svým Microsoft účtem.

### 2. Vytvoř novou aplikaci
- Klikni na **Azure Active Directory** (vlevo v menu)
- Klikni na **App registrations**
- Klikni na **+ New registration**
- Vyplň:
  - **Name**: `ProPoj CLI`
  - **Supported account types**: `Accounts in this organizational directory only`
  - Klikni **Register**

### 3. Zkopíruj důležité identifikátory
Po vytvoření aplikace se otevře stránka s detaily. Zkopíruj si:
- **Application (client) ID** → ulož jako `CLIENT_ID`
- **Directory (tenant) ID** → ulož jako `TENANT_ID`

## Část 2: Nastavit oprávnění (Permissions)

### 4. Přidej API oprávnění
Na stránce aplikace:
- Klikni na **API permissions**
- Klikni na **+ Add a permission**
- Vyhledej a vyber **Microsoft Graph**
- Vyber **Delegated permissions** a přidej:
  - `Mail.Read`
  - `Mail.Send`
  - `Calendar.Read`
  - `Calendar.ReadWrite`
  - `Files.ReadWrite.All`
  - `User.Read`

- Klikni **Add permissions**

### 5. Souhlas správce (Admin consent)
- Na **API permissions** stránce klikni **Grant admin consent for...**
- Potvrd pomocí **Yes**

## Část 3: Nastavit autentizaci

### 6. Přidej Redirect URI
- Klikni na **Authentication**
- Klikni na **+ Add a platform**
- Vyber **Mobile and desktop applications**
- V Default redirect URIs by mělo být:
  - `https://login.microsoftonline.com/common/oauth2/nativeclient`
  - `http://localhost`
- Klikni **Configure**

## Část 4: Vytvoř Client Secret (volitelně)
Pokud chceš používat aplikaci z serveru:
- Klikni na **Certificates & secrets**
- Klikni na **+ New client secret**
- Nastav expiraci (např. 24 months)
- Klikni **Add**
- Zkopíruj hodnotu (ukazuje se jen jednou!)

## Část 5: Nastav CLI

Spusť tento příkaz s tvými hodnotami:

```bash
propoj auth setup --client-id "YOUR_CLIENT_ID" --tenant-id "YOUR_TENANT_ID"
```

Příklad:
```bash
propoj auth setup --client-id "a1b2c3d4-e5f6-7890-abcd-ef1234567890" --tenant-id "f1e2d3c4-b5a6-7890-1234-567890abcdef"
```

## Část 6: Přihlášení

Po nastavení credentials:
```bash
propoj auth login
```

Otevře se prohlížeč, kde se přihlaś svým Microsoft 365 účtem.

---

## Cheatsheet - Co kam jde:

| Kde v Azure | Co to je | Kam v CLI |
|---|---|---|
| Application (client) ID | Jedinečný ID aplikace | `--client-id` |
| Directory (tenant) ID | ID tvé organizace | `--tenant-id` |
| Client Secret | Heslo aplikace | V `auth.ts` |

## Zajímavé odkazy:
- [Azure Portal](https://portal.azure.com)
- [Azure AD dokumentace](https://docs.microsoft.com/en-us/azure/active-directory/)
- [Microsoft Graph API](https://graph.microsoft.com)

## Problémy?

**"Application does not have permission"** 
→ Jdi na API permissions a udělej Grant admin consent

**"Invalid tenant"**
→ Zkontroluj Directory (tenant) ID, ne Application ID

**"Redirect URI mismatch"**
→ Jdi na Authentication a přidej redirect URI
