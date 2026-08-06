#!/usr/bin/env node

import { program } from 'commander';
import { mailCommand } from './commands/mail.js';
import { calendarCommand } from './commands/calendar.js';
import { sharepointCommand } from './commands/sharepoint.js';
import { authCommand } from './commands/auth.js';

program
  .name('propoj')
  .description('Microsoft 365 CLI tool - Přístup k mailu, kalendáři, SharePointu a dalšímu')
  .version('1.0.0');

program.addCommand(authCommand);
program.addCommand(mailCommand);
program.addCommand(calendarCommand);
program.addCommand(sharepointCommand);

program.parse(process.argv);

if (!process.argv.slice(2).length) {
  program.outputHelp();
}
