# TODO: Unimplemented Anki-Connect API Actions

This document tracks the remaining Anki-Connect API actions and types that need to be strongly typed and implemented as MCP tools.

Reference: [Anki-Connect SourceHut](https://git.sr.ht/~foosoft/anki-connect)

## Note Types & Models
- [ ] `createModel`: Create a new note type with custom fields and templates.
- [ ] `modelTemplates`: Get templates for a model.
- [ ] `modelStyling`: Get CSS for a model.
- [ ] `updateModelTemplates`: Update templates for an existing model.
- [ ] `updateModelStyling`: Update CSS for an existing model.
- [ ] `modelNamesAndIds`: Get both names and IDs of models.

## Decks
- [ ] `deleteDecks`: Delete multiple decks by name.
- [ ] `getDeckConfig`: Get configuration for a deck.
- [ ] `saveDeckConfig`: Save configuration for a deck.
- [ ] `setDeckConfigId`: Set the config ID for a deck.
- [ ] `getDeckStats`: Get statistics for a deck.

## Cards
- [ ] `suspend`: Suspend cards by ID.
- [ ] `unsuspend`: Unsuspend cards by ID.
- [ ] `areSuspended`: Check if cards are suspended.
- [ ] `areDue`: Check if cards are due.
- [ ] `getIntervals`: Get review intervals for cards.
- [ ] `forgetCards`: Reset cards to "new" state.
- [ ] `relearnCards`: Set cards to "relearn" state.
- [ ] `answerCards`: Answer cards programmatically (useful for automation).

## Media
- [ ] `storeMediaFile`: Upload a file to Anki's media folder.
- [ ] `retrieveMediaFile`: Download a file from Anki's media folder.
- [ ] `getMediaFilesNames`: List files in the media folder.
- [ ] `deleteMediaFile`: Delete a file from the media folder.

## Graphical (GUI)
- [ ] `guiBrowse`: Open the browser with a specific query.
- [ ] `guiAddCards`: Open the "Add Cards" dialog with pre-filled fields.
- [ ] `guiEditNote`: Open the editor for a specific note.
- [ ] `guiCurrentCard`: Get information about the card currently being reviewed.
- [ ] `guiCheckDatabase`: Trigger a database check.

## Miscellaneous
- [ ] `apiReflect`: Discover available API actions.
- [ ] `sync`: Trigger a sync with AnkiWeb.
- [ ] `getProfiles`: List available profiles.
- [ ] `loadProfile`: Switch to a different profile.
- [ ] `exportPackage`: Export a deck as an .apkg file.
- [ ] `importPackage`: Import an .apkg file.

## Tags
- [ ] `getTags`: List all tags.
- [ ] `clearUnusedTags`: Remove tags that aren't used by any notes.
- [ ] `replaceTags`: Replace tags across a set of notes.
- [ ] `replaceTagsInAllNotes`: Global tag replacement.
