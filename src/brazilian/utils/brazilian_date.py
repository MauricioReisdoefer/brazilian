import re
from dataclasses import dataclass
from ..errors.invalid_date_error import InvalidDateError


def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))


def _split_date(value: str):
    """Aceita formatos: DD-MM-YYYY, DD/MM/YYYY, YYYY-MM-DD, YYYY/MM/DD."""
    if not value:
        return None

    clean = re.sub(r"[^\d]", " ", value)
    parts = clean.split()

    if len(parts) != 3:
        return None

    a, b, c = parts

    if len(a) == 4:        # YYYY-MM-DD
        year, month, day = a, b, c
    elif len(c) == 4:      # DD-MM-YYYY
        day, month, year = a, b, c
    else:
        return None

    return day, month, year


def _is_leap_year(y: int) -> bool:
    return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)


@dataclass(frozen=True)
class Date:
    _day: str
    _month: str
    _year: str

    def __init__(self, value: str, *, strict: bool = True):
        parts = _split_date(value)
        if not parts:
            raise InvalidDateError(f"Data inválida: {value!r}")

        day, month, year = parts

        object.__setattr__(self, "_day", day)
        object.__setattr__(self, "_month", month)
        object.__setattr__(self, "_year", year)

        if strict:
            self.self_validate(raise_error=True)

    @property
    def day(self) -> str:
        return self._day

    @property
    def month(self) -> str:
        return self._month

    @property
    def year(self) -> str:
        return self._year

    @property
    def formatted(self) -> str:
        """DD-MM-YYYY"""
        return f"{self.day.zfill(2)}-{self.month.zfill(2)}-{self.year.zfill(4)}"

    @property
    def iso(self) -> str:
        """YYYY-MM-DD"""
        return f"{self.year.zfill(4)}-{self.month.zfill(2)}-{self.day.zfill(2)}"

    @property
    def is_valid(self) -> bool:
        return Date.validate(self.formatted)

    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = Date.validate(self.formatted)
        if not valid and raise_error:
            raise InvalidDateError(f"Data inválida: {self.formatted}")
        return valid

    @staticmethod
    def validate(value: str, *, raise_error: bool = False) -> bool:
        parts = _split_date(value)
        if not parts:
            if raise_error:
                raise InvalidDateError(f"Data inválida: {value!r}")
            return False

        day, month, year = parts

        if not (day.isdigit() and month.isdigit() and year.isdigit()):
            if raise_error:
                raise InvalidDateError("Dia, mês e ano devem ser numéricos.")
            return False

        d, m, y = int(day), int(month), int(year)

        if not (1 <= m <= 12):
            if raise_error:
                raise InvalidDateError(f"Mês inválido: {m}")
            return False

        days_month = {
            1: 31,
            2: 29 if _is_leap_year(y) else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        if not (1 <= d <= days_month[m]):
            if raise_error:
                raise InvalidDateError(f"Dia inválido: {d} para o mês {m}")
            return False

        return True

    def self_to_dict(self) -> dict:
        return {
            "day": self.day,
            "month": self.month,
            "year": self.year,
            "formatted": self.formatted,
            "iso": self.iso,
            "is_valid": self.is_valid,
        }

    @staticmethod
    def clean(value: str):
        """Extrai apenas os números da data."""
        return _only_digits(value)

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return f"Date('{self.formatted}')"

    def __eq__(self, other):
        if isinstance(other, Date):
            return self.iso == other.iso
        if isinstance(other, str):
            try:
                return self.iso == Date(other).iso
            except Exception:
                return False
        return False

    def __hash__(self):
        return hash(self.iso)
