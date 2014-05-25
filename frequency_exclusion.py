#!/usr/bin/env python3

import argparse
from collections import defaultdict
import os.path

from utils import morphgnt_filename, print_status

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "occurrences", type=int,
    help="lower occurrence limit to exclude")
argparser.add_argument(
    "--sblgnt", dest="sblgnt_dir", default="../sblgnt",
    help="path to MorphGNT sblgnt directory (defaults to ../sblgnt)")
args = argparser.parse_args()

lexeme_counts = defaultdict(int)

for book_num in range(1, 28):
    filename = os.path.join(args.sblgnt_dir, morphgnt_filename(book_num))
    with open(filename) as morphgnt_file:
        for line in morphgnt_file:
            lexeme = line.split()[7]
            lexeme_counts[lexeme] += 1

num_lexemes = 0
for lexeme, count in lexeme_counts.items():
    if count >= args.occurrences:
        print(lexeme)
        num_lexemes += 1

print_status("output {}/{} lexemes appearing {} times or more".format(
    num_lexemes, len(lexeme_counts), args.occurrences)
)
