try:
    from pydantic import BaseModel, BeforeValidator
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.cnpj import CNPJ
from typing import Annotated

def validate_cnpj(value):
    cnpj = CNPJ(value, strict=True)  
    return cnpj

CNPJType = Annotated[CNPJ, BeforeValidator(validate_cnpj)]

class CNPJModel(BaseModel):
    cnpj: CNPJType

    model_config = {
        "json_encoders": {
            CNPJ: lambda c: c.formatted
        }
    }