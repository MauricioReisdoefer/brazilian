try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..utils.brazilian_date import Date
from typing import Annotated

def validate_brazilian_date(value):
    if isinstance(value, Date):
        return value
    if not isinstance(value, str):
        raise TypeError("Date precisa ser uma string.")
    return Date(value, strict=True)

DateType = Annotated[Date, BeforeValidator(validate_brazilian_date)]

class DateModel(BaseModel):
    date: DateType

    @field_serializer("date")
    def serialize_date(self, date: Date, _info):
        return date.formatted