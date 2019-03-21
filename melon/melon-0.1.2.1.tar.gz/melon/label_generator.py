import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='%(name)-12s: %(levelname)-8s: %(message)s')
log = logging.getLogger(__name__)


class LabelGenerator:
    _default_labels_file_name = "labels.txt"

    @staticmethod
    def generate_labels(source_dir):
        labels_file = Path(source_dir) / LabelGenerator._default_labels_file_name
        if labels_file.exists():
            raise ValueError("Labels file already exists.")
        files = [f for f in os.listdir(source_dir) if os.path.isfile(os.path.join(source_dir, f)) and not f.startswith(".")]

        with open(str(labels_file), "w") as infile:
            infile.write("---\n")
            infile.write("#map\n")
            for f in files:
                file = Path(f)
                infile.write(file.name + ":\n")
        log.info("Generated labels file {} in '{}'".format(LabelGenerator._default_labels_file_name, source_dir))
