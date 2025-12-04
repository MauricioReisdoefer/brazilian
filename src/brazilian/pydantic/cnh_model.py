try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from typing import Annotated
from ..documents.cnh import CNH

def validate_cnh(value):
    
    if isinstance(value, CNH):
        return value
    if not isinstance(value, str):
        raise TypeError("CNH precisa ser uma string.")
    return CNH(value, strict=True)

CNHType = Annotated[CNH, BeforeValidator(validate_cnh)]

class CNHModel(BaseModel):
    cnh: CNHType

    @field_serializer("cnh")
    def serialize_cnh(self, cnh: CNH, _info):
        return cnh.formatted
