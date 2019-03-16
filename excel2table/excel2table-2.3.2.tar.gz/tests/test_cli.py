import os
from mock import patch
from nose.tools import eq_
from excel2table.cli import cli
from click.testing import CliRunner


def test_cli():
    runner = CliRunner()

    result = runner.invoke(cli, ['sample/goog.ods', 'goog.html'])
    eq_(result.exit_code, 0)
    os.unlink('goog.html')


@patch('click.getchar')
def test_cli_prompt(fake_getchar):
    fake_getchar.return_value = 'y'
    runner = CliRunner()

    result = runner.invoke(cli, ['sample/goog.ods', 'goog.html'])
    result = runner.invoke(cli, ['sample/goog.ods', 'goog.html'])
    eq_(result.exit_code, 0)
    os.unlink('goog.html')


def test_vs():
    runner = CliRunner()

    result = runner.invoke(cli, ['-vs', '100', 'sample/goog.ods', 'goog.html'])
    eq_(result.exit_code, 0)
    os.unlink('goog.html')


def test_vs_disabled():
    runner = CliRunner()

    result = runner.invoke(cli, ['-vs', '-1', 'sample/goog.ods', 'goog.html'])
    eq_(result.exit_code, 0)
    os.unlink('goog.html')


@patch('webbrowser.open')
@patch('time.sleep', side_effect=KeyboardInterrupt())
def test_serve(fake_time, fake_webbrowser):
    runner = CliRunner()

    result = runner.invoke(cli, ['-s', 'sample/goog.ods'])
    eq_(result.exit_code, 0)
