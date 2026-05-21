# script for draw two pairwise matrix in one square box
# usage: [this] [matrix1] [matrix2] (-o output_prefix)

import argparse
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
parser.add_argument('arg2')
parser.add_argument('-o', '--out')
parser.add_argument('--valuefont', type=float, default=10)
parser.set_defaults(out = "")
args = parser.parse_args()
outprefix = args.out

identMatrix1 = pd.read_csv(args.arg1, sep="\t", index_col=0)
identMatrix2 = pd.read_csv(args.arg2, sep="\t", index_col=0)

mask_upper = np.triu(np.ones_like(identMatrix1, dtype=bool), k=0)
mask_lower = np.tril(np.ones_like(identMatrix1, dtype=bool), k=0)

combined_matrix = np.where(mask_upper, identMatrix2, identMatrix1)
np.fill_diagonal(combined_matrix, np.nan)
combined_matrix = pd.DataFrame(combined_matrix, index = identMatrix1.index, columns = identMatrix1.columns)

plt.figure(figsize=(25, 15))

sns.heatmap(combined_matrix, annot=True, fmt=".1f", cmap='YlGnBu', annot_kws={"size": args.valuefont}, square=False, linewidths=.5, cbar_kws={"shrink": .5})

plt.tick_params(axis='x', bottom=False, top=True, labelbottom=False, labeltop=True)
plt.xlabel("")
plt.ylabel("")
plt.xticks(rotation=270)
plt.rcParams["font.size"] = 8
plt.tight_layout()

plt.savefig(outprefix + "doubleplotMatrix.png", dpi=300)
