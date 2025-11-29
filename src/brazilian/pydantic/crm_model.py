try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..documents.crm import CRM
from typing import Annotated

def validate_crm(value):
    if isinstance(value, CRM):
        return value
    if not isinstance(value, str):
        raise TypeError("CRM precisa ser uma string.")
    return CRM(value, strict=True)

CRMType = Annotated[CRM, BeforeValidator(validate_crm)]

class CRMModel(BaseModel):
    crm: CRMType

    @field_serializer("crm")
    def serialize_crm(self, crm: CRM, _info):
        return crm.formatted