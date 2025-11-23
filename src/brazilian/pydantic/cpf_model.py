try:
    from pydantic import BaseModel, BeforeValidator
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

    model_config = {
        "json_encoders": {
            CPF: lambda c: c.formatted
        }
    }