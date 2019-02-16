import re
import html.entities

def cleantxt(text):
    for nuketagblock in ['title', 'head']:
        text = noTagBlock(text, nuketagblock)
    text = justBody(text)
    text = noComments(text)
    for nuketagblock in ['script', 'style', 'noscript', 'form',
                         'object', 'embed', 'select']:
        text = noTagBlock(text, nuketagblock)
    text = stripParams(text)
    text = lowercaseTags(text)
    text = listNuker(text)
    for nuketag in ['div', 'span', 'img', 'a', 'b', 'i', 'param', 'table',
                    'td', 'tr', 'font', 'title', 'head', 'meta', 'strong', 'em', 'iframe']:
        text = noTag(text, nuketag)
    text = singleizer(text)
    text = convert_html_entities(text)
    text = addmarkdown(text)
    text = just2LR(text)

    return text


def justBody(text):
    pattern = r"<\s*body\s*.*?>(?P<capture>.*)<\s*/body\s*>"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    bodymat = pat.search(text)
    if bodymat:
        return bodymat.group('capture')
    else:
        return ''


def addmarkdown(text):
    text = text.replace('<p>', "\n")
    text = text.replace('</p>', "")
    text = text.replace('<hr>', "\n")
    text = text.replace('<blockquote>', "\n")
    text = text.replace('</blockquote>', "")
    text = text.replace('<h1>', "\n")
    text = text.replace('<h2>', "\n")
    text = text.replace('<h3>', "\n")
    text = text.replace('<h4>', "\n")
    text = text.replace('</h1>', "")
    text = text.replace('</h2>', "")
    text = text.replace('</h3>', "")
    text = text.replace('</h4>', "")
    text = text.strip()
    return text


def just2LR(text):
    pattern = r"\n{2,}"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    less = pat.sub(r'\n\n', text)
    pattern = " {2,}"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    less = pat.sub(' ', less)
    return less


def lowercaseTags(text):
    pattern = r"<(/?[a-zA-Z0-9]+)>"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    lowered = pat.sub(r'<\1>'.lower(), text)
    return lowered


def stripParams(text):
    pattern = r"(<\s*[a-zA-Z0-9]+).*?(?:>)"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    nopram = pat.sub(r'\1>', text)
    return nopram


def listNuker(text):
    pattern = r"<\s*(ol|ul)\s*.*?>.*?<\s*/(ol|ul)\s*>"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    listless = pat.sub('', text)
    pattern = r"<\s*li\s*.*?>.*?<\s*/li\s*>"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    listless = pat.sub('', listless)
    pattern = r"(<\s*(li|ol|ul)\s*.*?>)|(<\s*/(li|ol|ul)\s*>)"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    listless = pat.sub('', listless)
    return listless


def noTag(text, tag):
    pattern = r"(<\s*%s\s*.*?>)|(<\s*/%s\s*>)" % (tag, tag)
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    tagless = pat.sub('', text)
    return tagless


def noTagBlock(text, tag):
    pattern = r"<\s*%s\s*.*?>.*?<\s*/%s\s*>" % (tag, tag)
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    byeblock = pat.sub('', text)
    return byeblock


def noComments(text):
    pattern = r"<!--.*?-->"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    byeblock = pat.sub('', text)
    return byeblock


def singleizer(text):
    pattern = r"\t|\r"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    singled = pat.sub('', text)
    pattern = r"^.{,30}$"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL | re.MULTILINE)
    singled = pat.sub('', singled)
    pattern = r"\n{2,}"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    singled = pat.sub(r'\n', singled)
    pattern = r"\n.{,10}\n"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    singled = pat.sub(r'\n', singled)
    pattern = r"^\n|\n$"
    pat = re.compile(pattern, re.IGNORECASE | re.DOTALL)
    singled = pat.sub('', singled)
    return singled


def convert_html_entities(s):
    matches = re.findall("&#\d+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            name = hit[2:-1]
            try:
                entnum = int(name)
                s = s.replace(hit, chr(entnum))
            except ValueError:
                pass

    matches = re.findall("&#[xX][0-9a-fA-F]+;", s)
    if len(matches) > 0:
        hits = set(matches)
        for hit in hits:
            hex = hit[3:-1]
            try:
                entnum = int(hex, 16)
                s = s.replace(hit, chr(entnum))
            except ValueError:
                pass

    matches = re.findall("&\w+;", s)
    hits = set(matches)
    amp = "&"
    if amp in hits:
        hits.remove(amp)
    for hit in hits:
        name = hit[1:-1]
        if name in html.entities.name2codepoint:
            s = s.replace(hit, chr(html.entities.name2codepoint[name]))
    s = s.replace(amp, "&")
    return s
