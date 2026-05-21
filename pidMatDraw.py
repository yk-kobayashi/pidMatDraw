#!/usr/bin/env python3

# usage: [this] [tab-formatted alinged sequences] (-o output_prefix) (-v) (-s) (-f font_size)
# 
# recommended preparation for input sequences:
# mafft multifasta.fasta > multifasta_aligned.fasta
# seqkit fx2tab multifasta_aligned.fasta > multifasta_aligned.tab

import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument('arg1')
parser.add_argument('-o', '--out', default="")
parser.add_argument('-v', '--withvalue', action='store_true')
parser.add_argument('-f', '--fontsize', type=float, default=12)
parser.add_argument('--valuefont', type=float, default=10)
parser.add_argument('-s', '--square', action='store_true')
args = parser.parse_args()
outprefix = args.out

# input tab-formatted aligned FASTA file
alignedseqs = {}
with open(args.arg1, "r") as alignmentfile:
     for eachseq in alignmentfile:
        content = eachseq.split("\t")
        alignedseqs[content[0]] = content[1]

# define mutation and rate calculation
def compare_seqs(a, b):
    if a is None or b is None:
        print("Empty sequence included")
        return

    alignlength = max(len(a), len(b)) - 1
    matchbase, mismatch, indel, gap = 0, 0, 0, 0

    for i in range(alignlength):
        if a[i] == b[i] and a[i] != "-":
            matchbase += 1
        if a[i] != b[i] and a[i] != "-" and b[i] != "-":
            mismatch += 1
        if a[i] != b[i] and (a[i] == "-" or b[i] == "-"):
            indel += 1
        if a[i] == b[i] and a[i] == "-":
            gap += 1

    pairwisealignlength = alignlength - gap
    mutationrate = 100 * (mismatch + indel) / float(pairwisealignlength)
    identity = 100 * matchbase / float(pairwisealignlength)
    return [pairwisealignlength, matchbase, mismatch, indel, identity, mutationrate]

# compare and output
df = pd.DataFrame(columns=["seq1", "seq2", "length", "match", "SNP", "indel", "p_identity", "mutation_rate(%)"])
for key1, value1 in alignedseqs.items():
    name1 = key1
    seq1 = value1
    for key2, value2 in alignedseqs.items():
        name2 = key2
        seq2 = value2
        result = [name1, name2] + compare_seqs(seq1, seq2)
        comparison = name1 + "vs" + name2
        df.loc[comparison] = result

df.to_csv(outprefix + "fulltable.tsv", index=False, sep="\t")

identMatrix = df.pivot(index="seq1", columns="seq2", values="p_identity")
identMatrix.to_csv(outprefix + "matrix.tsv", sep="\t")

mask = np.triu(np.ones_like(identMatrix, dtype=bool))

# draw matrix heatmap
plt.figure(figsize=(20, 15))
plt.rcParams["font.size"] = args.fontsize

sns.heatmap(identMatrix, mask=mask, annot=args.withvalue, annot_kws={"size": args.valuefont}, fmt=".1f", cmap='YlGnBu', square=args.square, linewidths=.5, cbar_kws={"shrink": .5, "aspect": 20, "pad": 0.02})
plt.xlabel("")
plt.ylabel("")
plt.tight_layout()

plt.savefig(outprefix + "pidentMatrix.png", dpi=300)
