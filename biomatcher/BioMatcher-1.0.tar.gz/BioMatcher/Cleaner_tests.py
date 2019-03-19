from Cleaner import cleaning
import click
from click.testing import CliRunner
import os
import Exceptions as exc


@click.command()
def test():
    runner = CliRunner()
    result = runner.invoke(cleaning, ['-m', 'mature_plant_reduced.fa'])
    assert result.exit_code == 0

    result = runner.invoke(cleaning, [])
    assert result.exit_code == 2

    result = runner.invoke(cleaning, ['-m', 'mature_plant_test_noredund.fa', '-r', 'CL03.csv'])
    assert not os.path.exists('CL03.csv')

    result = runner.invoke(cleaning, ['-m', 'mature_plant_reduced.fa', '-e', 'CL04.fa'])
    assert not os.path.exists('CL04.fa')

    result = runner.invoke(cleaning, ['-m', 'README.md'])
    assert type(result.exception) == exc.ErrorInFileException

    result = runner.invoke(cleaning, ['-m', 'mature_plant_test_cleaner.fa', '-e', 'CL06.fa'])
    assert len(open("CL06.fa").readlines())/2 == 3

    result = runner.invoke(cleaning, ['-m', 'mature_plant_test_cleaner.fa', '-r', 'CL07.csv'])
    assert (open("CL07.csv").readlines())[1] == "MIMAT0016323,MIMAT0016326|MIMAT0016330\n"

    result = runner.invoke(cleaning, ['-m', 'mature_plant_cleaned.fa', '-o', 'CL08_cleaned.fa', '-r', 'CL08.csv',
                                      '-e', 'CL08.fa'])
    assert not os.path.exists('CL08.fa')
    assert not os.path.exists('CL08.csv')


if __name__ == '__main__':
    test()
