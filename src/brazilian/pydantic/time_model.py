from pydantic import BaseModel, BeforeValidator
from ..utils.brazilian_time import Time
from typing import Annotated

def validate_brazilian_time(value):
    brazilian_time = Time(value, strict=True)  
    return brazilian_time

TimeType = Annotated[Time, BeforeValidator(validate_brazilian_time)]

class TimeModel(BaseModel):
    brazilian_time: TimeType
