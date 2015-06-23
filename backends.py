class LangMap:

    def lookup(language, backend):
        if backend == "backends.SILE":
            key = 0
        if backend == "backends.LaTeX":
            key = 1
        # ISO-639-3 : [ SILE, LaTeX ]
        supported_languages = {
            "afr": [ "af", None ],
            "amh": [ None, "amharic" ],
            "ara": [ None, "arabic" ],
            "asm": [ "as", None ],
            "ast": [ None, "asturian" ],
            "ben": [ "bn", "bengali" ],
            "bod": [ "bo", "tibetan" ],
            "bre": [ None, "breton" ],
            "bul": [ "bg", "bulgarian" ],
            "cat": [ "ca", "catalan" ],
            "ces": [ "cs", "czech" ],
            "cop": [ None, "coptic" ],
            "cym": [ "cy", "welsh" ],
            "dan": [ "da", "danish" ],
            "deu": [ "de", "german" ],
            "div": [ None, "divehi" ],
            "dsb": [ None, "lsorbian" ],
            "dsb": [ None, "usorbian" ],
            "ell": [ "el", "greek" ],
            "eng": [ "en", "english" ],
            "epo": [ "eo", "esperanto" ],
            "est": [ "et", "estonian" ],
            "eus": [ "eu", "basque" ],
            "fas": [ None, "farsi" ],
            "fin": [ "fi", "finnish" ],
            "fra": [ "fr", "french" ],
            "fur": [ None, "friulan" ],
            "gla": [ None, "scoish" ],
            "gle": [ "ga", "irish" ],
            "glg": [ None, "galician" ],
            "heb": [ None, "hebrew" ],
            "hin": [ "hi", "hindi" ],
            "hrv": [ "hr", "croatian" ],
            "hun": [ "hu", "magyar" ],
            "hye": [ None, "armenian" ],
            "ina": [ None, "interlingua" ],
            "ind": [ "id", "bahasai" ],
            "isl": [ "is", "icelandic" ],
            "ita": [ "it", "italian" ],
            "jpn": [ "ja", None ],
            "kan": [ "kn", "kannada" ],
            "lao": [ None, "lao" ],
            "lat": [ "la", "latin" ],
            "lav": [ "lv", "latvian" ],
            "lit": [ "lt", "lithuanian" ],
            "mal": [ "ml", "malayalam" ],
            "mar": [ "mr", "marathi" ],
            "msa": [ None, "bahasam" ],
            "nld": [ None, "dutch" ],
            "nno": [ "no", "nynorsk" ],
            "nor": [ None, "norsk" ],
            "nqo": [ None, "nko" ],
            "oci": [ None, "occitan" ],
            "ori": [ "or", None ],
            "pan": [ "pa", None ],
            "pms": [ None, "piedmontese" ],
            "pol": [ "pl", "polish" ],
            "pot": [ "pt", "portuges" ],
            "ptb": [ None, "brazil" ],
            "roh": [ "rm", "romansh" ],
            "ron": [ "ro", "romanian" ],
            "rus": [ "ru", "russian" ],
            "slk": [ "sk", "slovak" ],
            "slv": [ "sl", "slovenian" ],
            "sme": [ None, "samin" ],
            "san": [ "sa", "sanskrit" ],
            "spa": [ "es", "spanish" ],
            "sqi": [ None, "albanian" ],
            "srp": [ "sr", "serbian" ],
            "swe": [ "sv", "swedish" ],
            "syc": [ None, "syriac" ],
            "tam": [ "ta", "tamil" ],
            "tel": [ None, "telugu" ],
            "tha": [ "th", "thai" ],
            "tuk": [ "tk", "turkmen" ],
            "tur": [ "tr", "turkish" ],
            "ukr": [ "uk", "ukrainian" ],
            "urd": [ None, "urdu" ],
            "vie": [ None, "vietnamese" ]
        }
        if language in supported_languages and supported_languages[language][key]:
            return supported_languages[language][key]
        else:
            # This will pass through the language name given by the user which
            # will likely produce an error on typesetting, but better not to
            # just fail here in the event they have added language support for
            # their language above the currently known supported list
            return language


class LaTeX:

    def preamble(self, typeface, lang):
        return """
\\documentclass[a4paper,12pt]{{scrartcl}}

\\usepackage{{setspace}}
\\usepackage{{fontspec}}
\\usepackage{{dblfnote}}
\\usepackage{{pfnote}}
\\usepackage{{polyglossia}}
\\setdefaultlanguage[variant=ancient]{{greek}}
\\setotherlanguage{{{lang}}}

\\setromanfont{{{typeface}}}

\\linespread{{1.5}}
\\onehalfspacing

\\makeatletter
\\renewcommand\\@makefntext[1]{{\\leftskip=2em\\hskip-2em\\@makefnmark#1}}
\\makeatother

\\begin{{document}}
""".format(typeface=typeface, lang=lang)

    def chapter_verse(self, chapter, verse):
        return "\\textbf{{\Large {}.{}}}~".format(chapter, verse)

    def verse(self, verse):
        return "\\textbf{{{}}}~".format(verse)

    def word(self, text, headword=None, parse=None, gloss=None, lang=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("\\textendash\\ {}".format(parse))
            if gloss:
                footnote.append("\\textendash\\ \\text{}{{\\textit{{{}}}}}".format(lang, gloss))

            return "{}\\footnote{{{}}}".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"



class SILE:

    def preamble(self, typeface, lang):
        return """\
\\begin[papersize=a4,class=book]{{document}}

\\font[family="{typeface}",size=12pt,language=el]
\\set[parameter=document.lineskip,value=6pt]
""".format(typeface=typeface)

    def chapter_verse(self, chapter, verse):
        return "\\font[size=16pt,weight=700]{{{}.{}}}\\nobreak".format(chapter, verse)

    def verse(self, verse):
        return "\\font[weight=700]{{{}}}\\nobreak".format(verse)

    def word(self, text, headword=None, parse=None, gloss=None, lang=None):
        if headword is None and parse is None and gloss is None:
            return text
        else:
            footnote = []
            if headword:
                footnote.append(headword)
            if parse:
                footnote.append("– {}".format(parse))
            if gloss:
                footnote.append("– \\font[style=italic,language={}]{{{}}}".format(lang, gloss))

            return "{}\\footnote{{{}}}".format(text, " ".join(footnote))

    def comment(self, text):
        return "% {}".format(text)

    def postamble(self):
        return "\\end{document}"
