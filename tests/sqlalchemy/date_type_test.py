import pytest
from brazilian.sqlalchemy.date_type import SQLAlchemyDateType
from brazilian.utils.brazilian_date import Date

try:
    from brazilian.pydantic.date_model import DateModel
    PYDANTIC = True
except ImportError:
    DateModel = None
    PYDANTIC = False

VALID_DATE_MASKED = "12/12/2012"
VALID_DATE_ISO = "12-12-2012"

def test_process_bind_param_string():
    t = SQLAlchemyDateType()
    assert t.process_bind_param(VALID_DATE_MASKED, None) == VALID_DATE_ISO

def test_process_bind_param_date_object():
    t = SQLAlchemyDateType()
    date = Date(VALID_DATE_MASKED)
    assert t.process_bind_param(date, None) == VALID_DATE_ISO

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyDateType()
    model = DateModel(date=VALID_DATE_ISO)
    assert t.process_bind_param(model, None) == VALID_DATE_ISO

def test_process_result_value_without_pydantic():
    t = SQLAlchemyDateType()
    result = t.process_result_value(VALID_DATE_ISO, None)

    if PYDANTIC:
        assert isinstance(result, DateModel)
        assert result.date.formatted == VALID_DATE_ISO
    else:
        assert isinstance(result, Date)
        assert result.formatted == VALID_DATE_ISO

def test_process_literal_param():
    t = SQLAlchemyDateType()
    assert t.process_literal_param(VALID_DATE_MASKED, None) == VALID_DATE_ISO
