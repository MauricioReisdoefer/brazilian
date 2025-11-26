import pytest
from brazilian.sqlalchemy.time_type import SQLAlchemyTimeType
from brazilian.utils.brazilian_time import Time

try:
    from brazilian.pydantic.time_model import TimeModel
    PYDANTIC = True
except ImportError:
    TimeModel = None
    PYDANTIC = False

VALID_DATE_MASKED = "12:12"
VALID_DATE_ISO = "12:12"

def test_process_bind_param_string():
    t = SQLAlchemyTimeType()
    assert t.process_bind_param(VALID_DATE_MASKED, None) == VALID_DATE_ISO

def test_process_bind_param_time_object():
    t = SQLAlchemyTimeType()
    time = Time(VALID_DATE_MASKED)
    assert t.process_bind_param(time, None) == VALID_DATE_ISO

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyTimeType()
    model = TimeModel(time=VALID_DATE_ISO)
    assert t.process_bind_param(model, None) == VALID_DATE_ISO

def test_process_result_value_without_pydantic():
    t = SQLAlchemyTimeType()
    result = t.process_result_value(VALID_DATE_ISO, None)

    if PYDANTIC:
        assert isinstance(result, TimeModel)
        assert result.time.formatted == VALID_DATE_ISO
    else:
        assert isinstance(result, Time)
        assert result.formatted == VALID_DATE_ISO

def test_process_literal_param():
    t = SQLAlchemyTimeType()
    assert t.process_literal_param(VALID_DATE_MASKED, None) == VALID_DATE_ISO

def test_process_bind_param_none():
    t = SQLAlchemyTimeType()
    assert t.process_bind_param(None, None) == None