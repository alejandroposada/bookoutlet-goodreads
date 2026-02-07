"""Progress tracking utilities using Rich library."""

from contextlib import contextmanager
from typing import Optional

from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
    TimeRemainingColumn,
    TimeElapsedColumn,
)


@contextmanager
def create_search_progress(total: int, description: str = "Searching books"):
    """
    Create a rich progress bar context for book searching.

    Args:
        total: Total number of books to search
        description: Description text for the progress bar

    Yields:
        Tuple of (Progress object, task_id)

    Example:
        >>> with create_search_progress(230) as (progress, task):
        ...     for i in range(230):
        ...         progress.update(task, advance=1, description=f"Searching: {titles[i]}")
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TextColumn("•"),
        TimeElapsedColumn(),
        TextColumn("•"),
        TimeRemainingColumn(),
        expand=False,
    )

    with progress:
        task_id = progress.add_task(description, total=total)
        yield progress, task_id


def create_simple_progress(total: int, description: str = "Processing") -> tuple[Progress, int]:
    """
    Create a simple progress bar without context manager (for manual control).

    Args:
        total: Total number of items
        description: Description text

    Returns:
        Tuple of (Progress object, task_id)
    """
    progress = Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
    )

    progress.start()
    task_id = progress.add_task(description, total=total)
    return progress, task_id
