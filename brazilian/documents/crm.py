import random
import re
from dataclasses import dataclass
from ..errors.invalid_crm_error import InvalidCRMError

UF_LIST = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS",
    "MG","PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC",
    "SP","SE","TO"
]

UF_TO_REGION = {
    "AC": "Norte",
    "AL": "Nordeste",
    "AP": "Norte",
    "AM": "Norte",
    "BA": "Nordeste",
    "CE": "Nordeste",
    "DF": "Centro-Oeste",
    "ES": "Sudeste",
    "GO": "Centro-Oeste",
    "MA": "Nordeste",
    "MT": "Centro-Oeste",
    "MS": "Centro-Oeste",
    "MG": "Sudeste",
    "PA": "Norte",
    "PB": "Nordeste",
    "PR": "Sul",
    "PE": "Nordeste",
    "PI": "Nordeste",
    "RJ": "Sudeste",
    "RN": "Nordeste",
    "RS": "Sul",
    "RO": "Norte",
    "RR": "Norte",
    "SC": "Sul",
    "SP": "Sudeste",
    "SE": "Nordeste",
    "TO": "Norte"
}

UF_ACRONYM_TO_UF = {
    "AC": "Acre",
    "AL": "Alagoas",
    "AP": "Amapa",
    "AM": "Amazonas",
    "BA": "Bahia",
    "CE": "Ceara",
    "DF": "Distrito Federal",
    "ES": "Espirito Santo",
    "GO": "Goias",
    "MA": "Maranhao",
    "MT": "Mato Grosso",
    "MS": "Mato Grosso do Sul",
    "MG": "Minas Gerais",
    "PA": "Para",
    "PB": "Paraiba",
    "PR": "Parana",
    "PE": "Pernambuco",
    "PI": "Piaui",
    "RJ": "Rio de Janeiro",
    "RN": "Rio Grande do Norte",
    "RS": "Rio Grande do Sul",
    "RO": "Rondonia",
    "RR": "Roraima",
    "SC": "Santa Catarina",
    "SP": "Sao Paulo",
    "SE": "Sergipe",
    "TO": "Tocantins"
}


def _clean_crm(value: str) -> str:
    if not value:
        return ""
    return re.sub(r"[^0-9A-Za-z]", "", value).upper()


@dataclass(frozen=True)
class CRM:
    _value: str

    def __init__(self, value=None, *, strict: bool = True):
        clean = _clean_crm(value)
        object.__setattr__(self, "_value", clean)
        if strict:
            self.self_validate(raise_error=True)

    @property
    def value(self) -> str:
        return self._value or ""

    @property
    def number(self) -> str:
        """Parte numérica do CRM."""
        digits = re.sub(r"\D", "", self.value)
        return digits

    @property
    def uf_acronym(self) -> str:
        """Sigla do UF associada ao CRM."""
        letters = re.sub(r"[^A-Z]", "", self.value)
        return letters if letters in UF_LIST else None
    
    @property
    def uf(self) -> str:
        """UF associada ao CRM."""
        return UF_ACRONYM_TO_UF[self.uf_acronym]

    @property
    def region(self) -> str:
        """Retorna 'Sudeste', 'Sul', etc."""
        if not self.uf:
            return None
        return UF_TO_REGION.get(self.uf)

    @property
    def formatted(self) -> str:
        """Formata como 123456-SP."""
        if not self.number or not self.uf:
            return self.value
        return f"{self.number}-{self.uf}"

    @property
    def masked(self) -> str:
        """Exibe como ***456-SP."""
        if not self.number or not self.uf:
            return self.value
        if len(self.number) < 3:
            return f"***-{self.uf}"
        return f"{'*' * (len(self.number) - 3)}{self.number[-3:]}-{self.uf}"

    @property
    def is_valid(self) -> bool:
        return CRM.validate(self.value)

    @staticmethod
    def validate(value: str, raise_error: bool = False) -> bool:
        v = _clean_crm(value)

        number = re.sub(r"\D", "", v)
        letters = re.sub(r"[^A-Z]", "", v)

        if not number or not letters:
            if raise_error:
                raise InvalidCRMError(f"Invalid CRM: {value!r}")
            return False

        if letters not in UF_LIST:
            if raise_error:
                raise InvalidCRMError(f"Invalid CRM UF: {value!r}")
            return False

        if not (4 <= len(number) <= 6):
            if raise_error:
                raise InvalidCRMError(f"Invalid CRM number: {value!r}")
            return False

        return True

    def self_validate(self, *, raise_error: bool = False) -> bool:
        ok = CRM.validate(self.value)
        if not ok and raise_error:
            raise InvalidCRMError(f"Invalid CRM: {self.formatted or self.value!r}")
        return ok

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
            "uf": self.uf,
            "region": self.region,
        }
        
    @staticmethod
    def clean(value: str) -> str:
        return _clean_crm(value)

    @staticmethod
    def generate(uf: str = None, formatted: bool = False):
        if uf is None:
            uf = random.choice(UF_LIST)
        if uf not in UF_LIST:
            raise InvalidCRMError(f"Invalid UF for CRM: {uf!r}")

        number = str(random.randint(1000, 999999))
        crm = number + uf

        if formatted:
            return CRM(crm).formatted

        return CRM(crm, strict=True)

    @staticmethod
    def random_str(formatted: bool = False):
        gen = CRM.generate(formatted=formatted)
        return gen if isinstance(gen, str) else gen.value

    @staticmethod
    def format(value: str):
        return CRM(value).formatted

    def __str__(self):
        return self.formatted or self.value

    def __repr__(self):
        return f"CRM('{self.formatted or self.value}')"

    def __eq__(self, other):
        if isinstance(other, CRM):
            return self.value == other.value
        return self.value == _clean_crm(other)

    def __len__(self):
        return len(self.value)

    def __hash__(self):
        return hash(self.value)
