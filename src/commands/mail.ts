import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { table } from 'table';
import { GraphClient } from '../graph.js';

export const mailCommand = new Command('mail')
  .description('Správa e-mailu (Outlook)');

mailCommand
  .command('inbox')
  .option('-t, --top <number>', 'Počet e-mailů k zobrazení', '10')
  .description('Zobrazit e-maily v doručené poště')
  .action(async (options) => {
    const spinner = ora('Načítám e-maily...').start();

    try {
      const graph = new GraphClient();
      const mails = await graph.getMails(parseInt(options.top));

      spinner.stop();

      if (!mails.value || mails.value.length === 0) {
        console.log(chalk.yellow('Žádné e-maily nenalezeny'));
        return;
      }

      const data = [
        [chalk.bold('Předmět'), chalk.bold('Od'), chalk.bold('Datum'), chalk.bold('Příloha')],
        ...mails.value.map((mail: any) => [
          mail.subject || '(bez předmětu)',
          mail.from?.emailAddress?.name || 'N/A',
          new Date(mail.receivedDateTime).toLocaleString('cs-CZ'),
          mail.hasAttachments ? '✓' : '',
        ]),
      ];

      console.log(table(data));
    } catch (error) {
      spinner.fail('Chyba při načítání e-mailů');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });

mailCommand
  .command('send')
  .requiredOption('-t, --to <email>', 'Příjemce (e-mailová adresa)')
  .requiredOption('-s, --subject <text>', 'Předmět e-mailu')
  .requiredOption('-b, --body <text>', 'Obsah e-mailu')
  .description('Poslat e-mail')
  .action(async (options) => {
    const spinner = ora('Odesílám e-mail...').start();

    try {
      const graph = new GraphClient();
      await graph.sendMail(options.to, options.subject, options.body);

      spinner.succeed('E-mail úspěšně odeslán');
      console.log(chalk.green(`✓ Příjemce: ${options.to}`));
      console.log(`  Předmět: ${options.subject}`);
    } catch (error) {
      spinner.fail('Chyba při odesílání e-mailu');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });

mailCommand
  .command('search')
  .requiredOption('-q, --query <text>', 'Vyhledávací dotaz')
  .description('Vyhledat e-maily')
  .action(async (options) => {
    const spinner = ora('Vyhledávám e-maily...').start();

    try {
      const graph = new GraphClient();
      const client = graph.getClient();
      const results = await client
        .api('/me/mailFolders/inbox/messages')
        .filter(`contains(subject,'${options.query}') or contains(from/emailAddress/address,'${options.query}')`)
        .select(['subject', 'from', 'receivedDateTime'])
        .top(20)
        .get();

      spinner.stop();

      if (!results.value || results.value.length === 0) {
        console.log(chalk.yellow(`Žádné e-maily pro dotaz "${options.query}" nenalezeny`));
        return;
      }

      const data = [
        [chalk.bold('Předmět'), chalk.bold('Od'), chalk.bold('Datum')],
        ...results.value.map((mail: any) => [
          mail.subject || '(bez předmětu)',
          mail.from?.emailAddress?.name || 'N/A',
          new Date(mail.receivedDateTime).toLocaleString('cs-CZ'),
        ]),
      ];

      console.log(table(data));
    } catch (error) {
      spinner.fail('Chyba při vyhledávání');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });
