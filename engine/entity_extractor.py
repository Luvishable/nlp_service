from enum import Enum
from typing import Optional, Dict


class Month(Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class EntityExtractor:
    def __init__(self) -> None:
        self.month_map: Dict[str, Month] = {
            "january": Month.JANUARY,
            "february": Month.FEBRUARY,
            "march": Month.MARCH,
            "april": Month.APRIL,
            "may": Month.MAY,
            "june": Month.JUNE,
            "july": Month.JULY,
            "august": Month.AUGUST,
            "september": Month.SEPTEMBER,
            "october": Month.OCTOBER,
            "november": Month.NOVEMBER,
            "december": Month.DECEMBER
        }

    def extract_month(self, text: str) -> Optional[int]:
        lowered = text.lower()
        for name, month_enum in self.month_map.items():
            if name in lowered:
                return month_enum.value
        return None
