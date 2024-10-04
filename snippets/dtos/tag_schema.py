from ninja import Schema
from typing import Optional, List

# from core.models import Tag


class TagIn(Schema):
    name: str

class TagOut(Schema):
    id: int
    name: str

class TagUpdate(Schema):
    name: Optional[str] = None
