# -*- coding: utf-8 -*-
import argparse
import re

import cloudscraper
from bs4 import BeautifulSoup


def parse_books(url: str, source: str) -> str:
    """
    Parse the list of titles from a URL.
    """
    scraper = cloudscraper.CloudScraper()
    data = scraper.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    if source == 'collison':
        return collison(soup)
    if source == 'goodreads':
        return goodreads(soup)
    if source == 'radicalreads':
        return radicalreads(soup)
    if source == 'favobooks':
        return favobooks(soup)
    raise ValueError('Unknown book list source!')


def collison(soup, include={'teal', 'green'}):
    """
    We can also filter books by the colour coding.
    Ignore the blue-coded books by default.
    """
    categories = {
        'blue': 'a',
        'teal': 'i',  # substantially above average
        'green': 'b'  # particularly great!
    }

    # only get external urls
    tags = soup.find_all(lambda x: x.name ==
                         'a' and x.get('href', '')[:4] == 'http')
    titles = []

    for category, ident in categories.items():
        if category in include:
            filtered_tags = list(
                filter(lambda x: x.next_element.name == ident, tags))
            titles.extend([x.text.strip() for x in filtered_tags])

    return set(titles)


def goodreads(soup):
    """
    Read the book titles from the image alt text.
    """
    tags = soup.find_all(lambda x: x.next_element.name ==
                         'img' and '/book/show/' in x.get('href', ''))
    titles = set(map(lambda x: x.img.get('alt').strip(), tags))
    return titles


def radicalreads(soup):
    """
    Get book titles from a radical reads page.
    """
    content = soup.find(lambda x: x.name == 'div' and x.get(
        'class') == ['entry-content'])
    tags = content.find_all(
        lambda x: x.name == 'a' and 'https://www.amazon' in x.get('href', ''))
    titles = set(map(lambda x: x.text.strip(), tags))
    return titles


def favobooks(soup):
    """
    Get book titles from a favobooks page.
    """
    rows = soup.find(lambda x: x.name == 'div' and x.get('id')
                     == 'page').find('table').findAll('tr')
    tags = [row.find(lambda x: x.name == 'td' and x.get(
        'class', []) == ['opisanie']).find('a') for row in rows]
    pattern = re.compile('(?<=").*(?=")')
    titles = set()
    for tag in tags:
        title = tag.text.replace(u'\u201c', '"').replace(u'\u201d', '"')
        match = re.search(pattern, title)
        if match:
            titles.add(match.group(0))
    return titles


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Parse a list of books from a webpage')
    parser.add_argument(
        'url', help='URL of bookshelf')
    parser.add_argument(
        'source', help='Name of source for book list ("collison", "goodreads", "radicalreads", "favobooks")')
    parser.add_argument(
        '--file', help='Name of the results file', required=False)
    args = parser.parse_args()

    titles = parse_books(args.url, args.source)

    if args.file:
        with open(args.file, 'w') as f:
            f.write('\n'.join(titles))
