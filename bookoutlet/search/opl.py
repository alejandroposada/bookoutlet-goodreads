from urllib.parse import urlencode
from typing import List
from bs4 import BeautifulSoup

from search.scraper import Scraper


class OttawaLibrarySearch(Scraper):
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        super().__init__(titles, fuzz_thresh=fuzz_thresh)
        self.base_url = 'https://ottawa.bibliocommons.com/v2/search?'

    def parse_titles(self, response: str) -> List[str]:
        """
        Find the physical books that are available at any library branch.
        """
        soup = BeautifulSoup(response, 'html.parser')
        titles = []
        search_results = soup.find_all(lambda t: t.has_attr(
            'data-key') and t.get('data-key') == 'search-result-item')  # limit to 5 titles
        for tag in search_results:
            title = tag.find(lambda t: t.has_attr('class')
                             and t.get('class') == ['title-content']).text
            identifier = tag.find(lambda t: t.has_attr(
                'class') and 'cp-format-indicator' in t.get('class', [])).text
            if identifier == 'Book':
                available = tag.find(lambda t: t.has_attr(
                    'data-key') and t.get('data-key') == 'availability-status-available')
                if available:
                    titles.append(title)
                else:
                    print("{} unavailable".format(title))
            else:
                print("{} not a book ({})".format(title, identifier))

        print("{} titles available out of {} search results".format(
            len(titles), len(search_results)))
        return titles

    def _search(self, query: str) -> str:
        encoded_query = urlencode({'searchType': 'smart', 'query': query})
        url = self.base_url + encoded_query
        return self.scraper.get(url).text
