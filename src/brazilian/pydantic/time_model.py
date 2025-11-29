try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..utils.brazilian_time import Time
from typing import Annotated

def validate_brazilian_time(value):
    if isinstance(value, Time):
        return value
    if not isinstance(value, str):
        raise TypeError("Time precisa ser uma string.")
    return Time(value, strict=True)

TimeType = Annotated[Time, BeforeValidator(validate_brazilian_time)]

class TimeModel(BaseModel):
    time: TimeType

    @field_serializer("time")
    def serialize_time(self, time: Time, _info):
        return time.formatted