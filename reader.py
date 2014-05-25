#!/usr/bin/env python3

import argparse

from utils import load_yaml, load_wordset, get_morphgnt, parse_verse_ranges

argparser = argparse.ArgumentParser()
argparser.add_argument("verses", help="verses to cover (e.g. 'John 18:1-11')")
argparser.add_argument("--headwords", help="headwords file")
argparser.add_argument("--glosses", help="glosses file")
argparser.add_argument("--exclude", help="exclusion list file")
argparser.add_argument(
    "--sblgnt", dest="sblgnt_dir", default="../sblgnt",
    help="path to MorphGNT sblgnt directory (defaults to ../sblgnt)")
argparser.add_argument(
    "--typeface", default="Times New Roman",
    help="typeface to use (defaults to Times New Roman)")

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


print("""
\\documentclass[a4paper,12pt]{{article}}

\\usepackage{{fontspec}}
\\usepackage{{dblfnote}}
\\usepackage{{pfnote}}

\\setromanfont{{{typeface}}}

\\linespread{{1.5}}
\\spaceskip 0.5em

\\begin{{document}}
""".format(typeface=args.typeface))

postponed_chapter = None

for entry in get_morphgnt(verses, args.sblgnt_dir):
    if entry[0] == "WORD":
        lexeme = entry[8]
        if lexeme not in exclusions:
            pos = entry[2]
            headword = headwords.get(lexeme, lexeme)
            if glosses:
                gloss = glosses[lexeme].get(entry[1], glosses[lexeme]["default"])
                if pos in ["V-"]:
                    print("{}\\footnote{{{} \\textendash\\ {} \\textendash\\ \\textit{{{}}}}}".format(strip_textcrit(entry[5]), headword, verb_parse(entry[3]), gloss))
                else:
                    print("{}\\footnote{{{} \\textendash\\ \\textit{{{}}}}}".format(strip_textcrit(entry[5]), headword, gloss))
            else:
                if pos in ["V-"]:
                    print("{}\\footnote{{{} \\textendash\\ {}}}".format(strip_textcrit(entry[5]), headword, verb_parse(entry[3])))
                else:
                    print("{}\\footnote{{{}}}".format(strip_textcrit(entry[5]), headword))
        else:
            print(strip_textcrit(entry[5]))
    elif entry[0] == "VERSE_START":
        if postponed_chapter:
            print("\\textbf{{\Large {}.{}}}".format(postponed_chapter, entry[1]))
            postponed_chapter = None
        else:
            print("\\textbf{{{}}}".format(entry[1]))
    elif entry[0] == "CHAPTER_START":
        postponed_chapter = entry[1]
    else:
        print("% {}".format(entry))

print("\\end{document}")
