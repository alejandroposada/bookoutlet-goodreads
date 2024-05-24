from typing import List
from urllib.parse import urlencode

import cloudscraper
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz, process


class Scraper:
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        self.titles = titles
        self.scraper = cloudscraper.create_scraper()
        self.fuzz_thresh = fuzz_thresh
        self.base_url = ""

    def search(self, query: str) -> str:
        print("Searching for: {}".format(query))
        return self._search(query)

    def find_title(self, title: str, titles: List[str]) -> bool:
        """
        Fuzzy string match the title against a list of titles.
        """
        if titles:
            # extractBests?
            choice, ratio = process.extractOne(
                title.lower(),
                list(map(lambda x: x.lower(), titles)),
                scorer=fuzz.partial_ratio,
            )
            found = ratio >= self.fuzz_thresh
        else:
            choice = "N/A"
            found = False
            ratio = 0
        print("'{}' was {}found".format(title, "" if found else "not "))
        print("Closest match ({}%): {}".format(ratio, choice))
        return found, choice, ratio

    def search_all_titles(self):
        found_titles = []
        for t in self.titles:
            # Search and check if the title was found
            print("***")
            r = self.search(t)
            r_titles = self.parse_titles(r)
            found, choice, ratio = self.find_title(t, r_titles)
            if r_titles and found:
                found_titles.append(
                    {"Query": t, "Match": choice, "Score": str(ratio) + "%"}
                )
            print("***")

        print("{} titles found out of {}".format(len(found_titles), len(self.titles)))
        return found_titles


class BookOutletSearch(Scraper):
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        super().__init__(titles, fuzz_thresh=fuzz_thresh)
        self.base_url = "https://bookoutlet.ca/browse?"

    def parse_titles(self, response: str) -> List[str]:
        soup = BeautifulSoup(response, "html.parser")
        titles = set([img["alt"] for img in soup.find_all("img", alt=True)])
        print("{} titles found".format(len(titles)))
        return titles

    def _search(self, query: str) -> str:
        encoded_query = urlencode({"qf": "All", "q": query})
        url = self.base_url + encoded_query
        return self.scraper.get(url).text
