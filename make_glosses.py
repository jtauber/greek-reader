#!/usr/bin/env python3

import argparse

from utils import (
    load_yaml, load_wordset, sorted_items, get_morphgnt, parse_verse_ranges)

argparser = argparse.ArgumentParser()
argparser.add_argument(
    "verses",
    help="verses to cover (e.g. 'John 18:1-11')")
argparser.add_argument(
    "--exclude",
    help="exclusion list file")
argparser.add_argument(
    "--existing", dest="glosses",
    help="existing glosses file")
argparser.add_argument(
    "--lexicon", dest="lexemes",
    default="../morphological-lexicon/lexemes.yaml",
    help="path to morphological-lexicon lexemes.yaml file "
         "(defaults to ../morphological-lexicon/lexemes.yaml)")
argparser.add_argument(
    "--sblgnt", dest="sblgnt_dir", default="../sblgnt",
    help="path to MorphGNT sblgnt directory (defaults to ../sblgnt)")

args = argparser.parse_args()

verses = parse_verse_ranges(args.verses)

if args.exclude:
    exclusions = load_wordset(args.exclude)
else:
    exclusions = set()

lexemes = load_yaml(args.lexemes)

if args.glosses:
    glosses = load_yaml(args.glosses)
else:
    glosses = {}


for entry in get_morphgnt(verses, args.sblgnt_dir):
    if entry[0] == "WORD":
        lexeme = entry[8]
        if lexeme not in exclusions and lexeme not in glosses:
            glosses[lexeme] = {"default": lexemes[lexeme].get("gloss", "@@@")}

for lexeme, gloss_entries in sorted_items(glosses):
    print("{}:".format(lexeme))
    for k, v in sorted_items(gloss_entries):
        print("    {}: {}".format(k, v))
