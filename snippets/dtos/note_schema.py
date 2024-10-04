from ninja import Schema
from typing import Optional, List
from django.utils import timezone
from datetime import datetime
from pydantic import field_validator

# from core.models import Note

class NoteIn(Schema):
    title: str
    content: str
    group: Optional[int] = None
    tags: Optional[List[int]] = None
    expiration_date: Optional[datetime] = None

class NoteOut(Schema):
    id: int
    title: str
    content: str
    user_id: int
    group: Optional[int] = None
    tags: Optional[List[int]] = None
    created_at: timezone.datetime
    updated_at: timezone.datetime
    expiration_date: Optional[datetime] = None

class NoteUpdate(Schema):
    title: Optional[str] = None
    content: Optional[str] = None
    group: Optional[int] = None
    tags: Optional[List[int]] = None
    expiration_date: Optional[datetime] = None

    @field_validator('expiration_date', mode='before')
    def validate_expiration_date(cls, value: Optional[str]) -> Optional[datetime]:
        print(f"Validating expiration_date: {value}")
        if value:
            try:
                date = datetime.fromisoformat(value)

                if date.tzinfo is None:
                    # date = timezone.make_aware(date, timezone.get_current_timezone())
                    date = timezone.make_aware(date)

                if date <= timezone.now():
                    raise ValueError('Expiration date cannot be in the past')

                return date
            except ValueError as e:
                raise ValueError(f'Invalid date format or value: {str(e)}. Please use ISO format (YYYY-MM-DDTHH:MM:SS).')
        return None

    @field_validator('tags')
    def validate_tags(cls, value):
        if value and not all(isinstance(tag, int) and tag > 0 for tag in value):
            raise ValueError('All tag IDs must be positive integers')
        return value