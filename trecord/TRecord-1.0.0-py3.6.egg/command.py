from trecord.database import Database
from trecord.error import TRecordError
from trecord.version import VERSION
from trecord.mysql import PyMySQL
from prompt_toolkit import PromptSession, print_formatted_text, HTML
from prompt_toolkit.styles import Style, style_from_pygments_cls, merge_styles
from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.sql import TransactSqlLexer
from pygments.styles.rainbow_dash import RainbowDashStyle
import sys
from tabulate import tabulate
from tablib import Dataset
import re
from trecord.keywords import COMMAND_KEYWORDS, SQL_KEYWORDS
from prompt_toolkit.completion import WordCompleter


class Command:
    """This class is an interactive command line client with Database"""
    def __init__(self, database: Database):
        self.database = database
        self.limit = 10
        self.message = None
        self.style = None
        self.setup_prompt()
        self.keywords = COMMAND_KEYWORDS + SQL_KEYWORDS + [k.lower() for k in SQL_KEYWORDS]
        self.session = PromptSession(style=self.style, lexer=PygmentsLexer(TransactSqlLexer),
                                     completer=WordCompleter(self.keywords), complete_while_typing=True)
        self.welcome()

    def welcome(self):
        print('Database {}'.format(self.database.get_version()))
        print('TRecord {}. Type "?" or "help" for help.'.format(VERSION))
        print()

    def set_limit(self, limit):
        self.limit = limit

    def setup_prompt(self):
        self.style = merge_styles([
            style_from_pygments_cls(RainbowDashStyle),

            Style.from_dict({
                'username': '#8dc3fc',
                'punctuation': '#090908',
                'host': '#8dc3fc',
                'database': '#aa83fc'
            })
        ])

        self.message = [
            ('class:username', self.database.database_url.username),
            ('class:punctuation', '@'),
            ('class:host', self.database.database_url.host),
            ('class:punctuation', ':'),
            ('class:database', self.database.get_current_db()),
            ('class:punctuation', '> '),
        ]

    @staticmethod
    def exit():
        print_formatted_text(HTML('<b>Quit.</b>'))
        sys.exit()

    def run_query_to_output(self, query):
        dataset = self.database.query(query, limit=self.limit)
        if dataset.height:
            print(tabulate(dataset, headers=dataset.headers, tablefmt='psql'))
            print('\n{} rows returned/limited'.format(dataset.height))
        else:
            print('no rows returned')

    @staticmethod
    def print_error(content):
        print_formatted_text(HTML('<red>{}</red>'.format(content)))

    @staticmethod
    def print_message(content):
        print_formatted_text(HTML('<green>{}</green>'.format(content)))

    def run_command(self, command: str):
        if command == '.quit':
            self.exit()
        elif command.startswith('.limit'):
            try:
                self.limit = int(re.split(r'\s+', command)[1])
            except (ValueError, IndexError):
                self.print_error('limit is required and needs to be an integer.')
        elif command.startswith('.tables'):
            database = None
            try:
                database = re.split(r'\s+', command)[1]
            except IndexError:
                pass

            for table in self.database.get_tables(database):
                print(table)
            print()
        elif command.startswith('.ddl'):
            try:
                arg = re.split(r'\s+', command)[1]
                table = arg
                database = None
                if '.' in arg:
                    database, table = arg.split('.')
                print(self.database.get_ddl(table, database))
                print()
            except IndexError:
                self.print_error('Table is required.')
        else:
            self.print_error('Command {} is not recognized'.format(command))

    @staticmethod
    def help():
        helps = Dataset()
        helps.headers = ['Input Form', 'Description']
        helps.append(['?', 'Print this help document.'])
        helps.append(['help', 'Print this help document.'])
        helps.append(['.limit <INTEGER>', 'Set the query limit.'])
        helps.append(['.tables [DATABASE]',
                      'Fetch the list of tables in current database or from the specified database.'])
        helps.append(['.ddl <[DATABASE.]TABLE>',
                      'Fetch the DDL of the table in current database or other if it is fully qualified.'])
        helps.append(['.quit', 'Quit.'])
        helps.append(['<QUERY>', 'Any SQL query.'])
        print(tabulate(helps, tablefmt='fancy_grid'))

    def loop(self):
        query_lines = []
        while True:
            try:
                this_line = self.session.prompt(self.message)
                this_line = this_line.strip()

                if this_line in ['help', '?']:
                    self.help()
                elif this_line.startswith('.'):
                    self.run_command(this_line)
                else:
                    query_lines.append(this_line)
                    if this_line.endswith(';'):
                        query = '\n'.join(query_lines).strip()
                        self.run_query_to_output(query)
                        query_lines = []

                        if query.lower().startswith('use'):  # reset the database at the prompt
                            self.setup_prompt()
            except TRecordError as err:
                query_lines = []
                self.print_error(err)
            except KeyboardInterrupt:
                query_lines = []
                self.print_message('Query input reset.')
            except EOFError:
                self.exit()


if __name__ == '__main__':
    # 'mysql+pymysql://lusaisai:lusaisai@198.58.115.91/employees'
    db = PyMySQL()
    db.connect(sys.argv[1])
    cmd = Command(db)
    cmd.loop()

