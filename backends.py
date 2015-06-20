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

\\makeatletter
\\renewcommand\\@makefntext[1]{{\\leftskip=2em\\hskip-2em\\@makefnmark#1}}
\\makeatother

\\begin{{document}}
""".format(typeface=typeface)

    def chapter_verse(self, chapter, verse):
        return "\\textbf{{\Large {}.{}}}~".format(chapter, verse)

    def verse(self, verse):
        return "\\textbf{{{}}}~".format(verse)

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


class SILE:

    def preamble(self, typeface):
        return """\
\\begin[papersize=a4,class=book]{{document}}

\\font[family="{typeface}",size=12pt]
\\set[parameter=document.lineskip,value=6pt]
""".format(typeface=typeface)

    def chapter_verse(self, chapter, verse):
        return "\\font[size=16pt,weight=700]{{{}.{}}}\nobreak".format(chapter, verse)

    def verse(self, verse):
        return "\\font[weight=700]{{{}}}\nobreak".format(verse)

    def word(self, text, headword=None, parse=None, gloss=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("– {}".format(parse))
            if gloss:
                footnote.append("– \\font[style=italic]{{{}}}".format(gloss))

            return "{}\\footnote{{{}}}".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"
