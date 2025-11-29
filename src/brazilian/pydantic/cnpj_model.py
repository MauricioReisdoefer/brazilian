try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.cnpj import CNPJ
from typing import Annotated

def validate_cnpj(value):
    if isinstance(value, CNPJ):
        return value
    if not isinstance(value, str):
        raise TypeError("CNPJ precisa ser uma string.")
    return CNPJ(value, strict=True)

CNPJType = Annotated[CNPJ, BeforeValidator(validate_cnpj)]

class CNPJModel(BaseModel):
    cnpj: CNPJType

    @field_serializer("cnpj")
    def serialize_cnpj(self, cnpj: CNPJ, _info):
        return cnpj.formatted