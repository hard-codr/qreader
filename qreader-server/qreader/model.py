

class Article:
    ARTICLE_MOOD_NEG = 'NEGATIVE'  # angry, sad, complaining
    ARTICLE_MOOD_POS = 'POSITIVE'  # happy, motivating, inspiring,
    ARTICLE_MOOD_NEUTRAL = 'NEUTRAL'  # no particular emotion, like tech article, explanations

    def __init__(self, did, url, is_parsed, title='', summary='', keywords=None, authors=None, markdown=''):
        if authors is None:
            authors = []
        if keywords is None:
            keywords = []
        self.did = did
        self.url = url
        self.is_parsed = is_parsed
        self.title = title
        self.summary = summary
        self.keywords = keywords
        self.authors = authors
        self.markdown = markdown
        self.mood = ''  # textacy emotional valance
        self.readability = ''  # textacy grade level
        self.reading_time_sec = 0  # time to read the article (for now standard time, not user specific)
        self.topic_complexity = 0  # ???
        self.t2s_score = 0  # text-2-speech score, 1-100, 1-properly text to speech, 100-not text to speech
        self.visual_score = 0  # how much visual information is present in the article, 1-100, 1-no visual , 100-high

    def set_mood(self, mood):
        self.mood = mood

    def set_readability(self, readability):
        self.readability = readability

    def set_reading_time(self, time_sec):
        self.reading_time_sec = time_sec
