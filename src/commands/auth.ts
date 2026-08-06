import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { M365Auth } from '../auth.js';

export const authCommand = new Command('auth')
  .description('Správa Microsoft 365 ověření')
  .action(async () => {
    const auth = new M365Auth();
    const config = auth.loadConfig();

    if (config) {
      console.log(chalk.green('✓ Konfigurace existuje'));
      console.log(`  Client ID: ${config.clientId}`);
      console.log(`  Tenant ID: ${config.tenantId}`);
      console.log(`  Cesta: ${auth.getConfigPath()}`);
    } else {
      console.log(chalk.yellow('✗ Konfigurace nenalezena'));
      console.log('Spusťte: propoj auth setup');
    }
  });

authCommand
  .command('setup')
  .description('Nastavit Microsoft 365 ověření')
  .requiredOption('-c, --client-id <id>', 'Azure Client ID')
  .requiredOption('-t, --tenant-id <id>', 'Azure Tenant ID')
  .action((options) => {
    const spinner = ora('Ukládám konfiguraci...').start();
    const auth = new M365Auth(options.clientId, options.tenantId);
    auth.saveConfig(options.clientId, options.tenantId);
    spinner.succeed('Konfigurace uložena');
    console.log(chalk.green('✓ Microsoft 365 ověření je připraveno'));
    console.log('  Nyní můžete používat: propoj mail, propoj calendar, propoj sharepoint');
  });

authCommand
  .command('login')
  .description('Přihlásit se k Microsoft 365')
  .action(async () => {
    const auth = new M365Auth();
    const spinner = ora('Přihlašuji na Microsoft 365...').start();

    try {
      await auth.login();
      spinner.succeed('Úspěšně přihlášen');
      console.log(chalk.green('✓ Nyní máte přístup ke všem funkcím'));
    } catch (error) {
      spinner.fail('Chyba při přihlášení');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });
