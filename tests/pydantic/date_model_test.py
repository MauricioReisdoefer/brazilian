import pytest
from pydantic import ValidationError
from brazilian.pydantic.date_model import DateModel
from brazilian.utils.brazilian_date import Date

def test_valid_date():
    model = DateModel(date="24/11/2025")
    assert isinstance(model.date, Date)
    assert model.date.formatted is not None

def test_invalid_date():
    with pytest.raises(ValidationError):
        DateModel(date="20225/120/12")

def test_json_encoder():
    model = DateModel(date="24/11/2025")
    json_output = model.model_dump_json()
    assert model.date.formatted in json_output 
