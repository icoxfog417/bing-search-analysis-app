import re
from collections import Counter
import requests
from bs4 import BeautifulSoup, Comment
from janome.tokenizer import Tokenizer


class PageReader():

    def __init__(self):
        self.tokenizer = Tokenizer(wakati=True)
        self.excludes = ["。", "、", "（", "）"]
        self.exclude_nodes = ["cite", "script", "style"]

    def get_page_text(self, url, target_description):
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")

        counter = Counter()
        for token in self.tokenizer.tokenize(target_description):
            counter[token] += 1

        word_counts = counter.most_common(10)
        words = [w for w, c in word_counts if w not in self.excludes]
        pattern = re.compile("({})".format("|".join(words)))
        nodes = soup.find_all(string=pattern)

        nodes = [n for n in nodes if not isinstance(n, Comment)]
        nodes = [n for n in nodes if n.parent.name not in self.exclude_nodes]
        texts = [n.string.strip() for n in nodes]
        texts = [t for t in texts if t]
        return texts
