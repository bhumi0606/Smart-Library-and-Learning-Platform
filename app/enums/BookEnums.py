
# ENUMS
from enum import Enum

class BookStatus(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"
    LOST = "lost"
    DAMAGED = "damaged"


class BookType(str, Enum):
    PHYSICAL = "physical"
    DIGITAL = "digital"