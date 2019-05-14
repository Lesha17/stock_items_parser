import pandas as pd
import random
import torch

class GoodsDataset:
    def __init__(self, max_seq_size):
        
        self.SOSTOKEN_i = 0
        self.SOSTOKEN_c = '?'
        self.EOSTOKEN_i = 1
        self.EOSTOKEN_c = '!'
        
        self.max_seq_length = max_seq_size
        
        self.load_data()
        self.build_vocab()

        
        
    def load_data(self):
        self.data = pd.read_csv('example1.csv', sep='\t')
        self.data.dropna(subset=['target'], inplace=True)
        self.text = list(self.data['text'])
        self.target = list(map(str, self.data['target']))
    
    def build_vocab(self):
        self.charset = set()
        for i in range(len(self.text)):
            self.charset |= set(self.text[i])
            self.charset |= set(self.target[i])
        self.charset = list(self.charset)
        
        self.charset = [self.SOSTOKEN_c, self.EOSTOKEN_c] + self.charset
        self.char_vocab_size = len(self.charset)
        self.char2idx = {c : i for i, c in enumerate(self.charset)}
        self.idx2char = {i : c for i, c in enumerate(self.charset)}
        
        print(self.char2idx)
        print(self.idx2char)
    
    def pad(self, sent, max_seq_len):
        return sent + []
    
    def seq2idx(self, seq):
        return [self.char2idx[l] for l in seq]
        
    def idx2seq(self, seq):
        return [self.idx2char[l] for l in seq]
    
    def gen_tensor(self, seq):
        ind = self.seq2idx(seq)[:self.max_seq_length-1]
        ind.append(self.EOSTOKEN_i) # EOS token
        return torch.tensor(ind, dtype=torch.long).view(-1, 1)
    
    def samples(self, n_iters):
        n_it = 0
        while n_it < n_iters:
            n_it += 1
            idx = random.randint(0, len(self.data)-1)
            x, y = self.gen_tensor(self.text[idx]), self.gen_tensor(self.target[idx])
            #x, y = self.gen_tensor(self.text[idx]), self.gen_tensor(self.text[idx].split()[0])
            yield x, y
                
                
            
            
