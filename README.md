# greek-reader

Python 3 tool for generating (initially Biblical) Greek readers

[Example from John 18:1-11](https://github.com/jtauber/greek-reader/raw/master/example/reader.pdf).
The steps to produce this are listed below under **A More Extended Example**.


## Background

*MorphGNT* and my *Morphological Lexicon* aren't quite rich enough yet to
produce the kind of readers I've long wanted to (much less the larger vision of
a *New Kind of Graded Reader*) but I've been inspired by Brian Renshaw's
(presumably manually produced) Greek Readers (e.g.
[A Good Friday Greek Reader](http://ntexegesis.com/blog/2014/4/18/a-good-friday-greek-reader-john-18-19))
to at least put together a tool to show what's possible now and then build on
it.

Of course, this isn't the first time I've written code to generate documents
from my Greek New Testament databases. This year marks the 20th anniversary of
my *Index to the Greek New Testament* which was the first major project I
undertook based on MorphGNT.

What I'm initially putting together here is a Python 3 library and command-line
script driven by text files. Eventually, I'll make a website out of this so the
majority of the target audience can actually use it :-)

For other Greek projects of mine, see <http://jktauber.com/>.


## Requirements

As well as Python 3, you'll need to install the packages in `requirements.txt`
via `pip` (preferably in a virtualenv).

This requirements file now includes the MorphGNT SBLGNT but if you want the
headwords and/or glosses from the `morphological-lexicon` you'll need to clone
that repo separately.

Finally, XeTeX is required as the current output of my scripts is LaTeX with
Unicode (although I do plan to support other backends eventually). On OS X, I
use the [MacTeX distribution](http://tug.org/mactex/mactex-download.html).


## How to Use


### Quick Start

Assuming you've installed the requirements, you can just type:

    ./reader.py "John 18:1-11" > reader.tex

You can then run

    xelatex reader.tex

twice (to ensure the footnotes are properly numbered).

Note that the `reader.pdf` PDF that results will footnote every word with the
lemma from MorphGNT and, in the case of verbs will include parsing codes. No
glosses will be included.


### Excluding Words

If you want to exclude certain words (for example, very common words) from
being annotated, you can pass an `--exclude` option to `reader.py`, giving the
name of a file which simply lists the lemmas to exclude. For example:

    αὐτός
    καί
    ὁ

You can easily generate such a file for any words occurring more than N times
by running `frequency_exclusion.py` with N as an argument. For example, to
create an exclusion file with any words occurring 31 times or more, run:

    ./frequency_exclusion.py 31 > exclude31.txt

and then run `./reader.py` with `--exclude exclude31.txt`.

Note that you can make edits to the file after running `frequency_exclusion.py`
to tailor the exclusion list to your needs.


### Adding Glosses

If you want to provide glosses, you can pass a `--glosses` option to `reader.py`
with the name of a YAML file that maps each lemma to a default gloss and
possibly per-verse overrides. A file with just default (i.e. global) glosses
might look like this:

    ἀποκόπτω:
        default: cut off
    ἕλκω:
        default: draw
    θήκη:
        default: sheath

If you have the `morphological-lexicon` checked out, you can auto-generate an
initial gloss file based on John Jeffrey Dodson's public domain lexicon using
`make_glosses.py` which takes a verse range argument just like `reader.py` as
well as an `--exclude` option.

If you want to extend an existing glosses file you can pass its name in using
the `--existing` option. This is useful if you've already made edits to the file
and you don't want to lose them when expanding the coverage of the file to more
verses (or fewer exclusions).


### Overriding Headwords

If you want to provide more detailed headwords (such as the article or
adjective endings) you can pass a `--headwords` option to `reader.py` with the
name of a YAML file that maps each lemma you want to override with the full
headword you want to use instead. For example:

    θήκη: θήκη, ης, ἡ
    Κεδρών: Κεδρών, ὁ

If you have the `morphological-lexicon` checked out, you can run
`make_headwords.py` to generate headword overrides for nouns and adjectives
based on Danker's Concise Lexicon. `make_headwords.py` takes a verse range
argument just like `reader.py` as well as an `--exclude` option.

If you want to extend an existing headword file you can pass its name in using
the `--existing` option. This is useful if you've already made edits to the file
and you don't want to lose them when expanding the coverage of the file to more
verses (or fewer exclusions).


### Changing Typeface

The default typeface is now Times New Roman but you can change this by passing
a `--typeface` option to `reader.py`.


### A More Extended Example

Here is how you might typically use the tools:

    ./frequency_exclusion.py 31 > example/exclude.txt
    ./make_glosses.py "John 18:1-11" --exclude example/exclude.txt > example/glosses.yaml
    # edit example/glosses.yaml to your liking
    ./make_headwords.py "John 18:1-11" --exclude example/exclude.txt > example/headwords.yaml
    ./reader.py "John 18:1-11" --headwords example/headwords.yaml --glosses example/glosses.yaml --exclude example/exclude.txt --typeface "Skolar PE" > example/reader.tex
    cd example
    xelatex reader.tex
    xelatex reader.tex
    open reader.pdf

You can see the results of this in the
[examples directory](https://github.com/jtauber/greek-reader/tree/master/example).
