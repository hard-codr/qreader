import qreader.extractor as extractor
from bs4 import BeautifulSoup
from requests.utils import requote_uri
import urllib.parse
import requests
import qreader.categorizer as categorizer

def get_hn_score(url):
    pass


def compute_complexity(article):
    pass

def extract_article_with_newspaper(url):
    """
    url = cleanup_url(url)
    did = get_hash(url)
    article = newspaper.Article(url=url, keep_article_html=True)
    try:
        article.download()
        article.parse()
        article.nlp()

        if is_failed(article.summary):
            return Article(did, url, False)
    except:
        return Article(did, url, False)

    article_html = article.article_html.strip()
    if article_html.startswith('<div>'):
        article_html = article_html[len('<div>'):-len('</div>')]

    article_md = pypandoc.convert_text(article_html, 'md', format='html')
    article_md = clean_markdown(article_md)

    def lx(l): return set(l) if l else set([])

    keywords = lx(article.keywords).union(lx(article.tags))
    keywords = [k.lower() for k in keywords]

    return Article(did, url, True, article.title, article.summary, keywords, article.authors, article_md)
    """
    pass


def get_bookmarks():
    ril_export = '/home/swapnil/Development/qReader/Research/ril_export.html'

    with open(ril_export, 'r') as f:
        lines = '\n'.join(f.readlines())

    bs = BeautifulSoup(lines, "lxml")
    anchors = bs.find_all('a')
    links = []
    for a in anchors:
        if 'href' in a.attrs:
            href = a.attrs['href']
            links += [href]

    return links


def extract_metadata():
    links = get_bookmarks()
    urls = {}
    i = 450
    with open('result.csv', 'w+') as f:
        # f.write('did,mood,readability,reading_time,url,title\n')
        for l in links[i:]:
            if not l.startswith('https://pocket.co/'):
                print('%s extracting %s' % (i+1, l))
                try:
                    a = extractor.extract_article_with_readibility(l)
                    if not a:
                        print('%s %s failed' % (i+1, l))
                        continue
                except:
                    print('%s %s failed' % (i+1, l))
                    i += 1
                    continue
                url = urllib.parse.urlparse(a.url)
                f.write('%s,%s,%s,%s,%s,%s,%s\n' % (i+1, a.did, a.mood, a.readability, int(a.reading_time_sec), url.netloc, a.title))
                f.flush()
            i += 1




def push_to_server():
    links = get_bookmarks()
    bulk = []
    headers = {
        "X-Authorization-Method": "Pocket",
        "Authorization": "Bearer abcdabcdabcdabcd",
        "Content-Type": "application/json"
    }
    for link in links:
        bulk += [link]
        if len(bulk) == 100:
            r = requests.post('http://192.168.31.32:12321/articles', headers=headers, json=bulk)
            if r.status_code != 201:
                break
            bulk = []


def categorize():
    links = get_bookmarks()
    id2link = {}
    for link in links:
        link_id = extractor.get_hash(link)
        id2link[link_id] = link

    with open('result.sum.csv', 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            splitline = line.split(',')
            did = splitline[1]
            mood = splitline[2]
            readability = splitline[3]
            time = splitline[4]

            if time == '': time = 60
            else: time = int(time)

            link = id2link[did] if did in id2link else 'unknown'

            print('%s = %s' % (link, categorizer.categories(mood, readability, time)))


if __name__ == '__main__':
    push_to_server()
    #a = extractor.extract_article_with_readibility('https://blog.skcript.com/asynchronous-io-in-rust-36b623e7b965')
    #print(a.readability)
    #print(a.mood)
    #print(a.reading_time_sec)
    pass
