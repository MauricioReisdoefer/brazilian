from pydantic import BaseModel, BeforeValidator
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