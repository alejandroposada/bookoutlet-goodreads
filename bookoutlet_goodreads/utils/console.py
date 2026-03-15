"""Rich console utilities for beautiful terminal output."""

from typing import List, Dict

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text

# Shared console instance
console = Console()


def print_results_table(results: List[Dict], threshold: int = 90):
    """
    Print search results in a beautiful rich table with color-coded scores.

    Args:
        results: List of match dictionaries with Query, Match, Score keys
        threshold: The threshold used for matching (for context)
    """
    if not results:
        console.print("[yellow]No matches found.[/yellow]")
        return

    table = Table(
        title="Book Matches Found",
        show_header=True,
        header_style="bold magenta",
        border_style="blue",
        title_style="bold cyan",
    )

    table.add_column("Goodreads Title", style="cyan", no_wrap=False, max_width=40)
    table.add_column("BookOutlet Match", style="green", no_wrap=False, max_width=40)
    table.add_column("Score", justify="right", style="yellow")

    for item in results:
        query = item.get("Query", "N/A")
        match = item.get("Match", "N/A")
        score_str = item.get("Score", "0%")

        # Extract numeric score for color coding
        score_num = int(score_str.rstrip('%'))

        # Color code the score
        if score_num >= 95:
            score_style = "bold green"
        elif score_num >= 90:
            score_style = "green"
        elif score_num >= 85:
            score_style = "yellow"
        else:
            score_style = "red"

        score_text = Text(score_str, style=score_style)

        table.add_row(query, match, score_text)

    console.print(table)


def print_summary(found: int, total: int, output_path: str, threshold: int = 90):
    """
    Print a summary panel with search statistics.

    Args:
        found: Number of matches found
        total: Total number of books searched
        output_path: Path where results were saved
        threshold: The threshold used for matching
    """
    percentage = (found / total * 100) if total > 0 else 0

    summary_text = f"""
[bold cyan]Search Complete![/bold cyan]

[bold]Matches Found:[/bold] {found} out of {total} books ({percentage:.1f}%)
[bold]Threshold:[/bold] {threshold}%
[bold]Results saved to:[/bold] {output_path}
"""

    # Choose color based on success rate
    if percentage >= 50:
        border_style = "green"
    elif percentage >= 25:
        border_style = "yellow"
    else:
        border_style = "red"

    panel = Panel(
        summary_text.strip(),
        border_style=border_style,
        title="Summary",
        title_align="left",
    )

    console.print(panel)


def print_search_header(total: int, csv_path: str, threshold: int):
    """
    Print a header at the start of the search.

    Args:
        total: Total number of books to search
        csv_path: Path to the CSV file
        threshold: The matching threshold
    """
    console.print()
    console.rule("[bold blue]BookOutlet-Goodreads Matcher[/bold blue]")
    console.print(f"[cyan]Loading books from:[/cyan] {csv_path}")
    console.print(f"[cyan]Books to search:[/cyan] {total}")
    console.print(f"[cyan]Match threshold:[/cyan] {threshold}%")
    console.rule()
    console.print()


def print_csv_not_found(csv_path: str):
    """
    Print a helpful error message when the Goodreads CSV is not found.

    Args:
        csv_path: The path that was searched
    """
    message = f"""[bold red]Goodreads CSV not found:[/bold red] [yellow]{csv_path}[/yellow]

[bold]To export your Goodreads library:[/bold]
  1. Go to [link=https://www.goodreads.com/review/import]https://www.goodreads.com/review/import[/link]
  2. Scroll down and click [bold]"Export Library"[/bold]
  3. Save the downloaded file as [bold]goodreads_library_export.csv[/bold] in this directory

Or point to an existing export:
  [cyan]python run.py --csv /path/to/your/export.csv[/cyan]"""

    panel = Panel(
        message,
        border_style="red",
        title="CSV Not Found",
        title_align="left",
    )
    console.print(panel)


def print_csv_autodetected(original_path: str, detected_path: str):
    """
    Print a notice when a CSV was auto-detected instead of the configured path.

    Args:
        original_path: The originally configured path
        detected_path: The auto-detected path that will be used
    """
    console.print(
        f"[yellow]Note:[/yellow] [cyan]{original_path}[/cyan] not found — "
        f"using [green]{detected_path}[/green] instead"
    )


def print_match_info(title: str, found: bool, match: str, score: int):
    """
    Print individual match information with color coding.

    Args:
        title: The query title
        found: Whether a match was found
        match: The matched title
        score: The match score (0-100)
    """
    if found:
        if score >= 95:
            console.print(f"[bold green]✓[/bold green] {title} → {match} ([bold green]{score}%[/bold green])")
        else:
            console.print(f"[green]✓[/green] {title} → {match} ([green]{score}%[/green])")
    else:
        console.print(f"[red]✗[/red] {title} - No match found")
