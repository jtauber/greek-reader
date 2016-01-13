#!/usr/bin/env python3

import argparse

from utils import (
    load_yaml, load_wordset, sorted_items, get_morphgnt, parse_verse_ranges)

argparser = argparse.ArgumentParser()
argparser.add_argument("verses", help="verses to cover (e.g. 'John 18:1-11')")
argparser.add_argument("--exclude", help="exclusion list file")
argparser.add_argument(
    "--existing", dest="strongs", help="existing strong file")
argparser.add_argument(
    "--lexicon", dest="lexemes",
    default="../morphological-lexicon/lexemes.yaml",
    help="path to morphological-lexicon lexemes.yaml file "
    "(defaults to ../morphological-lexicon/lexemes.yaml)")

args = argparser.parse_args()

verses = parse_verse_ranges(args.verses)

if args.exclude:
    exclusions = load_wordset(args.exclude)
else:
    exclusions = set()

lexemes = load_yaml(args.lexemes)

if args.strongs:
    strongs = load_yaml(args.strongs)
else:
    strongs = {}


for entry in get_morphgnt(verses):
    if entry[0] == "WORD":
        lemma = entry[1]["lemma"]
        if lemma not in exclusions and lemma not in strongs:
            strongs[lemma] = lexemes[lemma].get("strongs", "\"@@@\"")

for lemma, strong in sorted_items(strongs):
    print("{}: {}".format(lemma, strong))
