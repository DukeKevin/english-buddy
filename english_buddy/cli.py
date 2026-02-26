from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from .models import BuddyResponse

console = Console()


def display_response(resp: BuddyResponse) -> None:
    console.print()

    # Child-friendly translations
    for i, t in enumerate(resp.child_friendly_translation, 1):
        console.print(Panel(t, title=f"Expression {i}", style="bold green"))

    # Explanation
    console.print(f"\n[yellow]Why this works:[/yellow] {resp.explanation}")

    # Related sentences table
    table = Table(title="Related Sentences", show_lines=True)
    table.add_column("English", style="cyan")
    table.add_column("Chinese", style="white")
    for s in resp.related_sentences:
        table.add_row(s.english, s.chinese)
    console.print(table)

    # Pronunciation hints
    console.print(f"\n[magenta]Pronunciation:[/magenta] {resp.pronunciation_hints}")
    console.print()


def get_input() -> str:
    return console.input("[bold blue]Describe a scene in Chinese > [/bold blue]")


def show_spinner():
    return console.status("[cyan]Thinking...", spinner="dots")
