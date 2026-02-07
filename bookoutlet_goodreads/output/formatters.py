"""Base output formatter class."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime


class OutputFormatter(ABC):
    """Abstract base class for output formatters."""

    @abstractmethod
    def format(self, results: List[Dict], metadata: Dict[str, Any]) -> str:
        """
        Format search results.

        Args:
            results: List of match dictionaries with Query, Match, Score keys
            metadata: Additional metadata (total_searched, threshold, etc.)

        Returns:
            Formatted string
        """
        pass

    @abstractmethod
    def get_extension(self) -> str:
        """
        Get file extension for this format (without dot).

        Returns:
            Extension string (e.g., 'txt', 'json', 'csv')
        """
        pass

    def write(self, results: List[Dict], metadata: Dict[str, Any], path: str):
        """
        Format and write results to file.

        Args:
            results: List of match dictionaries
            metadata: Additional metadata
            path: Base path (extension will be added automatically)
        """
        # Add extension if not present
        if not path.endswith('.' + self.get_extension()):
            path = f"{path}.{self.get_extension()}"

        content = self.format(results, metadata)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

        return path

    def _get_default_metadata(self) -> Dict[str, Any]:
        """Get default metadata fields."""
        return {
            'generated_at': datetime.now().isoformat(),
            'tool': 'BookOutlet-Goodreads Matcher',
        }
