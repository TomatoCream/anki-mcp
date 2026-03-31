import asyncio
import sys
import os

# Add src to path to import our package
sys.path.append(os.path.abspath("src"))

from anki_mcp.client import AnkiClient
from anki_mcp.models import NoteInput

async def main():
    client = AnkiClient()
    
    try:
        # 1. Create a demo deck
        deck_name = "MCP_Demo"
        print(f"Creating deck: {deck_name}...")
        await client.invoke("createDeck", deck=deck_name)
        
        # 2. Prepare some notes
        notes = [
            NoteInput(
                deckName=deck_name,
                modelName="Basic",
                fields={
                    "Front": "What is <b>MCP</b>?",
                    "Back": "The <i>Model Context Protocol</i>, an open standard that allows LLMs to connect to data and tools."
                },
                tags=["mcp", "tech"]
            ),
            NoteInput(
                deckName=deck_name,
                modelName="Basic",
                fields={
                    "Front": "Who created the <b>Anki MCP Server</b>?",
                    "Back": "An AI assistant using the FastMCP framework!"
                },
                tags=["mcp", "anki"]
            )
        ]
        
        # 3. Add the notes
        print("Adding notes to Anki...")
        result = await client.invoke("addNotes", notes=[n.model_dump(exclude_none=True) for n in notes])
        
        print(f"Successfully added notes! IDs: {result}")
        
        # 4. Verify by listing decks
        decks = await client.invoke("deckNames")
        if deck_name in decks:
            print(f"Verified: Deck '{deck_name}' is in your collection.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
