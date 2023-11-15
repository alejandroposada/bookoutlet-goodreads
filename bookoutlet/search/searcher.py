import argparse
from typing import List

from search.bookoutlet import BookOutletSearch
from search.opl import OttawaLibrarySearch
from search.tpl import TorontoLibrarySearch


def search_all_titles(store: str, titles: List[str]) -> List[str]:
    if store == 'bookoutlet':
        searcher = BookOutletSearch(titles)
    elif store == 'opl':
        searcher = OttawaLibrarySearch(titles)
    elif store == 'tpl':
        searcher = TorontoLibrarySearch(titles)
    else:
        raise ValueError("Invalid store provided!")
    return searcher.search_all_titles()

if __name__ == "__main__":
    # read list of titles from txt file
    parser = argparse.ArgumentParser(description = 'Search a list of titles from a file')
    parser.add_argument('store', help='Name of store ("bookoutlet", "opl", "tpl")')
    parser.add_argument('file', help='Text file with list of books to search')
    args = parser.parse_args()
    with open(args.file) as f:
        titles = [l.strip() for l in f]

    # perform searches
    found = search_all_titles(args.store, titles)

    # write found to disk
    with open('found-{}-{}'.format(args.store, args.file), 'w') as f:
        f.write('\n'.join(found))

