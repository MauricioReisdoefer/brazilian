try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..utils.brazilian_date import Date
from typing import Annotated

def validate_brazilian_date(value):
    brazilian_date = Date(value, strict=True)  
    return brazilian_date

DateType = Annotated[Date, BeforeValidator(validate_brazilian_date)]

class DateModel(BaseModel):
    brazilian_date: DateType

    @field_serializer("brazilian_date")
    def serialize_date(self, date: Date, _info):
        return date.formatted