# Anki Connect MCP Server

A high-quality Model Context Protocol (MCP) server that provides a bridge between LLMs (like Claude) and [Anki](https://apps.ankiweb.net/) via the [Anki-Connect](https://ankiweb.net/shared/info/2055492159) plugin.

Built with:
- `python 3.12+`
- `FastMCP` (from Model Context Protocol ecosystem)
- `Pydantic v2` for strong typing and validation
- `Typer` and `Rich` for CLI interaction

## Features

- **Notes Management**: Add, search, update, and delete notes.
- **Card Inspection**: Find cards and get detailed rendering (HTML question/answer).
- **Deck & Model Support**: List decks, create decks, and explore note types.
- **Strong Typing**: Every tool uses Pydantic models for request/response, allowing LLMs to understand the inputs and outputs perfectly.
- **Well Documented**: Extensive docstrings and field descriptions specifically tailored for LLM consumption.

## Prerequisites

1.  **Anki** must be installed and running.
2.  **Anki-Connect** add-on must be installed in Anki (Add-on code: `2055492159`).
3.  **Python 3.12** or higher.
4.  **uv** (recommended) for package management.

## Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/org-anki.git
cd org-anki/anki-mcp

# Install dependencies and the package
uv pip install -e .
```

### Running the Server

The server communicates via `stdio` by default, which is the standard for MCP.

```bash
# From the anki-mcp directory
uv run anki-mcp --url http://localhost:8765
```

## Integration with Claude Desktop

To use this server in Claude Desktop, add the following to your `claude_desktop_config.json` (on Linux, usually at `~/.config/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "anki": {
      "command": "uv",
      "args": [
        "run",
        "--project",
        "/path/to/your/org-anki/anki-mcp",
        "anki-mcp"
      ]
    }
  }
}
```

*Replace `/path/to/your/org-anki/` with the absolute path to where you cloned the repository.*

## Available Tools

- `ping`: Check connectivity to Anki-Connect.
- `add_note`: Create a single note with fields, tags, and media.
- `add_notes`: Batch add multiple notes.
- `find_notes`: Search for notes using Anki's search syntax.
- `notes_info`: Get full note data (fields, tags, cards).
- `update_note_fields`: Modify fields or tags of an existing note.
- `delete_notes`: Remove notes from the collection.
- `find_cards`: Search for specific cards.
- `cards_info`: Get card details (HTML, interval, etc.).
- `deck_names`: List all decks.
- `create_deck`: Create a new deck.
- `model_names`: List all note types.
- `model_field_names`: List fields for a specific note type.

## Development

To run the server in development mode with the **FastMCP Inspector** (web debugger):

```bash
uv run fastmcp dev src/anki_mcp/main.py
```
This will launch a web interface where you can manually test all tools.
