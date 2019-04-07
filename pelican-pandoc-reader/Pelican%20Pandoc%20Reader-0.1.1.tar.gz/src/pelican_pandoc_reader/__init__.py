import json
from pathlib import Path

import pypandoc
from pelican import signals
from pelican.readers import BaseReader
from pelican.utils import pelican_open
from pkg_resources import DistributionNotFound, get_distribution

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    pass


class PandocReader(BaseReader):
    enabled = True
    file_extensions = ["md", "markdown", "mkd", "mdown"]
    output_format = "html5"

    template_path = Path(__file__).parents[0] / "metadata.template"

    def read(self, path):
        # Read the meta data
        metadata = self.read_metadata(path)

        # Read the settings
        extra_args, filters = self.read_settings()

        # Convert the file with Pandoc
        output = pypandoc.convert_file(
            path, to=self.output_format, extra_args=extra_args, filters=filters
        )
        output = output.replace("%7Bfilename%7D", "{filename}")

        return output, metadata

    def read_metadata(self, path):
        raw_metadata = pypandoc.convert_file(
            path, to=self.output_format, extra_args=["--template", self.template_path]
        )
        raw_metadata = json.loads(raw_metadata)

        return {
            key: self.process_metadata(key, value)
            for key, value in raw_metadata.items()
        }

    def read_settings(self):
        extra_args = self.settings.get("PANDOC_ARGS", [])
        filters = self.settings.get("PANDOC_EXTENSIONS", [])
        return extra_args, filters


def add_reader(readers):
    for ext in PandocReader.file_extensions:
        readers.reader_classes[ext] = PandocReader


def register():
    signals.readers_init.connect(add_reader)
