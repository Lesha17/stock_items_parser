import pandas as pd
import numpy as np
import sys
import os

dataset_file = sys.argv[1]

output_dir = sys.argv[2]
if not os.path.isdir(output_dir):
    os.makedirs(output_dir)

train_share = float(sys.argv[3])
test_in_other_share = float(sys.argv[4])

df = pd.read_excel(dataset_file)
df = df.sample(frac=1).reset_index(drop=True)

msk = np.random.rand(len(df)) < train_share

train = df[msk]
other = df[~msk]

msk_test = np.random.rand(len(other)) < test_in_other_share
test = other[msk_test]
other = other[~msk_test]

train.to_excel(output_dir + '/train.xlsx')
test.to_excel(output_dir + '/test.xlsx')
other.to_excel(output_dir + '/other.xlsx')