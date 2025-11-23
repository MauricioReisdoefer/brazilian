from pydantic import BaseModel, BeforeValidator
from ..utils.brazilian_date import Date
from typing import Annotated

def validate_brazilian_date(value):
    brazilian_date = Date(value, strict=True)  
    return brazilian_date

DateType = Annotated[Date, BeforeValidator(validate_brazilian_date)]

class DateModel(BaseModel):
    brazilian_date: DateType

    model_config = {
        "json_encoders": {
            brazilian_date: lambda c: c.formatted
        }
    }