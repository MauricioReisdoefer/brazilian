import re
import random
from dataclasses import dataclass
import requests
from ..errors.invalid_cep_error import InvalidCEPError

def _only_digits(value: str) -> str:
    return re.sub(r'\D', '', str(value or ''))


@dataclass(frozen=True)
class CEP:
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
    def digits(self) -> tuple:
        return tuple(int(d) for d in self.value) if self.value else tuple()

    @property
    def is_valid(self) -> bool:
        return CEP.validate(self.value)

    @property
    def region(self) -> str:
        """UF correspondente ao prefixo do CEP."""
        uf = CEP.uf_from_cep(self.value)
        return uf

    @property
    def region_acronym(self) -> str:
        """Alias para o mesmo resultado da propriedade region."""
        return self.region

    @property
    def formatted(self) -> str:
        v = self.value
        if len(v) != 8:
            return v
        return f"{v[:5]}-{v[5:]}"

    @property
    def masked(self) -> str:
        v = self.value
        if len(v) != 8:
            return v
        return f"*****-{v[5:]}"

    def self_validate(self, *, raise_error: bool = False) -> bool:
        valid = CEP.validate(self.value)
        if not valid and raise_error:
            raise InvalidCEPError(f"Invalid CEP: {self.formatted or self.value!r}")
        return valid

    @staticmethod
    def validate(value: str, raise_error: bool = False) -> bool:
        v = _only_digits(value)

        if len(v) != 8:
            if raise_error:
                raise InvalidCEPError(f"Invalid CEP: {value!r}")
            return False
        
        if CEP.uf_from_cep(v) is None:
            if raise_error:
                raise InvalidCEPError(f"Invalid CEP (prefixo desconhecido): {value!r}")
            return False

        return True

    PREFIX_MAP = {
        range(1000, 20000): "SP",
        range(20000, 29000): "RJ",
        range(29000, 30000): "ES",
        range(30000, 40000): "MG",
        range(40000, 49000): "BA",
        range(49000, 50000): "SE",
        range(50000, 58000): "PE",
        range(58000, 59000): "PB",
        range(59000, 60000): "RN",
        range(60000, 63000): "CE",
        range(63000, 65000): "PI",
        range(65000, 66000): "MA",
        range(66000, 69000): "PA",
        range(69000, 70000): "AM",
        range(70000, 73000): "DF",
        range(73000, 74000): "GO",
        range(74000, 78000): "MT",
        range(78000, 80000): "MS",

        range(80000, 88000): "PR",
        range(88000, 90000): "SC",
        range(90000, 100000): "RS",
    }

    @staticmethod
    def uf_from_cep(cep: str):
        cep = _only_digits(cep)
        if len(cep) < 5:
            return None

        try:
            prefix = int(cep[:5])
        except:
            return None

        for faixa, uf in CEP.PREFIX_MAP.items():
            if prefix in faixa:
                return uf

        return None

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
        
    def self_get_location(self):
        cep = self.formatted.strip("-")
        url = f"https://viacep.com.br/ws/{cep}/json/"

        resposta = requests.get(url)

        if resposta.status_code != 200:
            raise Exception("Erro ao acessar o ViaCEP")

        dados = resposta.json()
        return dados

    @staticmethod
    def clean(value: str) -> str:
        """Retorna apenas os dígitos"""
        return _only_digits(value)

    @staticmethod
    def generate(formatted: bool = False):
        faixa = random.choice(list(CEP.PREFIX_MAP.keys()))
        prefix = random.choice(list(faixa))
        sufixo = random.randint(0, 999)
        cep = f"{prefix:05d}{sufixo:03d}"

        if formatted:
            return CEP(cep).formatted
        return CEP(cep)

    @staticmethod
    def random_str(formatted: bool = False) -> str:
        gen = CEP.generate(formatted=formatted)
        return gen if isinstance(gen, str) else gen.value

    @staticmethod
    def format(value: str):
        return CEP(value).formatted
    
    @staticmethod
    def get_location(cep: "CEP"):
        cep = cep.formatted.strip("-")
        url = f"https://viacep.com.br/ws/{cep}/json/"

        resposta = requests.get(url)

        if resposta.status_code != 200:
            raise Exception("Erro ao acessar o ViaCEP")

        dados = resposta.json()
        return dados
    
    def __str__(self):
        return self.formatted or self.value

    def __repr__(self):
        return f"CEP('{self.formatted or self.value}')"

    def __eq__(self, other):
        if isinstance(other, CEP):
            return self.value == other.value
        return self.value == _only_digits(other)

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(self.value)