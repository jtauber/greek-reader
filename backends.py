from utils import load_yaml
import datetime


class LaTeX:

    def __init__(self):
        self.settings = load_yaml("LaTeX.yaml")

    def lang_code(self, language):
        return self.settings['languages'][language]

    def preamble(self, typeface, language):
        return """
\\documentclass[a4paper,12pt]{{scrartcl}}

\\usepackage{{setspace}}
\\usepackage{{fontspec}}
\\usepackage{{pfnote}}
\\usepackage{{polyglossia}}
\\setdefaultlanguage[variant=ancient]{{greek}}
\\setotherlanguage{{{language}}}

\\setromanfont{{{typeface}}}

\\linespread{{1.5}}
\\onehalfspacing

\\makeatletter
\\renewcommand\\@makefntext[1]{{\\leftskip=2em\\hskip-2em\\@makefnmark#1}}
\\makeatother

\\begin{{document}}
""".format(typeface=typeface, language=self.lang_code(language))

    def book_chapter_verse(self, book, chapter, verse):
        return """
\\textbf{{\Large {}.{}.{}}}~""".format(book, chapter, verse)

    def chapter_verse(self, chapter, verse):
        return """
\\textbf{{\Large {}.{}}}~""".format(chapter, verse)

    def verse(self, verse):
        return "\\textbf{{{}}}~".format(verse)

    def word(self, text, headword=None, parse=None, parse_robinson=None,
             gloss=None, strong=None, language=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("\\textendash\\ {}".format(parse))
            if gloss:
                footnote.append("\\textendash\\ \\text{}{{\\textit{{{}}}}}".format(self.lang_code(language), gloss))

            return "{}\\footnote{{{}}}".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"


class SILE:

    def __init__(self):
        self.settings = load_yaml("SILE.yaml")

    def lang_code(self, language):
        return self.settings['languages'][language]

    def preamble(self, typeface, language):
        return """\
\\begin[papersize=a4,class=book]{{document}}

\\font[family="{typeface}",size=12pt,language=el]
\\set[parameter=document.lineskip,value=6pt]
""".format(typeface=typeface)

    def book_chapter_verse(self, book, chapter, verse):
        return "\\font[size=16pt,weight=700]{{{}.{}.{}}} \\nobreak".format(
            book, chapter, verse)

    def chapter_verse(self, chapter, verse):
        return "\\font[size=16pt,weight=700]{{{}.{}}} \\nobreak".format(chapter, verse)

    def verse(self, verse):
        return "\\font[weight=700]{{{}}} \\nobreak".format(verse)

    def word(self, text, headword=None, parse=None, parse_robinson=None,
             gloss=None, strong=None, language=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("– {}".format(parse))
            if gloss:
                footnote.append("– \\font[style=italic,language={}]{{{}}}".format(self.lang_code(language), gloss))

            return "{}\\footnote{{{}}} %".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"


class MySword:

    VERSE_START_FORMAT = """INSERT INTO "Bible" VALUES({},{},{},'"""
    VERSE_END = "');"

    def __init__(self):
        self.book = None
        self.chapter = None
        self.postponed_verse = None

    def preamble(self, typeface, language):
        return """PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE "Bible" ("Book" INT,"Chapter" INT,"Verse" INT,"Scripture" TEXT);"""

    def book_chapter_verse(self, book, chapter, verse):
        self.book = 39 + book
        self.chapter = chapter
        old_pv = self.postponed_verse
        self.postponed_verse = self.VERSE_START_FORMAT.format(self.book, self.chapter, verse)
        return old_pv + self.VERSE_END if old_pv else ""

    def chapter_verse(self, chapter, verse):
        assert self.book
        self.chapter = chapter
        old_pv = self.postponed_verse
        assert old_pv
        self.postponed_verse = self.VERSE_START_FORMAT.format(self.book, self.chapter, verse)
        return old_pv + self.VERSE_END

    def verse(self, verse):
        assert self.book
        assert self.chapter
        old_pv = self.postponed_verse
        assert old_pv
        self.postponed_verse = self.VERSE_START_FORMAT.format(self.book, self.chapter, verse)
        return old_pv + self.VERSE_END

    def word(self, text, headword=None, parse=None, parse_robinson=None,
             gloss=None, strong=None, language=None):
        # Examples from established [MySword Bible
        # modules](http://mysword.info/download-mysword/bibles):
        # * ABP `<Q><wg>εν<WG1722><E> In<e><q> `
        # * HiSB `<Q><H><wh>בְּ<D>רֵאשִׁ֖ית<WH7225><h><X>be·re·Shit<x><T>In the beginning<t><q> `
        # * Byz2005++ `<wt>Βίβλος<WG976><WTN-NSF l=""βίβλος""> `
        # * TRa `<wt>Βίβλος<WG976><WTN-NSF l=""βίβλος""> `
        w = """<Q><G><wg>{}""".format(text) + ("""<WG{}>""".format(strong) if strong else "") + ("""<X>{}<x>""".format(headword) if headword else "") + ("""<WT{}>""".format(parse_robinson) if parse_robinson else "") + """<g><q> """  # Using `<X>...<x>` - meant for transliteration - for the headword because graphically better than a translators' note <RF>...<Rf> (inline vs. note).
        self.postponed_verse += w
        return ""

    def comment(self, text):
        return "-- {}".format(text)

    def postamble(self):
        self.book = None
        self.chapter = None
        x = []
        old_pv = self.postponed_verse
        if old_pv:
            x.append(old_pv + self.VERSE_END)
        self.postponed_verse = None
        x.append("""CREATE TABLE "Details" ("Description" TEXT, "Abbreviation" NVARCHAR(50), "Comments" TEXT, "Version" TEXT, "VersionDate" DATETIME, "PublishDate" DATETIME, "Source" TEXT, "Language" NVARCHAR(3), "RightToLeft" BOOL, "OT" BOOL, "NT" BOOL, "Strong" BOOL, encryption INT default 0, compressed INT default 0); -- No `"Title" NVARCHAR(255)`, as SBLGNT. No `"Publisher" TEXT, "Author" TEXT, "Creator" TEXT`, as SBLGNT. No `"VerseRules" TEXT`, following ABP rather than HiSB.
        INSERT INTO "Details" VALUES('Greek Reader with headwords, parsing codes, Strong''s numbers','GR','<div>This is the <a href="http://sblgnt.com">SBL Greek New Testament</a> with headwords, parsing codes and Strong''s numbers from the <a href="http://morphgnt.org/">MorphGNT</a> projects and <a href="https://github.com/jtauber/greek-reader">Greek reader generation</a> by James Tauber.</div>','0.0.1','{} 00:00:00',NULL,'https://github.com/jtauber/greek-reader','grc',0,0,1,0,0,0);
CREATE UNIQUE INDEX "bible_key" ON "Bible" ("Book" ASC, "Chapter" ASC, "Verse" ASC);
COMMIT;
""".format(datetime.date.today().strftime('%Y-%m-%d')))
        return """
""".join(x)
