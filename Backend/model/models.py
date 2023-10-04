from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Note(Base):
    __tablename__ = (
        "notes"  # Double underscores since we want it to be a private variable
    )

    id = Column(Integer, primary_key=True)
    title = Column(String)
    note_body = Column(String)

    def __repr__(self):
        return f"Note(id = {self.id}, title = {self.title}, note_body = {self.body})"
