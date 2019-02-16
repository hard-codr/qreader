import requests
import w3lib.url
import hashlib
from readability import Document
import html2text
import textacy
import textacy.lexicon_methods
import re
import logging
import time

import qreader.summarizer as summarizer
import qreader.cleantxt as textcleaner
import qreader.categorizer as categorizer
from qreader.model import Article


def cleanup_url(url):
    url = w3lib.url.canonicalize_url(url)
    if "utm_" in url:
        matches = re.findall(r'(.+\?)([^#]*)(.*)', url)
        if len(matches) > 0:
            match = matches[0]
            query = match[1]
            sanitized_query = '&'.join([p for p in query.split('&') if not p.startswith('utm_')])
            url = match[0] + sanitized_query + match[2]
            if url.endswith('?'):
                return url[:-1]
    return url


def get_hash(content):
    content = content.encode('utf-8')
    m = hashlib.sha256()
    m.update(content)
    return m.hexdigest()


def is_failed(text):
    text = text.lower()
    if 'make sure your browser supports javascript' in text:
        return True
    return False


WPS = 3

POSITIVE = set(['HAPPY', 'INSPIRED'])
NEUTRAL = set(['DONT_CARE', 'AMUSED'])
NEGATIVE = set(['AFRAID', 'ANGRY', 'ANNOYED', 'SAD'])


# Issues:
# - Bloomberg article doesn't work (JS rendered webpage)
# - crayon syntax highlighter doesn't work
def extract_article_with_readibility(url):
    url = cleanup_url(url)
    did = get_hash(url)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    try:
        r = requests.get(url, headers=headers, timeout=5)
    except:
        logging.info("request timed out")
        return None

    content_type = r.headers['Content-Type'] if 'Content-Type' in r.headers else 'text/html'
    if r.status_code != 200 or is_failed(r.text) or 'application/pdf' in content_type:
        logging.info("Got request status code = %s" % r.status_code)
        return None

    doc = Document(r.text)

    title = doc.title()
    html = doc.get_clean_html()
    text = textcleaner.cleantxt(html)
    text = textacy.preprocess_text(text, lowercase=True, no_punct=True, no_urls=True, no_emails=True,
                                  no_phone_numbers=True, no_numbers=True, no_contractions=True)
    doc = textacy.Doc(text, lang=u'en')
    md = html2text.html2text(html)

    ts = textacy.TextStats(doc)

    time_to_read_sec = ts.n_words/WPS

    flesch_reading_ease = ts.flesch_reading_ease
    if flesch_reading_ease > 60.0:
        readability = 'easy'
    elif 60.0 >= flesch_reading_ease > 30.0:
        readability = 'average'
    else:
        readability = 'difficult'

    summary = ' '.join([str(sent) for sent in summarizer.summarize(html, url)])
    summarydoc = textacy.Doc(summary, lang=u'en')

    emotions = textacy.lexicon_methods.emotional_valence(summarydoc.tokens)

    max_emotion = ''
    max_emotion_score = 0
    for k, v in emotions.items():
        if v > max_emotion_score:
            max_emotion = k
            max_emotion_score = v

    if max_emotion in POSITIVE:
        mood = 'positive'
    elif max_emotion in NEGATIVE:
        mood = 'negative'
    else:
        mood = 'neutral'

    # print('title = %s' % title)
    # print('url = %s' % url)
    # print('time = %s sec, mood = %s, readability = %s' % (time_to_read_sec, mood, readability))
    # print('summary = %s' % summary)
    # print('=== Article ===\n%s' % md)

    a = Article(did, url, True, title=title, summary=summary, markdown=md)
    a.set_mood(mood)
    a.set_reading_time(time_to_read_sec)
    a.set_readability(readability)

    return a


if __name__ == '__main__':
    headers = {
        "Authorization": "oOcXJlYWRlci1zZXJ2ZXJyVAsSC1VzZXJBcnRpY2xlIkM0Ml81MDIxMmZhZTM5OGQzYWI",
        "Content-Type": "application/json"
    }
    current_time = int(time.time())
    while True:
        r = requests.get('http://192.168.31.32:12321/queue?query_time=%s&limit=2' % current_time, headers=headers)
        if r.status_code == 200:
            links = r.json()['records']
            if len(links) == 0:
                break
            result = []
            for link in links:
                print('Processing %s' % link['link'])
                try:
                    article = extract_article_with_readibility(link['link'])
                    categories = categorizer.categories(article.mood, article.readability, article.reading_time_sec)
                except:
                    article = None

                if article:
                    result += [
                        {
                            "link_id": link['link_id'],
                            "is_parsed": True,
                            "title": article.title,
                            "summary": article.summary,
                            "mood": article.mood,
                            "reading_time": article.reading_time_sec,
                            "readability": article.readability,
                            "categories": categories
                        }
                    ]
                else:
                    result += [
                        {
                            "link_id": link['link_id'],
                            "is_parsed": False
                        }
                    ]

            r = requests.post('http://192.168.31.32:12321/queue', headers=headers, json=result)
            print('status_message = %s' % r.reason)
        else:
            print('status_message = %s' % r.reason)
            break

