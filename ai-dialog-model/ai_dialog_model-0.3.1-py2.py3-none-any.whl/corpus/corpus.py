from ai_dialog_model.processing.utilities import download_corpus


class Corpus:
    def __init__(self, corpus_name, download_path, url):
        self.corpus_name = corpus_name
        self.download_path = download_path
        self.url = url
        self.voc = {}
        self.pairs = {}

