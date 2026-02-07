"""Parallel search processing using ThreadPoolExecutor."""

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Callable, Optional


@dataclass
class SearchTask:
    """Represents a single book search task."""
    index: int
    title: str
    isbn: Optional[str] = None
    author: Optional[str] = None


class ParallelSearcher:
    """Manages parallel book searches with thread-safe operations."""

    def __init__(self, searcher, workers: int = 5, delay_ms: int = 100):
        """
        Initialize parallel searcher.

        Args:
            searcher: The BookOutletSearch instance to use
            workers: Number of concurrent workers
            delay_ms: Delay between requests in milliseconds
        """
        self.searcher = searcher
        self.workers = workers
        self.delay_ms = delay_ms
        self.lock = threading.Lock()  # For thread-safe operations

    def _search_single(self, task: SearchTask) -> Dict:
        """
        Search for a single book (thread-safe).

        Args:
            task: SearchTask containing book information

        Returns:
            Match dictionary or None
        """
        try:
            # Add delay to respect rate limiting
            if self.delay_ms > 0:
                time.sleep(self.delay_ms / 1000.0)

            # Perform search (HTTP request is thread-safe with lock in scraper)
            with self.lock:
                response = self.searcher.search(task.title, isbn=task.isbn, author=task.author)

            # Parse results
            book_data = self.searcher.parse_books(response)

            # Find best match
            found, choice, ratio, match_data = self.searcher.find_title(
                task.title,
                book_data,
                query_isbn=task.isbn,
                query_author=task.author
            )

            if book_data and found:
                result = {
                    "Query": task.title,
                    "Match": choice,
                    "Score": str(ratio) + "%",
                    "index": task.index  # Preserve order
                }

                # Add enhanced data if available
                if match_data:
                    result["Price"] = match_data.get('price', '')
                    result["URL"] = match_data.get('url', '')
                    result["CoverURL"] = match_data.get('cover_url', '')
                    result["ISBN"] = match_data.get('isbn', '')
                    result["MatchType"] = match_data.get('match_type', 'fuzzy')

                return result

            return None

        except Exception as e:
            print(f"Error searching for '{task.title}': {e}")
            return None

    def search_all_parallel(
        self,
        tasks: List[SearchTask],
        progress_callback: Optional[Callable[[int, str], None]] = None
    ) -> List[Dict]:
        """
        Search for all books in parallel.

        Args:
            tasks: List of SearchTask objects
            progress_callback: Optional callback(index, title) for progress updates

        Returns:
            List of match dictionaries (in original order)
        """
        results = []
        completed_count = 0

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            # Submit all tasks
            future_to_task = {
                executor.submit(self._search_single, task): task
                for task in tasks
            }

            # Process completed tasks
            for future in as_completed(future_to_task):
                task = future_to_task[future]
                completed_count += 1

                # Update progress
                if progress_callback:
                    progress_callback(completed_count, task.title)

                # Get result
                try:
                    result = future.result()
                    if result:
                        results.append(result)
                except Exception as e:
                    print(f"Error processing task for '{task.title}': {e}")

        # Sort results by original index to maintain order
        results.sort(key=lambda x: x.get('index', 0))

        # Remove index from final results
        for result in results:
            result.pop('index', None)

        return results
