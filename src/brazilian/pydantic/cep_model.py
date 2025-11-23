from pydantic import BaseModel, BeforeValidator
from ..documents.cep import CEP
from typing import Annotated

def validate_cep(value):
    cep = CEP(value, strict=True)  
    return cep

CEPType = Annotated[CEP, BeforeValidator(validate_cep)]

class CEPModel(BaseModel):
    cep: CEPType

    model_config = {
        "json_encoders": {
            CEP: lambda c: c.formatted
        }
    }