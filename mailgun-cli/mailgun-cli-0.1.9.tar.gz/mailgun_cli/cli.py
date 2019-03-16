import click
import pandas as pd

from mailgun_cli.forward import update_from_csv
from mailgun_cli.mailgun import Mailgun


@click.group()
def main():
    pass

@click.command()
def routes():
    """list all routes"""
    api = Mailgun()
    df = pd.DataFrame(api.list_routes()['items'])
    print(df)

@click.command()
@click.argument("url")
def forward(url):
    """create 1-to-1 forward mail route using a csv"""
    update_from_csv(url)


main.add_command(routes)
main.add_command(forward)

if __name__ == '__main__':
    main()
