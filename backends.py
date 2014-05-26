class LaTeX:

    def preamble(self, typeface):
        return """
\\documentclass[a4paper,12pt]{{article}}

\\usepackage{{setspace}}
\\usepackage{{fontspec}}
\\usepackage{{dblfnote}}
\\usepackage{{pfnote}}

\\setromanfont{{{typeface}}}

\\linespread{{1.5}}
\\onehalfspacing

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

            return "{}\\footnote{{{}}}".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"
