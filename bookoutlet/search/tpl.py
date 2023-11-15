from typing import List
from urllib.parse import urlencode

from bs4 import BeautifulSoup

from search.scraper import Scraper


class TorontoLibrarySearch(Scraper):
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        super().__init__(titles, fuzz_thresh=fuzz_thresh)
        self.base_url = 'https://www.torontopubliclibrary.ca/search.jsp?'
        self.domain = 'https://www.torontopubliclibrary.ca'

    def parse_titles(self, response: str) -> List[str]:
        """
        Find the physical books that are available at any library branch.
        """
        soup = BeautifulSoup(response, 'html.parser')
        titles = []
        search_results = soup.find_all(lambda t: t.name == 'div' and t.get('class') == ['record-result'])[:5] # limit to 5 titles
        for tag in search_results:
            title = tag.find(lambda t: t.name == 'span' and t.get('class') == ['notranslate']).text
            identifier = tag.find(lambda t: t.name == 'span' and t.get('class') == ['format']).text.strip()
            if identifier == 'Book':
                # Get the link to the book page
                page = tag.find(lambda t: t.name == 'a' and t.get('href', '')[:7] == '/detail').get('href')
                # Just check if it's available in at least 1 library branch
                if page and self.__check_availability(self.domain + page, 1):
                    titles.append(title)
                else:
                    print("{} unavailable".format(title))
            else:
                print("{} not a book ({})".format(title, identifier))
                                
        print("{} titles available out of {} search results".format(len(titles), len(search_results)))
        return titles

    def __check_availability(self, page: str, threshold: int = 1) -> bool:
        soup = BeautifulSoup(self.scraper.get(page).text, 'html.parser')
        holdings = soup.find(lambda t: t.name == 'div' and t.get('id') == 'branch-holdings')
        availability_fn = lambda t: t.name == 'span' and t.get('class') == ['in-library']
        if threshold == 1:
            return holdings.find(availability_fn) is not None
        return len(holdings.find_all(availability_fn)) >= threshold

    def _search(self, query: str) -> str:
        encoded_query = urlencode({'Ntt': query})
        url = self.base_url + encoded_query
        return self.scraper.get(url).text
