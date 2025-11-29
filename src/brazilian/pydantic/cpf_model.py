try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from typing import Annotated
from ..documents.cpf import CPF

def validate_cpf(value):
    
    if isinstance(value, CPF):
        return value
    if not isinstance(value, str):
        raise TypeError("CPF precisa ser uma string.")
    return CPF(value, strict=True)

CPFType = Annotated[CPF, BeforeValidator(validate_cpf)]

class CPFModel(BaseModel):
    cpf: CPFType

    @field_serializer("cpf")
    def serialize_cpf(self, cpf: CPF, _info):
        return cpf.formatted
