#!/usr/bin/env python3

import argparse

from utils import (get_morphgnt, load_path_attr, load_wordset, load_yaml,
                   parse_verse_ranges)

argparser = argparse.ArgumentParser()
argparser.add_argument("verses", help="verses to cover (e.g. 'John 18:1-11')")
argparser.add_argument("--headwords", help="headwords file")
argparser.add_argument("--glosses", help="glosses file")
argparser.add_argument(
    "--language", default="eng",
    help="language of glosses and other non-Greek text (defaults to eng)")
argparser.add_argument("--exclude", help="exclusion list file")
argparser.add_argument(
    "--typeface", default="Times New Roman",
    help="typeface to use (defaults to Times New Roman)")
argparser.add_argument(
    "--backend", default="backends.LaTeX",
    help="python class to use for backend (defaults to backends.LaTeX)")


args = argparser.parse_args()

verses = parse_verse_ranges(args.verses)

if args.exclude:
    exclusions = load_wordset(args.exclude)
else:
    exclusions = set()

if args.glosses:
    glosses = load_yaml(args.glosses)
else:
    glosses = None

if args.headwords:
    headwords = load_yaml(args.headwords)
else:
    headwords = {}


def verb_parse(ccat_parse):
    text = ccat_parse[1:4]
    if ccat_parse[3] in "DISO":
        text += " " + ccat_parse[0] + ccat_parse[5]
    elif ccat_parse[3] == "P":
        text += " " + ccat_parse[4:7]
    return text


def strip_textcrit(word):
    return word.replace("⸀", "").replace("⸂", "").replace("⸃", "")


def output_reader(verses, backend, language):
    print(backend.preamble(args.typeface, language))

    postponed_book = postponed_chapter = None

    for entry in get_morphgnt(verses):
        if entry[0] == "WORD":
            row = entry[1]
            lexeme = row["lemma"]
            text = strip_textcrit(row["text"])
            if lexeme not in exclusions:
                pos = row["ccat-pos"]
                headword = headwords.get(lexeme, lexeme)
                if glosses:
                    gloss = glosses[lexeme].get(
                        row["bcv"], glosses[lexeme]["default"])
                else:
                    gloss = None
                if pos in ["V-"]:
                    parse = verb_parse(row["ccat-parse"])
                else:
                    parse = None
                print(backend.word(text, headword, parse, gloss, language), end="")
            else:
                print(backend.word(text), end="")

        elif entry[0] == "VERSE_START":
            if postponed_book:
                print(backend.book_chapter_verse(
                    postponed_book, postponed_chapter, entry[1]), end="")
                postponed_book = postponed_chapter = None
            elif postponed_chapter:
                print(backend.chapter_verse(postponed_chapter, entry[1]), end="")
                postponed_chapter = None
            else:
                print(backend.verse(entry[1]), end="")
        elif entry[0] == "CHAPTER_START":
            postponed_chapter = entry[1]
        elif entry[0] == "BOOK_START":
            postponed_book = entry[1]
        else:
            print(backend.comment(entry))

    print(backend.postamble())


output_reader(verses, load_path_attr(args.backend)(), args.language)
