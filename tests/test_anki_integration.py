import pytest
import asyncio
from anki_mcp.client import AnkiClient
from anki_mcp.models import NoteInput, NoteUpdateInput

# This requires Anki-Connect to be running locally at http://localhost:8765
@pytest.fixture
def client():
    return AnkiClient()

@pytest.mark.asyncio
async def test_ping(client):
    version = await client.invoke("version")
    assert isinstance(version, int)

@pytest.mark.asyncio
async def test_deck_management(client):
    deck_name = "TEST_DECK_PYTEST"
    
    # Create deck
    await client.invoke("createDeck", deck=deck_name)
    
    # Verify deck exists
    decks = await client.invoke("deckNames")
    assert deck_name in decks
    
    # Clean up (Anki doesn't have a direct 'deleteDeck' in base Anki-Connect 
    # but we can check if it's there)
    assert deck_name in decks

@pytest.mark.asyncio
async def test_note_lifecycle(client):
    deck_name = "TEST_DECK_PYTEST"
    model_name = "Basic"
    
    # 1. Add Note
    note = NoteInput(
        deckName=deck_name,
        modelName=model_name,
        fields={"Front": "Pytest Question", "Back": "Pytest Answer"},
        tags=["pytest", "test"]
    )
    note_id = await client.invoke("addNote", note=note.model_dump(exclude_none=True))
    assert isinstance(note_id, int)
    
    # 2. Get Note Info
    notes_info = await client.invoke("notesInfo", notes=[note_id])
    assert len(notes_info) == 1
    assert notes_info[0]["fields"]["Front"]["value"] == "Pytest Question"
    
    # 3. Update Note
    update = NoteUpdateInput(
        id=note_id,
        fields={"Front": "Updated Question"}
    )
    await client.invoke("updateNoteFields", note=update.model_dump(exclude_none=True))
    
    # 4. Verify Update
    notes_info_updated = await client.invoke("notesInfo", notes=[note_id])
    assert notes_info_updated[0]["fields"]["Front"]["value"] == "Updated Question"
    
    # 5. Delete Note
    await client.invoke("deleteNotes", notes=[note_id])
    
    # 6. Verify Deletion
    notes_info_deleted = await client.invoke("notesInfo", notes=[note_id])
    assert not notes_info_deleted[0]
