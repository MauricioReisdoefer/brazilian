try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.cep import CEP
from typing import Annotated

def validate_cep(value):
    if isinstance(value, CEP):
        return value
    if not isinstance(value, str):
        raise TypeError("CEP precisa ser uma string.")
    return CEP(value, strict=True)

CEPType = Annotated[CEP, BeforeValidator(validate_cep)]

class CEPModel(BaseModel):
    cep: CEPType

    @field_serializer("cep")
    def serialize_cep(self, cep: CEP, _info):
        return cep.formatted