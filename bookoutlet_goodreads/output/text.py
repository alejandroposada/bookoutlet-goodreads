"""Text output formatter (maintains backward compatibility)."""

from typing import List, Dict, Any

from .formatters import OutputFormatter


class TextFormatter(OutputFormatter):
    """Format results as plain text (original format)."""

    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format results as plain text lines.

        Example output:
            BookOutlet: The Song of Achilles by Madeline Miller, Goodreads: The Song of Achilles, Match Score: 98%
        """
        if not results:
            return "No matches found.\n"

        lines = []
        for item in results:
            line = f"BookOutlet: {item['Match']}, Goodreads: {item['Query']}, Match Score: {item['Score']}"
            lines.append(line)

        return '\n'.join(lines) + '\n'

    def get_extension(self) -> str:
        """Return 'txt' extension."""
        return 'txt'
