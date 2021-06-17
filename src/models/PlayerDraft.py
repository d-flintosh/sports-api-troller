from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True, eq=True)
class PlayerDraft:
    id: Union[str, int]
    full_name: str
    college: str
    draft_year: int = None
    college_id: int = None
