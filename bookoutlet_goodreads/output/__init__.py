"""Output formatters for search results."""

from .formatters import OutputFormatter
from .text import TextFormatter
from .csv_formatter import CSVFormatter
from .json_formatter import JSONFormatter
from .markdown import MarkdownFormatter
from .html_interactive import HTMLInteractiveFormatter

# Formatter registry
FORMATTERS = {
    'text': TextFormatter,
    'csv': CSVFormatter,
    'json': JSONFormatter,
    'markdown': MarkdownFormatter,
    'html': HTMLInteractiveFormatter,
}


def get_formatter(format_name: str) -> OutputFormatter:
    """
    Get formatter instance by name.

    Args:
        format_name: The format name (text, csv, json, markdown, html)

    Returns:
        OutputFormatter instance

    Raises:
        ValueError: If format is not supported
    """
    formatter_class = FORMATTERS.get(format_name.lower())
    if not formatter_class:
        available = ', '.join(FORMATTERS.keys())
        raise ValueError(f"Unknown format '{format_name}'. Available: {available}")

    return formatter_class()


__all__ = [
    'OutputFormatter',
    'TextFormatter',
    'CSVFormatter',
    'JSONFormatter',
    'MarkdownFormatter',
    'HTMLInteractiveFormatter',
    'get_formatter',
    'FORMATTERS',
]
