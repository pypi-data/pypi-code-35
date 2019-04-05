# -*- coding: utf-8 -*-

"""Console script for fast-datacard."""
import sys
import click
from . import dataframe_to_datacard_cfg


@click.command()
@click.argument('yaml_config')
def main(yaml_config):
    """Console script for fast-datacard."""
    return dataframe_to_datacard_cfg.main(yaml_config)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
