"""
Anki Connect MCP Server
Powered by Anki-Connect: https://git.sr.ht/~foosoft/anki-connect
"""
from typing import Dict, List, Optional, Any, Union, Annotated
from fastmcp import FastMCP
import typer
from rich.console import Console
from rich.table import Table
import asyncio
from .client import AnkiClient
from .models import NoteInput, NoteUpdateInput, NoteInfo, CardInfo

# Initialize Console for rich output
console = Console()

# Create the FastMCP server
mcp = FastMCP(
    "Anki Connect MCP Server",
    instructions="A Model Context Protocol server that allows LLMs to interact with Anki via the Anki-Connect plugin. "
                 "It supports creating notes, searching cards, and managing decks with full type safety and documentation."
)

# Default Anki Client (will be re-initialized in run command)
anki = AnkiClient()

# Shared CLI option for Anki-Connect URL
URL_OPTION = typer.Option("http://localhost:8765", "--url", help="Anki-Connect URL")

def _run(coro):
    """Run an async coroutine synchronously."""
    return asyncio.run(coro)

def _client(url: str) -> AnkiClient:
    """Create an AnkiClient for CLI commands."""
    return AnkiClient(url=url)


# ── MCP Tools ──────────────────────────────────────────────────────

@mcp.tool()
async def ping() -> str:
    """
    Checks if Anki-Connect is reachable and running.

    Returns:
        A success message or raises an exception if unreachable.
    """
    await anki.invoke("version")
    return "Anki-Connect is online and reachable."

@mcp.tool()
async def add_note(note: NoteInput) -> int:
    """
    Adds a single note to Anki.

    Args:
        note: The note object containing deckName, modelName, fields, and optional tags/media.
              The fields dictionary should map field names (e.g., 'Front') to their content.

    Returns:
        The unique ID of the newly created note.
    """
    return await anki.invoke("addNote", note=note.model_dump(exclude_none=True))

@mcp.tool()
async def add_notes(notes: List[NoteInput]) -> List[Optional[int]]:
    """
    Adds multiple notes to Anki in a single batch request for efficiency.

    Args:
        notes: A list of NoteInput objects.

    Returns:
        A list of note IDs. If a note fails to be added, its corresponding entry in the list will be null.
    """
    return await anki.invoke("addNotes", notes=[n.model_dump(exclude_none=True) for n in notes])

@mcp.tool()
async def find_notes(query: str) -> List[int]:
    """
    Finds note IDs matching a given Anki search query.

    Args:
        query: Anki search query (e.g., 'deck:Default', 'tag:marked', 'apple').
               See Anki documentation for search syntax.

    Returns:
        A list of matching note IDs.
    """
    return await anki.invoke("findNotes", query=query)

@mcp.tool()
async def notes_info(notes: List[int]) -> List[Optional[NoteInfo]]:
    """
    Retrieves detailed information for a list of note IDs.

    Args:
        notes: A list of note IDs to fetch information for.

    Returns:
        A list of NoteInfo objects containing the note's fields, tags, and model information.
    """
    result = await anki.invoke("notesInfo", notes=notes)
    return [NoteInfo(**n) if n else None for n in result]

@mcp.tool()
async def update_note_fields(note: NoteUpdateInput) -> str:
    """
    Updates the fields or tags of an existing note.

    Args:
        note: An object containing the note 'id' and the new 'fields' or 'tags'.

    Returns:
        A success message.
    """
    await anki.invoke("updateNoteFields", note=note.model_dump(exclude_none=True))
    return f"Note {note.id} updated successfully."

@mcp.tool()
async def delete_notes(notes: List[int]) -> str:
    """
    Deletes the specified notes and their associated cards.

    Args:
        notes: A list of note IDs to be deleted.

    Returns:
        A success message.
    """
    await anki.invoke("deleteNotes", notes=notes)
    return f"Successfully deleted {len(notes)} notes."

@mcp.tool()
async def find_cards(query: str) -> List[int]:
    """
    Finds card IDs matching a given Anki search query.

    Args:
        query: Anki search query.

    Returns:
        A list of matching card IDs.
    """
    return await anki.invoke("findCards", query=query)

@mcp.tool()
async def cards_info(cards: List[int]) -> List[Optional[CardInfo]]:
    """
    Retrieves detailed information for a list of card IDs, including their rendered HTML.

    Args:
        cards: A list of card IDs.

    Returns:
        A list of CardInfo objects.
    """
    result = await anki.invoke("cardsInfo", cards=cards)
    return [CardInfo(**c) if c else None for c in result]

@mcp.tool()
async def deck_names() -> List[str]:
    """
    Lists all available deck names in the current Anki profile.

    Returns:
        A list of deck names as strings.
    """
    return await anki.invoke("deckNames")

@mcp.tool()
async def create_deck(deck: str) -> int:
    """
    Creates a new deck with the specified name.

    Args:
        deck: The name of the deck to create (e.g., 'Languages::Spanish').

    Returns:
        The ID of the newly created deck.
    """
    return await anki.invoke("createDeck", deck=deck)

@mcp.tool()
async def model_names() -> List[str]:
    """
    Lists all available note type (model) names.

    Returns:
        A list of model names.
    """
    return await anki.invoke("modelNames")

@mcp.tool()
async def model_field_names(modelName: str) -> List[str]:
    """
    Lists all field names for a specific note type (model).

    Args:
        modelName: The name of the note type (e.g., 'Basic').

    Returns:
        A list of field names.
    """
    return await anki.invoke("modelFieldNames", modelName=modelName)


# ── CLI Commands ───────────────────────────────────────────────────

app = typer.Typer(help="Anki Connect MCP Server & CLI")

@app.command()
def run(
    url: str = typer.Option("http://localhost:8765", help="Anki-Connect URL"),
    version: int = typer.Option(6, help="Anki-Connect version")
):
    """Run the Anki MCP server over stdio."""
    global anki
    anki = AnkiClient(url=url, version=version)
    console.print(f"[bold green]Starting Anki MCP Server connecting to {url}[/bold green]")
    mcp.run()

@app.command("ping")
def cli_ping(url: str = URL_OPTION):
    """Check if Anki-Connect is reachable."""
    try:
        version = _run(_client(url).invoke("version"))
        console.print(f"[bold green]Anki-Connect is online (version {version})[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("decks")
def cli_decks(url: str = URL_OPTION):
    """List all deck names."""
    try:
        result = _run(_client(url).invoke("deckNames"))
        for name in sorted(result):
            console.print(name)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("models")
def cli_models(url: str = URL_OPTION):
    """List all note type (model) names."""
    try:
        result = _run(_client(url).invoke("modelNames"))
        for name in sorted(result):
            console.print(name)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("fields")
def cli_fields(
    model: str = typer.Argument(help="Note type (model) name, e.g. 'Basic'"),
    url: str = URL_OPTION,
):
    """List field names for a note type."""
    try:
        result = _run(_client(url).invoke("modelFieldNames", modelName=model))
        for name in result:
            console.print(name)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("find")
def cli_find(
    query: str = typer.Argument(help="Anki search query, e.g. 'deck:Default'"),
    url: str = URL_OPTION,
):
    """Find note IDs matching an Anki search query."""
    try:
        result = _run(_client(url).invoke("findNotes", query=query))
        if not result:
            console.print("[dim]No notes found.[/dim]")
            return
        console.print(f"[dim]{len(result)} note(s) found:[/dim]")
        for nid in result:
            console.print(str(nid))
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("info")
def cli_info(
    note_ids: List[int] = typer.Argument(help="One or more note IDs"),
    url: str = URL_OPTION,
):
    """Show detailed info for one or more notes."""
    try:
        result = _run(_client(url).invoke("notesInfo", notes=note_ids))
        for note_data in result:
            if not note_data:
                continue
            note = NoteInfo(**note_data)
            table = Table(title=f"Note {note.noteId}", show_header=True)
            table.add_column("Field", style="bold")
            table.add_column("Value")
            for fname, finfo in note.fields.items():
                table.add_row(fname, finfo.value)
            console.print(table)
            console.print(f"  [dim]Model:[/dim] {note.modelName}")
            console.print(f"  [dim]Tags:[/dim]  {', '.join(note.tags) if note.tags else '(none)'}")
            console.print(f"  [dim]Cards:[/dim] {', '.join(str(c) for c in note.cards)}")
            console.print()
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("add")
def cli_add(
    deck: str = typer.Option(..., "--deck", "-d", help="Target deck name"),
    model: str = typer.Option(..., "--model", "-m", help="Note type (model) name"),
    field: List[str] = typer.Option(..., "--field", "-f", help="Field value as 'Name=Content' (repeat for each field)"),
    tag: Optional[List[str]] = typer.Option(None, "--tag", "-t", help="Tag to add (repeat for multiple)"),
    url: str = URL_OPTION,
):
    """Add a note to Anki.

    Example: anki-mcp add -d Default -m Basic -f 'Front=hello' -f 'Back=world' -t vocab
    """
    fields_dict: Dict[str, str] = {}
    for f in field:
        if "=" not in f:
            console.print(f"[bold red]Error:[/bold red] Field must be 'Name=Content', got: {f}")
            raise typer.Exit(1)
        key, value = f.split("=", 1)
        fields_dict[key] = value

    note_data = {
        "deckName": deck,
        "modelName": model,
        "fields": fields_dict,
        "tags": tag or [],
    }
    try:
        note = NoteInput(**note_data)
        nid = _run(_client(url).invoke("addNote", note=note.model_dump(exclude_none=True)))
        console.print(f"[bold green]Note created:[/bold green] {nid}")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("delete")
def cli_delete(
    note_ids: List[int] = typer.Argument(help="Note IDs to delete"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation"),
    url: str = URL_OPTION,
):
    """Delete notes by ID."""
    if not yes:
        confirm = typer.confirm(f"Delete {len(note_ids)} note(s)?")
        if not confirm:
            raise typer.Abort()
    try:
        _run(_client(url).invoke("deleteNotes", notes=note_ids))
        console.print(f"[bold green]Deleted {len(note_ids)} note(s).[/bold green]")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

@app.command("create-deck")
def cli_create_deck(
    name: str = typer.Argument(help="Deck name, e.g. 'Languages::Spanish'"),
    url: str = URL_OPTION,
):
    """Create a new deck."""
    try:
        deck_id = _run(_client(url).invoke("createDeck", deck=name))
        console.print(f"[bold green]Deck created:[/bold green] {name} (id: {deck_id})")
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
