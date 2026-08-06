import fs from 'fs';
import path from 'path';
import os from 'os';

const CONFIG_DIR = path.join(os.homedir(), '.propoj');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');

interface AuthConfig {
  clientId: string;
  tenantId: string;
  clientSecret?: string;
}

export class M365Auth {
  private config: AuthConfig;

  constructor(clientId?: string, tenantId?: string) {
    this.config = {
      clientId: clientId || 'YOUR_CLIENT_ID',
      tenantId: tenantId || 'common',
    };
  }

  async login(scopes: string[] = ['https://graph.microsoft.com/.default']): Promise<string> {
    try {
      console.log('Přihlašovací URL:');
      console.log(`https://login.microsoftonline.com/${this.config.tenantId}/oauth2/v2.0/authorize?client_id=${this.config.clientId}&scope=${encodeURIComponent(scopes.join(' '))}&response_type=code`);
      return 'token';
    } catch (error) {
      throw new Error(`Chyba při přihlášení: ${error}`);
    }
  }

  saveConfig(clientId: string, tenantId: string): void {
    if (!fs.existsSync(CONFIG_DIR)) {
      fs.mkdirSync(CONFIG_DIR, { recursive: true });
    }

    fs.writeFileSync(
      CONFIG_FILE,
      JSON.stringify({ clientId, tenantId }, null, 2)
    );
  }

  loadConfig(): AuthConfig | null {
    if (fs.existsSync(CONFIG_FILE)) {
      const data = fs.readFileSync(CONFIG_FILE, 'utf-8');
      return JSON.parse(data);
    }
    return null;
  }

  getConfigPath(): string {
    return CONFIG_FILE;
  }
}
