#!/usr/bin/env python3

import torch
import torch.autograd as autograd
from torch.autograd import Variable
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np
import string

class RNN(nn.Module):

    def __init__(self, embedding_dim, hidden_dim, vocab_size, tagset_size):
        super().__init__()
        self.hidden_dim = hidden_dim
        self.word_embeddings = nn.Embedding(vocab_size, embedding_dim)
        self.lstm = nn.LSTM(embedding_dim, hidden_dim)
        self.hidden2tag = nn.Linear(hidden_dim, tagset_size)
        self.hidden = self.init_hidden()

    def init_hidden(self):
        return (Variable(torch.zeros(1,1,self.hidden_dim)), Variable(torch.zeros(1,1,self.hidden_dim)))

    def forward(self, sentence):
        embeds = self.word_embeddings(sentence)
        lstm_out, self.hidden = self.lstm(embeds.view(len(sentence), 1, -1), self.hidden)
        tag_space = self.hidden2tag(lstm_out.view(len(sentence), -1))
        tag_scores = F.log_softmax(tag_space, dim=1)
        return tag_scores

all_letters = string.printable
n_letters = len(all_letters)

class PrepareData():

    def __init__(self, filename, batch_size, val_ratio=0.):
        self.filename = filename
        self.batch_size = batch_size
        self.val_ratio = val_ratio

        self.load_dataset(filename, batch_size, val_ratio)

    def load_dataset(self, filename, batch_size, val_ratio=0.):
        with open(filename, 'r') as f:
            data = f.read()
        self.data = [data[i*batch_size:(i+1)*batch_size] for i in range(len(data)//batch_size)]
        self.shuffle_data()

    def shuffle_data(self):
        n_data = len(self.data)
        n_val = int(n_data * self.val_ratio)
        perm = np.random.permutation(n_data)

        self.train_data = [self.data[i] for i in perm[n_val:]]
        self.val_data = [self.data[i] for i in perm[:n_val]]

    def dataset(self):
        return self.train_data, self.val_data