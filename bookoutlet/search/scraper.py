from typing import List

import cloudscraper
from fuzzywuzzy import fuzz, process


class Scraper:
    def __init__(self, titles: List[str], fuzz_thresh: int = 90):
        self.titles = titles
        self.scraper = cloudscraper.CloudScraper()
        self.fuzz_thresh = fuzz_thresh
        self.base_url = ''

    def parse_titles(self, response: str) -> List[str]:
        pass

    def search(self, query: str) -> str:
        print("Searching for: {}".format(query))
        return self._search(query)

    def _search(self, query: str) -> str:
        pass

    def find_title(self, title: str, titles: List[str]) -> bool:
        """
        Fuzzy string match the title against a list of titles.
        """
        if titles:
            choice, ratio = process.extractOne(title.lower(), list(
                map(lambda x: x.lower(), titles)), scorer=fuzz.partial_ratio)
            found = ratio >= self.fuzz_thresh
        else:
            choice = "N/A"
            found = False
            ratio = 0
        print("'{}' was {}found".format(title, "" if found else "not "))
        print("Closest match ({}%): {}".format(ratio, choice))
        return found

    def search_all_titles(self):
        found = []
        for t in self.titles:
            # Search and check if the title was found
            print("***")
            r = self.search(t)
            r_titles = self.parse_titles(r)
            if r_titles and self.find_title(t, r_titles):
                found.append(t)
            print("***")

        print("{} titles found out of {}".format(len(found), len(self.titles)))
        return found
