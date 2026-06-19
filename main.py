import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


# -----------------------------
# Note Model
# -----------------------------
class Note(BaseModel):
    title: str
    content: str


# -----------------------------
# Home Route
# -----------------------------
@app.get("/")
def home():
    return {
        "message": "Second Brain Backend Running"
    }


# -----------------------------
# Add Note
# -----------------------------
@app.post("/add-note")
def add_note(note: Note):

    with open("notes.json", "r") as f:
        notes = json.load(f)

    updated = False

    for existing_note in notes:
        if existing_note["title"].lower() == note.title.lower():
            existing_note["content"] = note.content
            updated = True
            break

    if not updated:
        notes.append({
            "title": note.title,
            "content": note.content
        })

    with open("notes.json", "w") as f:
        json.dump(notes, f, indent=4)

    return {
        "message": "Note saved successfully"
    }

# -----------------------------
# View Notes
# -----------------------------
@app.get("/notes")
def get_notes():

    with open("notes.json", "r") as f:
        notes = json.load(f)

    return notes
@app.get("/search")
def search_notes(keyword: str):

    with open("notes.json", "r") as f:
        notes = json.load(f)

    results = []

    for note in notes:

        if (
            keyword.lower() in note["title"].lower()
            or keyword.lower() in note["content"].lower()
        ):
            results.append(note)

    return results    
@app.delete("/delete-note/{title}")
def delete_note(title: str):

    with open("notes.json", "r") as f:
        notes = json.load(f)

    updated_notes = []

    for note in notes:
        if note["title"] != title:
            updated_notes.append(note)

    with open("notes.json", "w") as f:
        json.dump(updated_notes, f, indent=4)

    return {"message": "Note deleted successfully"}    