from Filter import filtering
import click
from click.testing import CliRunner
import Exceptions as exc


@click.command()
def test():
    runner = CliRunner()
    result = runner.invoke(filtering, ['-m', 'mature_plant_reduced.fa', '-s', 'jsonspecies.json'])
    assert result.exit_code == 0

    result = runner.invoke(filtering, ['-m', 'mature_plant_reduced.fa', '-s', 'jsonspecies_empty.json'])
    assert type(result.exception) == exc.NoSpeciesSelectException

    result = runner.invoke(filtering, ['-m', 'mature_plant_reduced.fa'])
    assert result.exit_code == 2

    result = runner.invoke(filtering, ['-m', 'mature_plant_reduced.fa', '-s', 'jsonspecies_error.json'])
    assert type(result.exception) == exc.ErrorInFileException

    result = runner.invoke(filtering, ['-m', 'mature_plant_reduced.fa', '-s', 'jsonspecies.json'])
    assert len(open("mature_plant_filtered.fa").readlines())/2 == 42


if __name__ == '__main__':
    test()
