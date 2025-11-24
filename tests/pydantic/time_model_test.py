import pytest
from pydantic import ValidationError
from brazilian.pydantic.time_model import TimeModel
from brazilian.utils.brazilian_time import Time

def test_valid_time():
    model = TimeModel(time="18:55")
    assert isinstance(model.time, Time)
    assert model.time.formatted is not None

def test_invalid_time():
    with pytest.raises(ValidationError):
        TimeModel(time="20225/120/12")

def test_json_encoder():
    model = TimeModel(time="23:10")
    json_output = model.model_dump_json()
    assert model.time.formatted in json_output 
