from pydantic import BaseModel


class RelatedSentence(BaseModel):
    english: str
    chinese: str


class BuddyResponse(BaseModel):
    child_friendly_translation: list[str]
    explanation: str
    related_sentences: list[RelatedSentence]
    pronunciation_hints: str
