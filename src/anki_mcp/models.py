from __future__ import annotations
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class MediaInput(BaseModel):
    """
    Input for media files (audio, video, picture) to be stored in Anki.
    """
    url: Optional[str] = Field(None, description="The URL from where the file will be downloaded. Use this for remote files.")
    path: Optional[str] = Field(None, description="The absolute file path to the media file on the local system. Use this for local files.")
    data: Optional[str] = Field(None, description="The base64-encoded contents of the file. Use this if you have the file content already.")
    filename: str = Field(..., description="The name of the file as it will be saved in Anki's collection.media folder. Prefix with '_' to prevent Anki from deleting it if not used.")
    skipHash: Optional[str] = Field(None, description="Optional MD5 hash of the file. If provided, Anki-Connect will skip storing the file if the existing file matches this hash.")
    fields: List[str] = Field(default_factory=list, description="A list of field names (e.g., ['Front', 'Back']) in which to insert the media reference (like <img src='...'> or [sound:...]).")
    deleteExisting: bool = Field(True, description="If true (default), any existing file with the same name will be deleted before saving the new one.")

class DuplicateScopeOptions(BaseModel):
    """
    Options for defining the scope when checking for duplicate notes.
    """
    deckName: Optional[str] = Field(None, description="The name of the deck to check for duplicates within.")
    checkChildren: bool = Field(False, description="If true, sub-decks of the specified deck will also be checked.")
    checkAllModels: bool = Field(False, description="If true, duplicates will be checked across all note types, not just the one specified for the new note.")

class NoteOptions(BaseModel):
    """
    Optional configuration for adding a new note.
    """
    allowDuplicate: bool = Field(False, description="Whether to allow the creation of a note even if it's considered a duplicate.")
    duplicateScope: Optional[str] = Field(None, description="The scope of duplicate checking. Use 'deck' to check within a specific deck, or null for global check.")
    duplicateScopeOptions: Optional[DuplicateScopeOptions] = Field(None, description="Detailed options for the duplicate scope.")

class NoteInput(BaseModel):
    """
    The full data required to create a new note in Anki.
    """
    deckName: str = Field(..., description="The name of the target deck (e.g., 'Japanese::Kanji'). If it doesn't exist, it will NOT be created automatically by addNote; use createDeck first if unsure.")
    modelName: str = Field(..., description="The name of the note type to use (e.g., 'Basic', 'Cloze').")
    fields: Dict[str, str] = Field(..., description="A mapping of field names to their HTML contents. Example: {'Front': 'apple', 'Back': 'りんご'}.")
    tags: List[str] = Field(default_factory=list, description="A list of tags to associate with the note.")
    options: Optional[NoteOptions] = Field(None, description="Duplicate checking and creation options.")
    audio: Optional[List[MediaInput]] = Field(None, description="Optional audio files to embed in the fields.")
    video: Optional[List[MediaInput]] = Field(None, description="Optional video files to embed in the fields.")
    picture: Optional[List[MediaInput]] = Field(None, description="Optional picture files to embed in the fields.")

class NoteUpdateInput(BaseModel):
    """
    Data required to update an existing note's fields or tags.
    """
    id: int = Field(..., description="The unique ID of the existing note to update.")
    fields: Optional[Dict[str, str]] = Field(None, description="A mapping of field names to their new HTML contents. Only provided fields will be updated.")
    tags: Optional[List[str]] = Field(None, description="A new list of tags for the note. This REPLACES all existing tags.")
    audio: Optional[List[MediaInput]] = Field(None, description="Optional new audio files to embed.")
    video: Optional[List[MediaInput]] = Field(None, description="Optional new video files to embed.")
    picture: Optional[List[MediaInput]] = Field(None, description="Optional new picture files to embed.")

class FieldInfo(BaseModel):
    """
    Information about a single field within a note or card.
    """
    value: str = Field(..., description="The HTML content of the field.")
    order: int = Field(..., description="The 0-based ordinal position of this field in the note type definition.")

class NoteInfo(BaseModel):
    """
    Detailed information about a note as returned by Anki.
    """
    noteId: int = Field(..., description="The unique ID of the note.")
    profile: str = Field(..., description="The name of the Anki profile this note belongs to.")
    tags: List[str] = Field(..., description="A list of tags currently on the note.")
    fields: Dict[str, FieldInfo] = Field(..., description="A mapping of field names to their values and order.")
    modelName: str = Field(..., description="The name of the note type (model).")
    mod: int = Field(..., description="The timestamp of the last modification to this note.")
    cards: List[int] = Field(..., description="A list of card IDs that were generated from this note.")

class CardInfo(BaseModel):
    """
    Exhaustive information about a card as returned by Anki.
    """
    cardId: int = Field(..., description="The unique ID of the card.")
    fields: Dict[str, FieldInfo] = Field(..., description="A mapping of field names from the parent note.")
    fieldOrder: int = Field(..., description="The index of this card's template within the note type.")
    question: str = Field(..., description="The rendered HTML of the question side.")
    answer: str = Field(..., description="The rendered HTML of the answer side.")
    modelName: str = Field(..., description="The note type name.")
    ord: int = Field(..., description="The ordinal number of the card.")
    deckName: str = Field(..., description="The name of the deck containing this card.")
    css: str = Field(..., description="The CSS styling applied to the card.")
    factor: int = Field(..., description="The ease factor (1000 = 100%).")
    interval: int = Field(..., description="The current review interval. Positive values are days, negative are seconds.")
    note: int = Field(..., description="The ID of the parent note.")
    type: int = Field(..., description="The state of the card: 0=new, 1=learning, 2=review, 3=relearning.")
    queue: int = Field(..., description="The queue position: -1=suspended, 0=new, 1=learning, 2=review, 3=in-situ learning, 4=preview.")
    due: int = Field(..., description="The due date (timestamp or day number depending on card type).")
    reps: int = Field(..., description="The total number of times this card has been reviewed.")
    lapses: int = Field(..., description="The total number of times this card has lapsed.")
    left: int = Field(..., description="The number of steps left in the current learning stage (e.g., 1001 means 1 step left).")
    mod: int = Field(..., description="The timestamp of the last modification.")

class AnkiResponse(BaseModel):
    """
    Standard response format from Anki-Connect.
    """
    result: Any = None
    error: Optional[str] = None
