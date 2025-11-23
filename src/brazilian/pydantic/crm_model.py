try:
    from pydantic import BaseModel, BeforeValidator
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.crm import CRM
from typing import Annotated

def validate_crm(value):
    crm = CRM(value, strict=True)  
    return crm

CRMType = Annotated[CRM, BeforeValidator(validate_crm)]

class CRMModel(BaseModel):
    crm: CRMType

    model_config = {
        "json_encoders": {
            CRM: lambda c: c.formatted
        }
    }