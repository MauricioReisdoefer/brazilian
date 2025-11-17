import random
import re
from dataclasses import dataclass

from ..errors.invalid_cnpj_error import InvalidCNPJError


def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))


def _is_repeated_digits(digits: str) -> bool:
    return len(set(digits)) == 1


def _calculate_check_digits(base_digits: str) -> str:
    """Calcula os dois dígitos verificadores do CNPJ."""
    nums = [int(d) for d in base_digits]

    weights1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    weights2 = [6] + weights1  

    sum1 = sum(nums[i] * weights1[i] for i in range(12))
    r1 = sum1 % 11
    d1 = 0 if r1 < 2 else 11 - r1

    nums.append(d1)

    sum2 = sum(nums[i] * weights2[i] for i in range(13))
    r2 = sum2 % 11
    d2 = 0 if r2 < 2 else 11 - r2

    return f"{d1}{d2}"


@dataclass(frozen=True)
class CNPJ:
    _value: str

    def __init__(self, value=None, *, strict: bool = True):
        clean = _only_digits(value)
        object.__setattr__(self, "_value", clean)

        if strict:
            self.self_validate(raise_error=True)

    @property
    def value(self) -> str:
        return self._value or ""

    @property
    def digits(self):
        return tuple(int(d) for d in self.value) if self.value else tuple()

    @property
    def is_valid(self) -> bool:
        return CNPJ.validate(self.value)

    @property
    def formatted(self) -> str:
        v = self.value
        if len(v) != 14:
            return v
        return f"{v[0:2]}.{v[2:5]}.{v[5:8]}/{v[8:12]}-{v[12:14]}"

    @property
    def masked(self) -> str:
        v = self.value
        if len(v) != 14:
            return v
        return f"**.***.***/{v[8:12]}-{v[12:14]}"

    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = CNPJ.validate(self.value)
        if not valid and raise_error:
            raise InvalidCNPJError(f"Invalid CNPJ: {self.formatted or self.value!r}")
        return valid
    
    def self_format(self) -> str:
        return self.formatted
    
    def self_mask(self) -> str:
        return self.masked
    
    def self_to_dict(self) -> dict:
        return {
            "value": self.value,
            "formatted": self.formatted,
            "masked": self.masked,
            "is_valid": self.is_valid,
            "region": self.region
        }

    @staticmethod
    def validate(value: str, raise_error: bool = False) -> bool:
        v = _only_digits(value)

        if len(v) != 14 or _is_repeated_digits(v):
            if raise_error:
                raise InvalidCNPJError(f"Invalid CNPJ: {value!r}")
            return False

        base = v[:12]
        expected = _calculate_check_digits(base)

        valid = v[12:14] == expected

        if not valid and raise_error:
            raise InvalidCNPJError(f"Invalid CNPJ: {value!r}")

        return valid

    @staticmethod
    def clean(value: str) -> str:
        return _only_digits(value)

    @staticmethod
    def format(value: str) -> str:
        return CNPJ(value).formatted

    @staticmethod
    def generate(formatted: bool = False) -> "CNPJ":
        base = "".join(str(random.randint(0, 9)) for _ in range(8))
        base += "0001" 
        check = _calculate_check_digits(base)
        cnpj = base + check

        if formatted:
            return CNPJ(cnpj).formatted

        return CNPJ(cnpj)

    @staticmethod
    def random_str(formatted: bool = False) -> str:
        g = CNPJ.generate(formatted=formatted)
        return g if isinstance(g, str) else g.value

    def self_to_dict(self) -> dict:
        return {
            "value": self.value,
            "formatted": self.formatted,
            "masked": self.masked,
            "is_valid": self.is_valid
        }

    def __str__(self):
        return self.formatted or self.value

    def __repr__(self):
        return f"CNPJ('{self.formatted or self.value}')"

    def __eq__(self, other):
        if isinstance(other, CNPJ):
            return self.value == other.value
        return self.value == _only_digits(other)

    def __hash__(self):
        return hash(self.value)

    def __len__(self):
        return len(self.value)