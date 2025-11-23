from pydantic import BaseModel, BeforeValidator
from ..documents.cnpj import CNPJ
from typing import Annotated

def validate_cnpj(value):
    cnpj = CNPJ(value, strict=True)  
    return cnpj

CNPJType = Annotated[CNPJ, BeforeValidator(validate_cnpj)]

class CNPJModel(BaseModel):
    cnpj: CNPJType
