import torch
import torch.nn as nn
from torch import optim

from tryouts.torch_sec2sec import layers

import matplotlib.pyplot as plt
plt.switch_backend('agg')
import matplotlib.ticker as ticker

import time
import math
import random


def asMinutes(s):
    m = math.floor(s / 60)
    s -= m * 60
    return '%dm %ds' % (m, s)


def timeSince(since, percent):
    now = time.time()
    s = now - since
    es = s / (percent)
    rs = es - s
    return '%s (- %s)' % (asMinutes(s), asMinutes(rs))

def showPlot(points):
    plt.figure()
    fig, ax = plt.subplots()
    # this locator puts ticks at regular intervals
    loc = ticker.MultipleLocator(base=0.2)
    ax.yaxis.set_major_locator(loc)
    plt.plot(points)

def to_str(l):
    s = ''
    for c in l:
        s += c
    return s

class Seq2seqAttModel:
    def __init__(self, dataset, teacher_forcing_ratio=0.3):
        
        self.dataset = dataset
        self.teacher_forcing_ratio = teacher_forcing_ratio
        
        self.max_seq_length = dataset.max_seq_length
        
        self.encoder = layers.EncoderRNN(input_size=dataset.char_vocab_size,
                                         hidden_size=200)
        self.decoder = layers.AttnDecoderRNN(hidden_size=200,
                                             output_size=dataset.char_vocab_size,
                                             dropout_p=0.1,
                                             max_length=dataset.max_seq_length)  
       
                                             
        
    def train_on_sample(self, input_tensor, target_tensor, encoder_optimizer, decoder_optimizer, criterion):
        encoder_hidden = self.encoder.initHidden()

        encoder_optimizer.zero_grad()
        decoder_optimizer.zero_grad()

        input_length = input_tensor.size(0)
        target_length = target_tensor.size(0)

        encoder_outputs = torch.zeros(self.max_seq_length, self.encoder.hidden_size)

        loss = 0

        for ei in range(input_length):
            encoder_output, encoder_hidden = self.encoder(
                input_tensor[ei], encoder_hidden)
            encoder_outputs[ei] = encoder_output[0, 0]

        decoder_input = torch.tensor([[self.dataset.SOSTOKEN_i]]) # SOS TOKEN

        decoder_hidden = encoder_hidden

        use_teacher_forcing = (random.random() < self.teacher_forcing_ratio)

        if use_teacher_forcing:
            # Teacher forcing: Feed the target as the next input
            for di in range(target_length):
                decoder_output, decoder_hidden, decoder_attention = self.decoder(
                    decoder_input, decoder_hidden, encoder_outputs)
                loss += criterion(decoder_output, target_tensor[di])
                decoder_input = target_tensor[di]  # Teacher forcing

        else:
            # Without teacher forcing: use its own predictions as the next input
            for di in range(target_length):
                decoder_output, decoder_hidden, decoder_attention = self.decoder(
                    decoder_input, decoder_hidden, encoder_outputs)
                topv, topi = decoder_output.topk(1)
                decoder_input = topi.squeeze().detach()  # detach from history as input

                loss += criterion(decoder_output, target_tensor[di])
                if decoder_input.item() == self.dataset.EOSTOKEN_i: # EOS TOKEN
                    break

        loss.backward()

        encoder_optimizer.step()
        decoder_optimizer.step()

        return loss.item() / target_length
    
    def train(self, n_iters, print_every=500, plot_every=100, learning_rate=0.005):
        start = time.time()
        plot_losses = []
        print_loss_total = 0  # Reset every print_every
        plot_loss_total = 0  # Reset every plot_every

        encoder_optimizer = optim.SGD(self.encoder.parameters(), lr=learning_rate)
        decoder_optimizer = optim.SGD(self.decoder.parameters(), lr=learning_rate)
        criterion = nn.NLLLoss()
        
        iteration = 0   
        for input_tensor, target_tensor in self.dataset.samples(n_iters):
            iteration += 1

            #if iteration % print_every == 0:
            #    print('Before')
             #   print('Input sample: {}'.format(to_str(self.dataset.idx2seq(input_tensor[:,0].tolist()))))
              #  wrds, _ = self.evaluate(to_str(self.dataset.idx2seq(input_tensor[:, 0].tolist())))
               # print(to_str(wrds))

            loss = self.train_on_sample(input_tensor, target_tensor, encoder_optimizer, decoder_optimizer, criterion)
            print_loss_total += loss
            plot_loss_total += loss

            if iteration % print_every == 0:
                print_loss_avg = print_loss_total / print_every
                print_loss_total = 0

                print('Input sample: {}'.format(to_str(self.dataset.idx2seq(input_tensor[:,0].tolist()))))
                wrds, _ = self.evaluate(to_str(self.dataset.idx2seq(input_tensor[:,0].tolist())))
                print(to_str(wrds))

                print('%s (%d %d%%) NLL = %.4f' % (timeSince(start, iteration / n_iters),
                                                   iteration, iteration / n_iters * 100, print_loss_avg))

                wrds, _ = self.evaluate('Здравствуйте, меня зовут Алексей')
                print(to_str(wrds))
                wrds, _ = self.evaluate('Карточка Очень темный желто-зеленый')
                print(to_str(wrds))

                #wrds, _ = self.evaluate(r'Зажим Сплитстоун 25d75x 1 g Селадон МЛ')
                #print(to_str(wrds))
                #wrds, _ = self.evaluate(r'Карточка JCM к1536316 Очень темный желто-зеленый')
                #print(to_str(wrds))


            if iteration % plot_every == 0:
                plot_loss_avg = plot_loss_total / plot_every
                plot_losses.append(plot_loss_avg)
                plot_loss_total = 0

        wrds, _ = self.evaluate('Здравствуйте, меня зовут Алексей')
        print(to_str(wrds))
        wrds, _ = self.evaluate('Карточка Очень темный желто-зеленый')
        print(to_str(wrds))

        showPlot(plot_losses)
        
    def evaluate(self, sentence):
        with torch.no_grad():
            input_tensor = self.dataset.gen_tensor(sentence)
            input_length = input_tensor.size()[0]
            encoder_hidden = self.encoder.initHidden()

            encoder_outputs = torch.zeros(self.max_seq_length, self.encoder.hidden_size)

            for ei in range(input_length):
                encoder_output, encoder_hidden = self.encoder(input_tensor[ei],
                                                              encoder_hidden)
                encoder_outputs[ei] += encoder_output[0, 0]

            decoder_input = torch.tensor([[self.dataset.SOSTOKEN_i]])  # SOS

            decoder_hidden = encoder_hidden

            decoded_chars = []
            decoder_attentions = torch.zeros(self.max_seq_length, self.max_seq_length)

            for di in range(self.max_seq_length):
                decoder_output, decoder_hidden, decoder_attention = self.decoder(
                    decoder_input, decoder_hidden, encoder_outputs)
                decoder_attentions[di] = decoder_attention.data
                topv, topi = decoder_output.data.topk(1)
                if topi.item() == self.dataset.EOSTOKEN_i:
                    decoded_chars.append(self.dataset.EOSTOKEN_i)
                    break
                else :
                    decoded_chars.append(topi.item())

                decoder_input = topi.squeeze().detach()

            return self.dataset.idx2seq(decoded_chars), decoder_attentions[:di + 1]
