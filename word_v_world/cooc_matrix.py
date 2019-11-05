import numpy as np
import sys
import pyprind

from cytoolz import itertoolz
from word_v_world import config, articles

# TODO - This writes an empty matrix and the progress bar doesn't work. Debug
# TODO - instead of a get file list, load in the tokenized file(s)


class CoocMatrix:

    def __init__(self, window_size, window_weight, window_type, vocab):
        self.corpus_name = None
        self.corpus_file_list = None

        self.window_size = window_size
        self.window_weight = window_weight
        self.window_type = window_type

        self.num_words = 0
        self.word_list = []
        self.w2id = {}
        self.id2w = {}

        self.pad = '*PAD*'
        self.verbose = False

        self.cooc_matrix = None

        for word in vocab:
            self.word_list.append(word)
            self.w2id[word] = self.num_words
            self.id2w[self.num_words] = word
            self.num_words += 1

        assert self.num_words > 0
        self.cooc_matrix = np.zeros([self.num_words, self.num_words], int)  # TODO needs to be sparse for wiki

    def update_from_file(self, param_name):
        with open(config.RemoteDirs.runs / param_name) as f:
            for line in f:
                tokens = line.strip('\n').split()  # convert string containing words into lsit of words
                # print(tokens)
                self.add_to_ww_matrix_fast(tokens)

    def update_from_list(self, tokens):
        self.add_to_ww_matrix_fast(tokens)

    def add_to_ww_matrix_fast(self, tokens):  # no function call overhead - twice as fast

            print('\nCounting word-word co-occurrences in {}-word moving window'.format(self.window_size))

            tokens += [self.pad] * self.window_size  # add padding such that all co-occurrences in last window are captured
            if self.verbose:
                print(tokens)
            windows = itertoolz.sliding_window(self.window_size + 1, tokens)  # + 1 because window consists of t2s only

            for w in windows:

                for t1, t2, dist in zip([w[0]] * self.window_size, w[1:], range(self.window_size)):
                    if t1 in self.w2id and t2 in self.w2id:

                        t1_id = self.w2id[t1]
                        t2_id = self.w2id[t2]
                        # increment
                        if t1_id == self.pad or t2_id == self.pad:
                            continue
                        if self.window_weight == "linear":
                            self.cooc_matrix[t1_id, t2_id] += self.window_size - dist
                        elif self.window_weight == "flat":
                            self.cooc_matrix[t1_id, t2_id] += 1
                        if self.verbose:
                            print('row {:>3} col {:>3} set to {}'.format(t1_id, t2_id, self.cooc_matrix[t1_id, t2_id]))

            if self.verbose:
                print()
            #pbar.update()
            # window_type
            if self.window_type == 'forward':
                self.cooc_matrix = self.cooc_matrix
            elif self.window_type == 'backward':
                self.cooc_matrix = self.cooc_matrix.transpose()
            elif self.window_type == 'summed':
                self.cooc_matrix = self.cooc_matrix + self.cooc_matrix.transpose()
            elif self.window_type == 'concatenated':
                self.cooc_matrix = np.concatenate((self.cooc_matrix, self.cooc_matrix.transpose()), axis=1)
            else:
                raise AttributeError('Invalid arg to "window_type".')
            print('Shape of normalized matrix={}'.format(self.cooc_matrix.shape))



