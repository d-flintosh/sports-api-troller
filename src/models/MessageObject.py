from dataclasses import dataclass
from typing import List


@dataclass
class MessageObject:
    raw_data: List
    message: str