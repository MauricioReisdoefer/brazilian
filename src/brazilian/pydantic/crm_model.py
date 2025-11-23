from pydantic import BaseModel, BeforeValidator
from ..documents.crm import CRM
from typing import Annotated

def validate_crm(value):
    crm = CRM(value, strict=True)  
    return crm

CRMType = Annotated[CRM, BeforeValidator(validate_crm)]

class CRMModel(BaseModel):
    crm: CRMType
