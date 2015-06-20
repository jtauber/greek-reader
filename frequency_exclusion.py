#!/usr/bin/env python3

import argparse
from collections import defaultdict

from pysblgnt import morphgnt_rows
from utils import print_status

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "occurrences", type=int,
    help="lower occurrence limit to exclude")
args = argparser.parse_args()

lexeme_counts = defaultdict(int)

for book_num in range(1, 28):
    for row in morphgnt_rows(book_num):
        lexeme_counts[row["lemma"]] += 1

num_lexemes = 0
for lexeme, count in lexeme_counts.items():
    if count >= args.occurrences:
        print(lexeme)
        num_lexemes += 1

print_status("output {}/{} lexemes appearing {} times or more".format(
    num_lexemes, len(lexeme_counts), args.occurrences)
)
