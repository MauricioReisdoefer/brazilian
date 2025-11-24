try:
    from pydantic import BaseModel, BeforeValidator, field_serializer
except ImportError as e:
    raise ImportError(
        "Para usar o módulo pydantic do brazilian, instale o extra `brazilian[pydantic]`."
    ) from e
    
from ..utils.brazilian_time import Time
from typing import Annotated

def validate_brazilian_time(value):
    brazilian_time = Time(value, strict=True)  
    return brazilian_time

TimeType = Annotated[Time, BeforeValidator(validate_brazilian_time)]

class TimeModel(BaseModel):
    brazilian_time: TimeType

    @field_serializer("brazilian_time")
    def serialize_time(self, time: Time, _info):
        return time.formatted