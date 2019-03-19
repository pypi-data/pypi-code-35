import torch
from torch import nn

from ai_dialog_model.models.seq2seq.encoder import EncoderRNN
from ai_dialog_model.models.seq2seq.evaluation.evaluate import evaluateInput
from ai_dialog_model.models.seq2seq.evaluation.greedy_search_decoder import GreedySearchDecoder
from ai_dialog_model.models.seq2seq.luong_attn_decoder import LuongAttnDecoderRNN
from torch import optim

from ai_dialog_model.models.seq2seq.train import trainIters


class Seq2Seq:
    def __init__(self, device, corpus,  load_filename=None):
        self.corpus = corpus
        self.device = device
        # Configure models
        self.model_name = 'cb_model'
        self.attn_model = 'dot'
        # attn_model = 'general'
        # attn_model = 'concat'
        self.hidden_size = 500
        self.encoder_n_layers = 2
        self.decoder_n_layers = 2
        self.dropout = 0.1
        self.batch_size = 32
        # Set checkpoint to load from; set to None if starting from scratch
        self.loadFilename = load_filename
        self.checkpoint_iter = 4000
        self.checkpoint = {}
        self.embedding_sd = {}
        self.encoder_sd = {}
        self.decoder_sd = {}
        self.encoder_optimizer_sd = {}
        self.decoder_optimizer_sd = {}
        self. encoder = {}
        self.decoder = {}
        self.embedding = {}

    def build(self):
        # Load model if a loadFilename is provided
        if self.loadFilename:
            # If loading on same machine the model was trained on
            checkpoint = torch.load(self.loadFilename)
            # If loading a model trained on GPU to CPU
            # checkpoint = torch.load(loadFilename, map_location=torch.device('cpu'))
            self.encoder_sd = checkpoint['en']
            self.decoder_sd = checkpoint['de']
            self.encoder_optimizer_sd = checkpoint['en_opt']
            self.decoder_optimizer_sd = checkpoint['de_opt']
            self.embedding_sd = checkpoint['embedding']
            self.corpus.voc.__dict__ = checkpoint['voc_dict']

        print('Building encoder and decoder ...')
        # Initialize word embeddings
        self.embedding = nn.Embedding(self.corpus.voc.num_words, self.hidden_size)
        if self.loadFilename:
            self.embedding.load_state_dict(self.embedding_sd)
        # Initialize encoder & decoder models
        self.encoder = EncoderRNN(self.hidden_size, self.embedding, self.encoder_n_layers, self.dropout)
        self.decoder = LuongAttnDecoderRNN(self.attn_model, self.embedding, self.hidden_size, self.corpus.voc.num_words, self.decoder_n_layers, self.dropout)
        if self.loadFilename:
            self.encoder.load_state_dict(self.encoder_sd)
            self.decoder.load_state_dict(self.decoder_sd)
        # Use appropriate device
        self.encoder = self.encoder.to(self.device)
        self.decoder = self.decoder.to(self.device)
        print('Models built and ready to go!')

    def train(self):
        # Configure training/optimization
        clip = 50.0
        teacher_forcing_ratio = 1.0
        learning_rate = 0.0001
        decoder_learning_ratio = 5.0
        n_iteration = 4000
        print_every = 1
        save_every = 500

        # Ensure dropout layers are in train mode
        self.encoder.train()
        self.decoder.train()

        # Initialize optimizers
        print('Building optimizers ...')
        encoder_optimizer = optim.Adam(self.encoder.parameters(), lr=learning_rate)
        decoder_optimizer = optim.Adam(self.decoder.parameters(), lr=learning_rate * decoder_learning_ratio)
        if self.loadFilename:
            encoder_optimizer.load_state_dict(self.encoder_optimizer_sd)
            decoder_optimizer.load_state_dict(self.decoder_optimizer_sd)

        # Run training iterations
        print("Starting Training!")
        trainIters(self.model_name, self.corpus.voc, self.corpus.pairs, self.encoder, self.decoder, encoder_optimizer,
                   decoder_optimizer, self.embedding, self.encoder_n_layers, self.decoder_n_layers, self.corpus.save_dir, n_iteration,
                   self.batch_size, print_every, save_every, clip, self.corpus.corpus_name,
                   self.loadFilename, teacher_forcing_ratio, self.checkpoint, self.hidden_size)

    def chat(self):
        # Set dropout layers to eval mode
        self.encoder.eval()
        self.decoder.eval()
        # Initialize search module
        searcher = GreedySearchDecoder(self.encoder, self.decoder)

        # Begin chatting (uncomment and run the following line to begin)
        evaluateInput(self.encoder, self.decoder, searcher, self.corpus.voc)

