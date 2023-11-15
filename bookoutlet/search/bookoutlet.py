from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from search.scraper import Scraper


class BookOutletSearch(Scraper):
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        super().__init__(titles, fuzz_thresh=fuzz_thresh)
        self.base_url = 'https://bookoutlet.ca/Store/Search?'

    def parse_titles(self, response: str) -> List[str]:
        soup = BeautifulSoup(response, 'html.parser')
        titles = list(map(lambda t: t.text, soup.find_all(
            lambda t: t.name == 'a' and t.get('data-text') is not None)))
        print("{} titles found".format(len(titles)))
        return titles

    def _search(self, query: str) -> str:
        encoded_query = urlencode({'qf': 'All', 'q': query})
        url = self.base_url + encoded_query
        return self.scraper.get(url).text
