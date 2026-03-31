"""
Anki Connect MCP Server
Powered by Anki-Connect: https://git.sr.ht/~foosoft/anki-connect
"""
from typing import Dict, List, Optional, Any, Union
from fastmcp import FastMCP
import typer
from rich.console import Console
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

app = typer.Typer(help="Anki Connect MCP Server")

@app.command()
def run(
    url: str = typer.Option("http://localhost:8765", help="Anki-Connect URL"),
    version: int = typer.Option(6, help="Anki-Connect version")
):
    """Run the Anki MCP server over stdio"""
    global anki
    anki = AnkiClient(url=url, version=version)
    console.print(f"[bold green]Starting Anki MCP Server connecting to {url}[/bold green]")
    mcp.run()

if __name__ == "__main__":
    app()
