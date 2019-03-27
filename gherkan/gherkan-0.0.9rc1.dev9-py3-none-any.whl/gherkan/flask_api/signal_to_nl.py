
import warnings

from gherkan.decoder.SignalParser import SignalParser
from gherkan.encoder.NLFileWriter import NLFileWriter


def process(input_file_path: str):
    """
    Processes a signals file and saves it as NL file.

    Parameters
    ----------
    input_file_path path to signals file

    """

    # TODO find a better way to do this
    if input_file_path.endswith("_signals.feature"):
        output_file = input_file_path.replace("_signals.feature", ".feature")
    else:
        warnings.warn("File does not end with '_signals.feature', saving the NL file as {}.plain"
                      .format(input_file_path))
        output_file = input_file_path + ".plain"

    # parse the signals file
    sp = SignalParser()
    signalBatch = sp.parseFile(input_file_path)

    # save the NL file
    nlFileWriter = NLFileWriter(signalBatch)
    nlFileWriter.write(output_file)