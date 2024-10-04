from ninja import Schema
from typing import Optional, List

# from core.models import Group


class GroupIn(Schema):
    name: str
    tags: Optional[List[int]] = None

class GroupOut(Schema):
    id: int
    name: str
    tags: Optional[List[int]] = None

class GroupUpdate(Schema):
    name: Optional[str] = None
    tags: Optional[List[int]] = None
