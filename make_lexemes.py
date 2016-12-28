#!/usr/bin/env python3

"""
Note that this is a one-off script to pull in the lexemes.yaml data from
morphological-lexicon and store it here.

Once the reduced lexemes.yaml is in this repo, this script exists only for
historical interest and reproducibility.
"""

from utils import load_yaml, sorted_items

for key, value in sorted_items(
        load_yaml("../../morphgnt/morphological-lexicon/lexemes.yaml")):
    print("{}:".format(key))
    headword = value.get("full-citation-form", value.get("danker-entry", key))
    gloss = value.get("gloss")
    print("    headword: {}".format(headword))
    if gloss:
        print("    gloss: {}".format(gloss))
