# -*- coding: utf-8 -*-
import torch

from .corpus.parse_cornell_corpus import CornellCorpus
from .models.seq2seq.seq2seq_model import Seq2Seq


def train_cornell_seq2seq_chitchat(save_dir='data'):

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    cornell = CornellCorpus(save_dir)
    cornell.processing_corpus()
    seq2seq = Seq2Seq(device, cornell)
    seq2seq.build()
    seq2seq.train()
    return seq2seq


def use_trained_cornell_seq2seq_chitchat(save_dir):

    use_cuda = torch.cuda.is_available()
    device = torch.device("cuda" if use_cuda else "cpu")

    cornell = CornellCorpus(save_dir)
    cornell.processing_corpus()
    seq2seq = Seq2Seq(device, cornell, save_dir)
    seq2seq.build()
    return seq2seq


"""Top-level package for nlg-deeppavlov-api."""

__author__ = """Simon Meoni"""
__email__ = '2426884M@student.gla.ac.uk'
__version__ = '0.1.0'
