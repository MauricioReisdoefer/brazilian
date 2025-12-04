import random
import re
from dataclasses import dataclass
from ..errors.invalid_cnh_error import InvalidCNHError


def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))


def _is_repeated_digits(digits: str) -> bool:
    return len(set(digits)) == 1


def _calculate_cnh_check_digits(base: str) -> str:
    nums = [int(d) for d in base]

    # 1º dígito
    s1 = sum(nums[i] * (9 - i) for i in range(9))
    d1 = s1 % 11
    if d1 >= 10:
        d1 = 0

    # 2º dígito
    s2 = sum(nums[i] * (i + 1) for i in range(9))
    d2 = s2 % 11
    if d2 >= 10:
        d2 = 0

    return f"{d1}{d2}"


@dataclass(frozen=True)
class CNH:
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
        return CNH.validate(self.value)

    @property
    def formatted(self) -> str:
        """Formato padrão CNH: 00000000000 → 000000000-00 (não existe máscara 100% oficial)."""
        v = self.value
        if len(v) != 11:
            return v
        return f"{v[0:9]}-{v[9:11]}"

    @property
    def masked(self) -> str:
        v = self.value
        if len(v) != 11:
            return v
        return f"*********-{v[9:11]}"

    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = CNH.validate(self.value)
        if not valid and raise_error:
            raise InvalidCNHError(f"Invalid CNH: {self.formatted or self.value!r}")
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
        }

    @staticmethod
    def clean(value: str) -> str:
        return _only_digits(value)

    @staticmethod
    def validate(value: str, raise_error: bool = False) -> bool:
        v = _only_digits(value)

        if len(v) != 11 or _is_repeated_digits(v):
            if raise_error:
                raise InvalidCNHError(f"Invalid CNH: {value!r}")
            return False

        base = v[:9]
        expected = _calculate_cnh_check_digits(base)

        valid = v[9:11] == expected

        if not valid and raise_error:
            raise InvalidCNHError(f"Invalid CNH: {value!r}")

        return valid

    @staticmethod
    def generate(formatted: bool = False):
        base = "".join(str(random.randint(0, 9)) for _ in range(9))
        check = _calculate_cnh_check_digits(base)
        cnh = base + check

        if formatted:
            return CNH(cnh, strict=True).formatted
        return CNH(cnh, strict=True)

    @staticmethod
    def random_str(formatted: bool = False) -> str:
        gen = CNH.generate(formatted=formatted)
        return gen if isinstance(gen, str) else gen.value

    @staticmethod
    def format(value: str):
        return CNH(value).formatted

    def __str__(self):
        return self.formatted or self.value

    def __repr__(self):
        return f"CNH('{self.formatted or self.value}')"

    def __eq__(self, other):
        if isinstance(other, CNH):
            return self.value == other.value
        return self.value == _only_digits(other)

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(self.value)
