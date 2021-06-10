from dataclasses import dataclass


@dataclass(frozen=True, eq=True)
class PlayerDraft:
    id: int
    full_name: str
    college: str
    draft_year: int = None
    college_id: int = None
