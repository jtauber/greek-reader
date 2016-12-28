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
    default="lexemes.yaml",
    help="path to lexemes file "
         "(defaults to lexemes.yaml)")

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


for entry in get_morphgnt(verses):
    if entry[0] == "WORD":
        lemma = entry[1]["lemma"]
        if lemma not in exclusions and lemma not in glosses:
            glosses[lemma] = {"default": lexemes[lemma].get("gloss", "\"@@@\"")}

for lemma, gloss_entries in sorted_items(glosses):
    print("{}:".format(lemma))
    for k, v in sorted_items(gloss_entries):
        print("    {}: {}".format(k, v))
