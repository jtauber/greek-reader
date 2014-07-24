class LaTeX:

    def __init__(self):
        self.footnotes = {}
        self.footnote_counter = 1

    def preamble(self, typeface):
        return """
\\documentclass[a4paper,12pt]{{article}}

\\usepackage{{setspace}}
\\usepackage{{fontspec}}
\\usepackage{{dblfnote}}
\\usepackage{{pfnote}}
\\usepackage{{hyperref}}

\\setromanfont{{{typeface}}}

\\newcommand{{\\footlabel}}[2]{{%
    \\addtocounter{{footnote}}{{1}}%
    \\footnotetext[\\thefootnote]{{%
        \\addtocounter{{footnote}}{{-1}}%
        \\refstepcounter{{footnote}}\label{{#1}}%
        #2%
    }}%
    $^{{\\ref{{#1}}}}$%
}}

\\newcommand{{\\footref}}[1]{{%
    $^{{\\ref{{#1}}}}$%
}}

\\linespread{{1.5}}
\\onehalfspacing

\\makeatletter
\\renewcommand\\@makefntext[1]{{\\leftskip=2em\\hskip-2em\\@makefnmark#1}}
\\makeatother

\\begin{{document}}
""".format(typeface=typeface)

    def chapter_verse(self, chapter, verse):
        return "\\textbf{{\Large {}.{}}}".format(chapter, verse)

    def verse(self, verse):
        return "\\textbf{{{}}}".format(verse)

    def word(self, text, headword=None, parse=None, gloss=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("\\textendash\\ {}".format(parse))
            if gloss:
                footnote.append("\\textendash\\ \\textit{{{}}}".format(gloss))

            footnote = " ".join(footnote)

            if footnote in self.footnotes:
                return "{}\\footref{{{}}}".format(text,
                                                  self.footnotes[footnote])
            else:
                ref = self.footnote_counter
                self.footnotes[footnote] = ref
                self.footnote_counter += 1
                return "{}\\footlabel{{{}}}{{{}}}".format(text, ref, footnote)

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"
