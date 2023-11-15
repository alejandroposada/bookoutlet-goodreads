import argparse
from bookoutlet_goodreads.search.scraper import BookOutletSearch
import pandas as pd


def main(csv_path, output_path, threshold):
    df = pd.read_csv(csv_path)
    books = list(df.loc[df["Bookshelves"] == "to-read"]["Title"])
    print(f'Loaded to-read bookshelve with {len(df)} titles.')

    searcher = BookOutletSearch(books, fuzz_thresh=threshold)
    results = searcher.search_all_titles()

    if results:
        matches = [m['Match'] for m in results]
        with open(output_path, "w") as file:
            for item in matches:
                file.write(f"{item}\n")
    else:
        matches = []

    print(f"Found {len(matches)} matches. Saved results in {output_path}.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Search titles and write matches to a file.")
    parser.add_argument("--csv", help="Path to the CSV file", default="goodreads_library_export.csv")
    parser.add_argument("--output", help="Path to the output file", default="output.txt")
    parser.add_argument("--threshold", help="Fuzz threshold for searching", type=int, default=100)

    args = parser.parse_args()
    main(args.csv, args.output, args.threshold)
