"""CSV output formatter."""

import csv
from io import StringIO
from typing import List, Dict, Any

from .formatters import OutputFormatter


class CSVFormatter(OutputFormatter):
    """Format results as CSV."""

    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format results as CSV with headers.

        Columns: Goodreads Title, BookOutlet Match, Score, Price, URL
        """
        if not results:
            return "Goodreads Title,BookOutlet Match,Score\nNo matches found,,\n"

        output = StringIO()
        writer = csv.writer(output)

        # Write header
        headers = ['Goodreads Title', 'BookOutlet Match', 'Score', 'Price', 'URL']
        writer.writerow(headers)

        # Write rows
        for item in results:
            row = [
                item.get('Query', ''),
                item.get('Match', ''),
                item.get('Score', ''),
                item.get('Price', ''),
                item.get('URL', ''),
            ]
            writer.writerow(row)

        return output.getvalue()

    def get_extension(self) -> str:
        """Return 'csv' extension."""
        return 'csv'
