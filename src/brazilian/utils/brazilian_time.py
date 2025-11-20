import re
from dataclasses import dataclass
from ..errors.invalid_time_error import InvalidTimeError


def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))


def _split_time(value: str):
    """
    Aceita formatos:
    - HH:MM
    - HH-MM
    - números juntos: HHMM
    """
    if not value:
        return None

    clean = _only_digits(value)

    if len(clean) == 4:
        hour = clean[:2]
        minute = clean[2:]
        return hour, minute

    parts = re.split(r'[:\-]', value)
    parts = [p for p in parts if p.strip()]

    if len(parts) == 2:
        h, m = parts
        return h, m

    return None

@dataclass(frozen=True)
class Time:
    _hour: str
    _minute: str

    def __init__(self, value: str, *, strict: bool = True):
        parts = _split_time(value)
        if not parts:
            raise InvalidTimeError(f"Hora inválida: {value!r}")

        hour, minute = parts

        object.__setattr__(self, "_hour", hour)
        object.__setattr__(self, "_minute", minute)

        if strict:
            self.self_validate(raise_error=True)
            
    @property
    def hour(self) -> str:
        return self._hour

    @property
    def minute(self) -> str:
        return self._minute

    @property
    def total_minutes(self) -> int:
        return int(self._minute) + int(self._hour)
    
    @property
    def formatted(self) -> str:
        """HH:MM"""
        return f"{self.hour.zfill(2)}:{self.minute.zfill(2)}"

    @property
    def iso(self) -> str:
        """ISO-like: HH:MM"""
        return self.formatted

    @property
    def is_valid(self) -> bool:
        return Time.validate(self.formatted)

    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = Time.validate(self.formatted)
        if not valid and raise_error:
            raise InvalidTimeError(f"Hora inválida: {self.formatted}")
        return valid

    @staticmethod
    def validate(value: str, *, raise_error: bool = False) -> bool:
        parts = _split_time(value)
        if not parts:
            if raise_error:
                raise InvalidTimeError(f"Hora inválida: {value!r}")
            return False

        hour, minute = parts

        if not (hour.isdigit() and minute.isdigit()):
            if raise_error:
                raise InvalidTimeError("Hora e minutos devem ser numéricos.")
            return False

        h, m = int(hour), int(minute)

        if not (0 <= h <= 23):
            if raise_error:
                raise InvalidTimeError(f"Hora inválida: {h}")
            return False

        if not (0 <= m <= 59):
            if raise_error:
                raise InvalidTimeError(f"Minutos inválidos: {m}")
            return False

        return True

    def self_to_dict(self) -> dict:
        return {
            "hour": self.hour,
            "minute": self.minute,
            "formatted": self.formatted,
            "iso": self.iso,
            "is_valid": self.is_valid,
        }

    @staticmethod
    def clean(value: str):
        """Extrai apenas os números do horário."""
        return _only_digits(value)

    def __str__(self):
        return self.formatted

    def __repr__(self):
        return f"Time('{self.formatted}')"

    def __eq__(self, other):
        if isinstance(other, Time):
            return self.iso == other.iso
        if isinstance(other, str):
            try:
                return self.iso == Time(other).iso
            except Exception:
                return False
        return False

    def __hash__(self):
        return hash(self.iso)
