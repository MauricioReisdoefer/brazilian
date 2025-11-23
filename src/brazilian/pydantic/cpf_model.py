try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.cpf import CPF
from typing import Annotated

def validate_cpf(value):
    cpf = CPF(value, strict=True)  
    return cpf

CPFType = Annotated[CPF, BeforeValidator(validate_cpf)]

class CPFModel(BaseModel):
    cpf: CPFType

    @field_serializer("cpf")
    def serialize_cpf(self, cpf: CPF, _info):
        return cpf.formatted