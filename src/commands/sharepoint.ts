import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { table } from 'table';
import fs from 'fs';
import { GraphClient } from '../graph.js';

export const sharepointCommand = new Command('sharepoint')
  .description('Správa SharePointu a OneDrive');

sharepointCommand
  .command('sites')
  .description('Zobrazit dostupné SharePoint stránky')
  .action(async () => {
    const spinner = ora('Načítám SharePoint stránky...').start();

    try {
      const graph = new GraphClient();
      const sites = await graph.getSharePointSites();

      spinner.stop();

      if (!sites.value || sites.value.length === 0) {
        console.log(chalk.yellow('Žádné SharePoint stránky nenalezeny'));
        return;
      }

      const data = [
        [chalk.bold('Název'), chalk.bold('ID'), chalk.bold('URL')],
        ...sites.value.map((site: any) => [
          site.displayName || site.name || 'N/A',
          site.id,
          site.webUrl || 'N/A',
        ]),
      ];

      console.log(table(data));
    } catch (error) {
      spinner.fail('Chyba při načítání SharePoint stránek');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });

sharepointCommand
  .command('files')
  .requiredOption('-s, --site <id>', 'SharePoint Site ID')
  .requiredOption('-d, --drive <id>', 'Drive ID')
  .description('Zobrazit soubory v SharePoint/OneDrive')
  .action(async (options) => {
    const spinner = ora('Načítám soubory...').start();

    try {
      const graph = new GraphClient();
      const files = await graph.getSharePointFiles(options.site, options.drive);

      spinner.stop();

      if (!files.value || files.value.length === 0) {
        console.log(chalk.yellow('Žádné soubory nenalezeny'));
        return;
      }

      const data = [
        [chalk.bold('Název'), chalk.bold('Typ'), chalk.bold('Velikost'), chalk.bold('Poslední úprava')],
        ...files.value.map((file: any) => [
          file.name || 'N/A',
          file.folder ? '📁 Složka' : '📄 Soubor',
          file.size ? `${(file.size / 1024 / 1024).toFixed(2)} MB` : 'N/A',
          new Date(file.modifiedDateTime).toLocaleString('cs-CZ'),
        ]),
      ];

      console.log(table(data));
    } catch (error) {
      spinner.fail('Chyba při načítání souborů');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });

sharepointCommand
  .command('upload')
  .requiredOption('-f, --file <path>', 'Cesta k souboru k nahrání')
  .requiredOption('-d, --drive <id>', 'Drive ID')
  .option('-n, --name <filename>', 'Jméno souboru v OneDrive (volitelné)')
  .description('Nahrát soubor na OneDrive/SharePoint')
  .action(async (options) => {
    const spinner = ora('Kontroluji soubor...').start();

    try {
      if (!fs.existsSync(options.file)) {
        spinner.fail('Soubor nenalezen');
        console.error(chalk.red(`Soubor neexistuje: ${options.file}`));
        process.exit(1);
      }

      spinner.text = 'Nahrávám soubor...';

      const fileContent = fs.readFileSync(options.file);
      const fileName = options.name || require('path').basename(options.file);

      const graph = new GraphClient();
      await graph.uploadFile(options.drive, fileName, fileContent);

      spinner.succeed('Soubor úspěšně nahrán');
      console.log(chalk.green(`✓ ${fileName}`));
      console.log(`  Velikost: ${(fileContent.length / 1024 / 1024).toFixed(2)} MB`);
    } catch (error) {
      spinner.fail('Chyba při nahrávání souboru');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });
