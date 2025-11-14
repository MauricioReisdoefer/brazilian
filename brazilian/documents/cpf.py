import random
import re
from dataclasses import dataclass
from ..errors.invalid_cpf_error import InvalidCPFError

def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))

def _is_repeated_digits(digits: str) -> bool:
    return len(set(digits)) == 1

def _calculate_check_digits(base_digits: str) -> str:
    nums = [int(d) for d in base_digits]
    s1 = sum((10 - i) * nums[i] for i in range(9))
    r1 = (s1 * 10) % 11
    d1 = r1 if r1 < 10 else 0
    nums.append(d1)
    s2 = sum((11 - i) * nums[i] for i in range(10))
    r2 = (s2 * 10) % 11
    d2 = r2 if r2 < 10 else 0
    return f"{d1}{d2}"

@dataclass(frozen=True)
class CPF:
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
        return CPF.validate(self.value)
 
    @property
    def region(self) -> str:
        """Retorna a região literal (ex: 'Sao Paulo', 'Minas Gerais', etc.)."""
        if len(self.value) < 9 or not self.value.isdigit():
            return None

        regions = {
            0: "Rio Grande do Sul",
            1: "Distrito Federal, Goias, Mato Grosso, Mato Grosso do Sul, Tocantins",
            2: "Para, Amazonas, Acre, Amapa, Rondonia, Roraima",
            3: "Ceara, Maranhao, Piaui",
            4: "Pernambuco, Rio Grande do Norte, Paraiba, Alagoas",
            5: "Bahia, Sergipe",
            6: "Minas Gerais",
            7: "Rio de Janeiro, Espirito Santo",
            8: "Sao Paulo",
            9: "Parana, Santa Catarina"
        }

        return regions.get(int(self.value[8]))
    
    @property
    def region_acronym(self) -> str:
        """Retorna a região em sigla (ex: 'SP', 'MG', etc.)."""
        if len(self.value) < 9 or not self.value.isdigit():
            return None

        regions = {
            0: "RS",
            1: "DF, GO, MT, MS, TO",
            2: "PA, AM, AC, AP, RO, RR",
            3: "CE, MA, PI",
            4: "PE, RN, PB, AL",
            5: "BA, SE",
            6: "MG",
            7: "RJ, ES",
            8: "SP",
            9: "PR, SC"
        }

        return regions.get(int(self.value[8]))
    
    @property
    def formatted(self) -> str:
        v = self.value
        if len(v) != 11:
            return v
        return f"{v[0:3]}.{v[3:6]}.{v[6:9]}-{v[9:11]}"
    
    @property
    def masked(self) -> str:
        v = self.value
        if len(v) != 11:
            return v
        return f"***.***.***-{v[9:11]}"
    
    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = CPF.validate(self.value)
        if not valid and raise_error:
            raise InvalidCPFError(f"Invalid CPF: {self.formatted or self.value!r}")
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
    def clean(value: str) -> str:
        return _only_digits(value)
    
    @staticmethod
    def validate(value: str, raise_error: bool = False) -> bool:
        v = _only_digits(value)

        if len(v) != 11 or _is_repeated_digits(v):
            if raise_error:
                raise InvalidCPFError(f"Invalid CPF: {value!r}")
            return False

        base = v[:9]
        expected = _calculate_check_digits(base)

        valid = v[9:11] == expected

        if not valid and raise_error:
            raise InvalidCPFError(f"Invalid CPF: {value!r}")
        
        return valid

    
    @staticmethod
    def generate(formatted: bool = False) -> "CPF":
        base = "".join(str(random.randint(0,9)) for _ in range(9))
        check = _calculate_check_digits(base)
        cpf = base + check
        if formatted:
            return CPF(cpf, strict=True).formatted
        return CPF(cpf, strict=True)
    
    @staticmethod
    def random_str(formatted: bool = False) -> str:
        gen = CPF.generate(formatted=formatted)
        return gen if isinstance(gen, str) else gen.value
    
    @staticmethod
    def format(value: str):
        self_cpf = CPF(value)
        return self_cpf.formatted
        
    def __str__(self):
        return self.formatted or self.value
    
    def __repr__(self):
        return f"CPF('{self.formatted or self.value}')"
    
    def __eq__(self, other):
        if isinstance(other, CPF):
            return self.value == other.value
        return self.value == _only_digits(other)
    
    def __len__(self):
        return len(self.value)
    
    def __hash__(self):
        return hash(self.value)