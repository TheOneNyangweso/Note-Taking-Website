# main.py - Entry point to our system

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm.exc import UnmappedInstanceError
from fastapi.middleware.cors import CORSMiddleware
from model.database import DBSession
from model import models
from schemas import NoteInput

app = FastAPI()


origins = ["http://localhost:5173"]  # One can add other front-end domains here

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Defining the API Routes to handle the logic of the CRUD operations for the Notes app
# /note - POST - add new note
# /notes - GET - get all notes from db
# /note/{note_id} - PUT - Update a note by its note_id
# /note/{note_id} - DELETE - Delete a note by its note_id


@app.get("/notes")
def read_notes():
    db = DBSession()
    try:
        notes = db.query(models.Note).all()
    finally:
        db.close()
    return notes


@app.post("/note")
def add_note(note: NoteInput):
    db = DBSession()
    try:
        if len(note.title) == 0 and len(note.note_body) == 0:
            raise HTTPException(
                status_code=400,
                detail={
                    "status": "Error 400 - Bad Request",
                    "msg": "Both 'title' and 'note_body' are empty. These are optional attributes but one must be provided",
                },
            )
        new_note = models.Note(title=note.title, note_body=note.note.note_body)

        db.add(new_note)
        db.commit()
        db.refresh(new_note)

    finally:
        db.close()

    return new_note


@app.put("/note/{note_id}")
# Logic here is to fetch the note to be updated from the database through its id
# and update the resulting note data
def update_note(note_id: int, updated_note: NoteInput):
    if len(update_note.title) == 0 and len(updated_note.note_body) == 0:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error 400 - Bad Request",
                "msg": "The note's 'title' and 'note_body' can't both be empty. These are optional attributes but one must be provided",
            },
        )

    db = DBSession()

    try:
        note = db.query(models.Note).filter(models.Note.id == note_id).first()
        note.title = updated_note.title
        note.note_body = updated_note.note_body
        db.commit()
        db.refresh(note)

    finally:
        db.close()

    return note


@app.delete("/note/{note_id}")
def delete_note(note_id: id):
    db = DBSession()
    try:
        note = db.query(models.Note).filter(models.Note.id == note_id).first()
        db.delete(note)
        db.commit()
    except UnmappedInstanceError:
        raise HTTPException(
            status_code=400,
            detail={
                "status": "Error 400 - Bad Request",
                "msg": f"Note with 'id' : '{note_id}' does not exist",
            },
        )

    finally:
        db.close()

    return {"status": "200", "msg": "Note deleted successfully"}
