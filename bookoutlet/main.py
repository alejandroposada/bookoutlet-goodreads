import argparse

from parse.parser import parse_books
from search.searcher import search_all_titles

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Search for books on bookoutlet')
    parser.add_argument(
        '--url', help='URL of bookshelf', required=True)
    parser.add_argument(
        '--source', help='Name of source for book list ("collison", "goodreads", "radicalreads", "favobooks")', required=True)
    parser.add_argument(
        '--store', help='Name of store ("bookoutlet", "opl", "tpl")', required=True)
    parser.add_argument(
        '--file', help='Name of the results file', required=False)
    args = parser.parse_args()

    # download and parse the webpage's book titles
    books = parse_books(args.url, args.source)

    # search each book title
    found = search_all_titles(args.store, books)

    # write found titles to disk
    if args.file:
        with open('found-{}-{}'.format(args.store, args.file), 'w') as f:
            f.write('\n'.join(found))
