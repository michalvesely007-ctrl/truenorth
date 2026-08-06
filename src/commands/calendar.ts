import { Command } from 'commander';
import chalk from 'chalk';
import ora from 'ora';
import { table } from 'table';
import { GraphClient } from '../graph.js';

export const calendarCommand = new Command('calendar')
  .description('Správa kalendáře');

calendarCommand
  .command('events')
  .option('-d, --days <number>', 'Počet dnů k zobrazení', '7')
  .description('Zobrazit nadcházející události')
  .action(async (options) => {
    const spinner = ora('Načítám kalendář...').start();

    try {
      const graph = new GraphClient();
      const events = await graph.getCalendarEvents(parseInt(options.days));

      spinner.stop();

      if (!events.value || events.value.length === 0) {
        console.log(chalk.yellow('Žádné nadcházející události'));
        return;
      }

      const data = [
        [chalk.bold('Událost'), chalk.bold('Začátek'), chalk.bold('Konec'), chalk.bold('Organizátor')],
        ...events.value.map((event: any) => [
          event.subject || '(bez názvu)',
          new Date(event.start.dateTime).toLocaleString('cs-CZ'),
          new Date(event.end.dateTime).toLocaleString('cs-CZ'),
          event.organizer?.emailAddress?.name || 'N/A',
        ]),
      ];

      console.log(table(data));
    } catch (error) {
      spinner.fail('Chyba při načítání kalendáře');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });

calendarCommand
  .command('create')
  .requiredOption('-s, --subject <text>', 'Název události')
  .requiredOption('--start <datetime>', 'Čas zahájení (ISO 8601)')
  .requiredOption('--end <datetime>', 'Čas ukončení (ISO 8601)')
  .option('-a, --attendees <emails...>', 'E-mailové adresy účastníků (volitelné)')
  .description('Vytvořit novou událost v kalendáři')
  .action(async (options) => {
    const spinner = ora('Vytvářím událost...').start();

    try {
      const graph = new GraphClient();
      const startTime = new Date(options.start);
      const endTime = new Date(options.end);

      if (isNaN(startTime.getTime()) || isNaN(endTime.getTime())) {
        spinner.fail('Neplatný formát data/času');
        console.error(chalk.red('Použijte formát ISO 8601: 2024-12-25T14:30:00'));
        process.exit(1);
      }

      await graph.createCalendarEvent(options.subject, startTime, endTime, options.attendees);

      spinner.succeed('Událost vytvořena');
      console.log(chalk.green(`✓ ${options.subject}`));
      console.log(`  Začátek: ${startTime.toLocaleString('cs-CZ')}`);
      console.log(`  Konec: ${endTime.toLocaleString('cs-CZ')}`);
      if (options.attendees && options.attendees.length > 0) {
        console.log(`  Účastníci: ${options.attendees.join(', ')}`);
      }
    } catch (error) {
      spinner.fail('Chyba při vytváření události');
      console.error(chalk.red(String(error)));
      process.exit(1);
    }
  });
