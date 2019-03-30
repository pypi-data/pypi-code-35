from typing import List

import click

from tdameritrade_cli.tools.client_factory import ClientFactory
from tdameritrade_cli.tools.positions import get_positions
from tdameritrade_cli.tools.ods_writer import ODSWriter


@click.group(help='CLI to use the TDA API. Before calling a subcommand, you must provide sufficient authentication '
                  'information. This can be done with the -a and -o options, or else by writing a separate json file '
                  'pointed to by -j. The file should contain acct_number, oauth_user_id, and redirect_uri keys with an '
                  'optional token_path. See the docs for TDClient for more information.')
@click.pass_context
@click.option('--json-config', '-j', type=click.Path(exists=True),
              help='Path to a json object with configuration options. Supercedes other options.')
@click.option('--acct-number', '-a', type=int, help='Account number of TDA account to link through.')
@click.option('--oauth-user-id', '-o', help='OAuth user ID for the TDA app you are using to access the API.')
@click.option('--redirect-uri', '-r', default='http://127.0.0.1:8080',
              help='Redirect URI for the TDA app you are using to access the API.')
def driver(ctx, json_config, acct_number, oauth_user_id, redirect_uri):
    def _client_factory():
        factory = ClientFactory(json_config, acct_number, oauth_user_id,
                                redirect_uri)
        if json_config is not None:
            client = factory.from_json()
        else:
            client = factory.from_config()

        return client
    ctx.obj = {
        'CLIENT_FACTORY': _client_factory
    }


@driver.command(name='list-positions', help='Print the positions data for the specified account.')
@click.pass_context
def list_positions_cli(ctx):
    client = ctx.obj['CLIENT_FACTORY']()
    liq_value, acct_positions = get_positions(client)

    click.echo(prettify_output(['Identifier', 'Asset Type', 'Market Value']))
    for pos in acct_positions:
        formatted_pos = prettify_output(pos)
        click.echo(formatted_pos)
    click.echo(f'Liquidation value: {liq_value}')


@driver.command(name='write-positions', help='Write the current positions data to an ods file at SHEET_PATH.')
@click.pass_context
@click.argument('sheet-path', type=click.Path())
def write_positions_cli(ctx, sheet_path):
    client = ctx.obj['CLIENT_FACTORY']()
    liq_value, acct_positions = get_positions(client)
    ods_writer = ODSWriter(sheet_path)
    ods_writer.write_positions(liq_value, acct_positions)


def prettify_output(output: List[str]) -> str:
    formatted = f''
    for item in output:
        formatted += f'{item:<20}    '
    return formatted


if __name__ == '__main__':
    driver()
