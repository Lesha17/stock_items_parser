from tryouts.torch_sec2sec.torch_sec2sec import Seq2seqAttModel
from utils import GoodsDataset

dataset = GoodsDataset(max_seq_size=128)

model = Seq2seqAttModel(dataset)

model.train(n_iters=5000)

