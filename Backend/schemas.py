# Setting type definition the JSON data
from pydantic import BaseModel


class NoteInput(BaseModel):
    title: str = ""
    note_body: str = ""
