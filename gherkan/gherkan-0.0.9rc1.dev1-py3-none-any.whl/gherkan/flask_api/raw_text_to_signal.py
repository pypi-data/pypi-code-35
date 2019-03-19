from gherkan.decoder.NLParser import NLParser
from gherkan.encoder.RawNLParser import RawNLParser
from gherkan.encoder.SignalFileWriter import SignalFileWriter

def process(base_path: str, request: dict):
    """
    Processes raw text and saves two files - intermediate NL file (base_path.feature) and
    resulting signal file (base_path_signals.feature).

    Parameters
    ----------
    base_path : str
        path/to/files/file_basename

    request : dict
        dictionary with raw text
    """

    # create paths to files based on base_path
    nl_file_path = base_path + ".feature"
    signal_file_path = base_path + "_signals.feature"

    # parse the raw text
    parser = RawNLParser()
    parser.parse(request["text_raw"])
    request["background"] = parser.process_sentence(request["background"])
    parser.generate_program_dict()
    raw_text_lines = parser.get_text_lines()

    # create intermediate representation - text lines of the NL file
    lines = [
        "# language: {}".format(request["language"]),
        "Feature: {}".format(request["feature"]),
        "  {}".format(request["feature_desc"]),
        "Background:",
        "  {}".format(request["background"])
    ]
    lines += raw_text_lines

    # save the intermediate NL file
    with open(nl_file_path, "wt") as out:
        out.write("\n".join(lines))

    print("Saved NL file as {}".format(nl_file_path))

    # parse the NL text lines
    nl_parser = NLParser()
    nl_batch = nl_parser.parse(lines)

    # write the signal file
    signalFileWriter = SignalFileWriter(nl_batch)
    signalFileWriter.write(signal_file_path)

    print("Saved signals file as {}".format(signal_file_path))
