import argparse
from pathlib import Path

import pandas as pd

from bookoutlet_goodreads.search.scraper import BookOutletSearch
from bookoutlet_goodreads.search.parallel import ParallelSearcher, SearchTask
from bookoutlet_goodreads.utils.isbn import extract_isbn_from_excel_formula
from bookoutlet_goodreads.utils.progress import create_search_progress
from bookoutlet_goodreads.utils.console import (
    console,
    print_results_table,
    print_summary,
    print_search_header,
)
from bookoutlet_goodreads.config import load_config
from bookoutlet_goodreads.output import get_formatter


def main(config_path=None, cli_overrides=None):
    """Main entry point with configuration support."""

    # Load configuration with CLI overrides
    config = load_config(config_path=config_path, cli_overrides=cli_overrides)

    # Load the CSV
    csv_path = config.input.csv_path
    df = pd.read_csv(csv_path)

    # Filter for specified bookshelf
    to_read_df = df.loc[df["Bookshelves"] == config.input.bookshelf]

    # Extract book data with title, author, and ISBN
    book_data = []
    for _, row in to_read_df.iterrows():
        book = {
            'title': row['Title'],
            'author': row.get('Author', ''),
        }

        # Extract ISBN from either ISBN or ISBN13 column (prefer ISBN13)
        if config.matching.use_isbn:
            isbn13 = extract_isbn_from_excel_formula(str(row.get('ISBN13', '')))
            isbn = extract_isbn_from_excel_formula(str(row.get('ISBN', '')))
            book['isbn'] = isbn13 or isbn
        else:
            book['isbn'] = None

        book_data.append(book)

    # Get just the titles for the searcher
    titles = [book['title'] for book in book_data]

    # Print header
    if config.display.show_progress:
        print_search_header(len(titles), csv_path, config.matching.threshold)

    # Create searcher with full book data
    searcher = BookOutletSearch(
        titles,
        fuzz_thresh=config.matching.threshold,
        book_data=book_data,
        require_author_match=config.matching.require_author_match,
        site=config.search.site
    )

    # Search with optional parallel processing
    results = []

    if config.parallel.enabled and len(titles) > 1:
        # Parallel execution
        tasks = [
            SearchTask(index=i, title=book['title'], isbn=book.get('isbn'), author=book.get('author'))
            for i, book in enumerate(book_data)
        ]

        parallel_searcher = ParallelSearcher(
            searcher,
            workers=config.parallel.workers,
            delay_ms=config.parallel.delay_ms
        )

        if config.display.show_progress:
            with create_search_progress(len(tasks)) as (progress, task):
                def progress_callback(current, title):
                    short_title = title[:50] + "..." if len(title) > 50 else title
                    progress.update(
                        task,
                        advance=1,
                        description=f"Searching books... [cyan]{short_title}[/cyan]"
                    )

                results = parallel_searcher.search_all_parallel(tasks, progress_callback)
        else:
            results = parallel_searcher.search_all_parallel(tasks)

    else:
        # Sequential execution (original behavior)
        if config.display.show_progress:
            with create_search_progress(len(titles)) as (progress, task):
                def progress_callback(current, title):
                    short_title = title[:50] + "..." if len(title) > 50 else title
                    progress.update(
                        task,
                        advance=1,
                        description=f"Searching books... [cyan]{short_title}[/cyan]"
                    )

                results = searcher.search_all_titles(progress_callback=progress_callback)
        else:
            results = searcher.search_all_titles()

    # Prepare metadata for formatters
    metadata = {
        'total_searched': len(titles),
        'total_matches': len(results),
        'threshold': config.matching.threshold,
        'parallel_enabled': config.parallel.enabled,
        'workers': config.parallel.workers if config.parallel.enabled else 1,
    }

    # Get formatter and write output
    formatter = get_formatter(config.output.format)
    output_path = formatter.write(results, metadata, config.output.path)

    if config.display.show_progress:
        console.print()  # Add spacing

        # Print beautiful results table
        print_results_table(results, config.matching.threshold)

        console.print()  # Add spacing

        # Print summary
        print_summary(len(results), len(titles), output_path, config.matching.threshold)


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Search BookOutlet for books from your Goodreads to-read shelf.",
        epilog="Configuration priority: CLI args > config.local.yaml > config.yaml > defaults"
    )

    parser.add_argument(
        "--config",
        help="Path to configuration YAML file",
        default=None
    )

    parser.add_argument(
        "--csv",
        help="Path to the Goodreads CSV export file",
        default=None
    )

    parser.add_argument(
        "--output",
        help="Path to the output file (extension added automatically)",
        default=None
    )

    parser.add_argument(
        "--threshold",
        help="Minimum match score (0-100)",
        type=int,
        default=None
    )

    parser.add_argument(
        "--format",
        help="Output format: text, json, csv, markdown, html",
        choices=['text', 'json', 'csv', 'markdown', 'html'],
        default=None
    )

    parser.add_argument(
        "--parallel",
        help="Enable parallel processing (true/false)",
        type=lambda x: x.lower() == 'true',
        default=None
    )

    parser.add_argument(
        "--workers",
        help="Number of parallel workers (1-20)",
        type=int,
        default=None
    )

    parser.add_argument(
        "--no-progress",
        help="Disable progress bar",
        action="store_true"
    )

    parser.add_argument(
        "--site",
        help="BookOutlet site: ca (Canada) or com (US)",
        choices=['ca', 'com'],
        default=None
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # Build CLI overrides dictionary
    cli_overrides = {}

    if args.csv:
        cli_overrides.setdefault('input', {})['csv_path'] = args.csv

    if args.output:
        cli_overrides.setdefault('output', {})['path'] = args.output

    if args.format:
        cli_overrides.setdefault('output', {})['format'] = args.format

    if args.threshold is not None:
        cli_overrides.setdefault('matching', {})['threshold'] = args.threshold

    if args.parallel is not None:
        cli_overrides.setdefault('parallel', {})['enabled'] = args.parallel

    if args.workers:
        cli_overrides.setdefault('parallel', {})['workers'] = args.workers

    if args.no_progress:
        cli_overrides.setdefault('display', {})['show_progress'] = False

    if args.site:
        cli_overrides.setdefault('search', {})['site'] = args.site

    # Run main with configuration
    main(config_path=args.config, cli_overrides=cli_overrides)
