import importlib
import re
import sys
import yaml

from pyuca import Collator

from pysblgnt import morphgnt_rows

collator = Collator()


def bcv_tuple(bcv):
    """
    converts a BBCCVV string into a tuple of book, chapter, verse number.

    e.g. "012801" returns (1, 28, 1)
    """
    return (int(i) for i in [bcv[0:2], bcv[2:4], bcv[4:6]])


def get_morphgnt(verses):
    """
    yield entries from MorphGNT for the given verses.

    verses is a list of verse-ranges where a verse-range is either a single
    verse-id or a tuple (start-verse-id, end-verse-id). A verse-id is the
    BBCCVV (book-chapter-verse) code used in the first column of MorphGNT.

    e.g. [("012801", "012815")] will yield Matthew 28:1-15.
    """
    for verse_range in verses:
        if isinstance(verse_range, (list, tuple)):
            start, end = verse_range
        else:
            start = end = verse_range

        yield("VERSE_RANGE_START", (start, end))

        start_book, start_chapter, start_verse = bcv_tuple(start)
        end_book, end_chapter, end_verse = bcv_tuple(end)

        state = 0  # 0 = not started, 1 = in progress, 2 = ended

        for book_num in range(start_book, end_book + 1):

            yield("BOOK_START", book_num)

            prev_chapter = prev_verse = None

            for row in morphgnt_rows(book_num):
                b, c, v = bcv_tuple(row["bcv"])
                if state == 0:
                    if (start_book, start_chapter, start_verse) == (b, c, v):
                        state = 1
                    else:
                        continue

                if (end_book, end_chapter) == (b, c) and end_verse < v:
                    state = 2
                    break

                if end_book == b and end_chapter < c:
                    state = 2
                    break

                if c != prev_chapter:
                    if prev_chapter:
                        if prev_verse:
                            yield("VERSE_END", prev_verse)
                        yield("CHAPTER_END", prev_chapter)
                    yield("CHAPTER_START", c)
                    prev_chapter = c
                    prev_verse = None

                if v != prev_verse:
                    if prev_verse:
                        yield("VERSE_END", prev_verse)
                    yield("VERSE_START", v)
                    prev_verse = v

                yield ("WORD", row)

            if state == 2:
                yield("VERSE_END", prev_verse)
                yield("CHAPTER_END_PARTIAL", prev_chapter)
                yield("BOOK_END_PARTIAL", book_num)
                break

            yield("VERSE_END", v)
            yield("CHAPTER_END", c)
            yield("BOOK_END", book_num)

        yield("VERSE_RANGE_END", (start, end))


def load_yaml(filename, wrapper=lambda key, metadata: metadata):
    with open(filename) as f:
        return {
            key: wrapper(key, metadata)
            for key, metadata in (yaml.load(f) or {}).items()
        }


def load_wordset(filename):
    with open(filename) as f:
        return set([
            word.split("#")[0].strip()
            for word in f
            if word.split("#")[0].strip()]
        )


def sorted_items(d):
    return sorted(d.items(), key=lambda x: collator.sort_key(x[0]))


def print_status(s):
    print("\x1b[36m" + s + "\x1b[0m", file=sys.stderr)


BOOK_NAMES = [
    {"Mt", "Matt", "Matthew"},
    {"Mk", "Mark"},
    {"Lk", "Luke"},
    {"Jn", "John"},
    {"Ac", "Acts"},
    {"Ro", "Rom", "Romans"},
    {"1Co", "1 Corinthians"},
    {"2Co", "2 Corinthians"},
    {"Ga", "Gal", "Galatians"},
    {"Eph", "Ephesians"},
    {"Php", "Philippians"},
    {"Col", "Colossians"},
    {"1Th", "1 Thessalonians"},
    {"2Th", "2 Thessalonians"},
    {"1Ti", "1 Timothy"},
    {"2Ti", "2 Timothy"},
    {"Tit", "Titus"},
    {"Phm", "Philemon"},
    {"Heb", "Hebrews"},
    {"Jas", "James"},
    {"1Pe", "1Pet", "1 Peter"},
    {"2Pe", "2Pet", "2 Peter"},
    {"1Jn", "1 John"},
    {"2Jn", "2 John"},
    {"3Jn", "3 John"},
    {"Jud", "Jude"},
    {"Re", "Rev", "Revelation"},
]

BOOK_NAME_MAPPINGS = {}

for i, name_set in enumerate(BOOK_NAMES, 1):
    for name in name_set:
        BOOK_NAME_MAPPINGS[name] = i

REF_RE = re.compile(r"""
        (
            (?P<book>({}))
            \s
            (
                (
                    (?P<chapter>\d+)
                    :
                    (?P<verse>\d+)
                    $
                )|(
                    (?P<chapter1>\d+)
                    :
                    (?P<verse_start1>\d+)
                    -
                    (?P<verse_end1>\d+)
                    $
                )|(
                    (?P<chapter_start2>\d+)
                    :
                    (?P<verse_start2>\d+)
                    -
                    (?P<chapter_end2>\d+)
                    :
                    (?P<verse_end2>\d+)
                    $
                )
            )
        )|(
            (?P<book_start>({}))
            \s
            (?P<chapter_start>\d+)
            :
            (?P<verse_start>\d+)
            -
            (?P<book_end>({}))
            \s
            (?P<chapter_end>\d+)
            :
            (?P<verse_end>\d+)
            $
        )
    """.format("|".join(BOOK_NAME_MAPPINGS.keys()),
               "|".join(BOOK_NAME_MAPPINGS.keys()),
               "|".join(BOOK_NAME_MAPPINGS.keys())),
    re.VERBOSE
)


def parse_verse_ranges(s):
    m = REF_RE.match(s)
    if not m:
        raise ValueError("can't parse verses")

    if m.groupdict()["book"]:
        book_start = BOOK_NAME_MAPPINGS[m.groupdict()["book"]]
        book_end = BOOK_NAME_MAPPINGS[m.groupdict()["book"]]
        if m.groupdict()["chapter"]:
            chapter_start = int(m.groupdict()["chapter"])
            chapter_end = int(m.groupdict()["chapter"])
            verse_start = int(m.groupdict()["verse"])
            verse_end = int(m.groupdict()["verse"])
        elif m.groupdict()["chapter1"]:
            chapter_start = int(m.groupdict()["chapter1"])
            chapter_end = int(m.groupdict()["chapter1"])
            verse_start = int(m.groupdict()["verse_start1"])
            verse_end = int(m.groupdict()["verse_end1"])
        else:
            chapter_start = int(m.groupdict()["chapter_start2"])
            chapter_end = int(m.groupdict()["chapter_end2"])
            verse_start = int(m.groupdict()["verse_start2"])
            verse_end = int(m.groupdict()["verse_end2"])
    elif m.groupdict()["book_start"]:
        book_start = BOOK_NAME_MAPPINGS[m.groupdict()["book_start"]]
        book_end = BOOK_NAME_MAPPINGS[m.groupdict()["book_end"]]
        chapter_start = int(m.groupdict()["chapter_start"])
        chapter_end = int(m.groupdict()["chapter_end"])
        verse_start = int(m.groupdict()["verse_start"])
        verse_end = int(m.groupdict()["verse_end"])

    if (book_start, chapter_start, verse_start) != \
       (book_end, chapter_end, verse_end):
        return [(
            "{:02d}{:02d}{:02d}".format(book_start, chapter_start, verse_start),
            "{:02d}{:02d}{:02d}".format(book_end, chapter_end, verse_end),
        )]
    else:
        return [
            "{:02d}{:02d}{:02d}".format(book_start, chapter_start, verse_start)
        ]


def load_path_attr(path):
    i = path.rfind(".")
    module, attr = path[:i], path[i + 1:]
    mod = importlib.import_module(module)
    return getattr(mod, attr)
