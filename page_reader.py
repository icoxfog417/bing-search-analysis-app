import re
import requests
from bs4 import BeautifulSoup


def get_page_text(url, target_description):
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    desc = target_description
    if "。" in target_description:
        desc = target_description[0:target_description.index("。")]
    match = re.compile(desc)
    nodes = soup.find_all(string=match)
    print(nodes)
