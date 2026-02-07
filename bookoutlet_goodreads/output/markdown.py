"""Markdown output formatter."""

from typing import List, Dict, Any

from .formatters import OutputFormatter


class MarkdownFormatter(OutputFormatter):
    """Format results as GitHub-flavored Markdown."""

    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format results as Markdown table.

        Example:
        # BookOutlet Matches

        Found 45 matches out of 230 books (threshold: 90%).

        | Goodreads Title | BookOutlet Match | Score |
        |---|---|---|
        | The Song of Achilles | The Song of Achilles by Madeline Miller | 98% |
        """
        # Build header
        lines = ['# BookOutlet Matches\n']

        total_searched = metadata.get('total_searched', len(results))
        threshold = metadata.get('threshold', 90)

        summary = f"Found **{len(results)}** matches out of **{total_searched}** books (threshold: {threshold}%).\n"
        lines.append(summary)

        if not results:
            lines.append("_No matches found._\n")
            return '\n'.join(lines)

        # Build table
        lines.append("| Goodreads Title | BookOutlet Match | Score | Price | Link |")
        lines.append("|---|---|---|---|---|")

        for item in results:
            query = self._escape_markdown(item.get('Query', ''))
            match = self._escape_markdown(item.get('Match', ''))
            score = item.get('Score', '')
            price = item.get('Price', '')
            url = item.get('URL', '')

            # Create link if URL available
            link = f"[View]({url})" if url else ""

            row = f"| {query} | {match} | {score} | {price} | {link} |"
            lines.append(row)

        return '\n'.join(lines) + '\n'

    def _escape_markdown(self, text: str) -> str:
        """Escape markdown special characters."""
        # Escape pipe characters for table cells
        return text.replace('|', '\\|')

    def get_extension(self) -> str:
        """Return 'md' extension."""
        return 'md'
