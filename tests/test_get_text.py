import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(__file__), "../"))
from app import get_page_text


class TestGetPageText(unittest.TestCase):

    def test_get_page_text(self):
        url = "https://ja.wikipedia.org/wiki/%E3%83%9A%E3%83%B3%E3%82%AE%E3%83%B3"
        desc = "ペンギンは、鳥綱ペンギン目（Sphenisciformes）に属する種の総称である。 ペンギン科（Spheniscidae）のみが現生する。. 主に南半球に生息する海鳥であり、飛ぶことができない。"

        text = get_page_text(url, desc)
        print(text)


if __name__ == "__main__":
    unittest.main()
