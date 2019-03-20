import codecs
import os


def write_file(output_file_path, content):
    validate_out_dir(output_file_path)

    with codecs.open(output_file_path, 'w', encoding="utf-8") as f:
        return f.write(content)


def validate_out_dir(output_file_path):
    target_dir = os.path.dirname(output_file_path)
    if not os.path.isdir(target_dir):
        raise ValueError("Target dir does not exist: {}".format(target_dir))
