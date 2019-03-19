import os

from ai_dialog_model.corpus.corpus import Corpus
from ai_dialog_model.processing.utilities import load_lines, load_conversations, write_formatted_data, \
    download_corpus
from ai_dialog_model.processing.voc_pairs import trim_rare_words, load_prepare_data


class CornellCorpus(Corpus):

    def __init__(self, save_dir):
        self.save_dir = os.path.join(save_dir)
        corpus_name = "cornell movie-dialogs corpus"
        Corpus.__init__(
            self,
            corpus_name,
            '/tmp/' + corpus_name,
            'http://www.cs.cornell.edu/~cristian/data/cornell_movie_dialogs_corpus.zip'
        )
        self.corpus_path = download_corpus(
            self.url,
            self.download_path,
            self.corpus_name
        )

    def processing_corpus(self):
        # Define path to new file
        datafile = os.path.join(self.corpus_path, "formatted_movie_lines.txt")
        print("\nProcessing corpus...")
        lines = load_lines(os.path.join(self.corpus_path, "movie_lines.txt"))
        print("\nLoading conversations...")
        conversations = load_conversations(os.path.join(self.corpus_path, "movie_conversations.txt"), lines)
        # Load/Assemble voc and pairs
        write_formatted_data(datafile, conversations)
        self.voc, self.pairs = load_prepare_data(self.corpus_name, datafile)

        # Trim voc and pairs
        self.pairs = trim_rare_words(self.voc, self.pairs)
