import pytest
from brazilian.sqlalchemy.cep_type import SQLAlchemyCEPType
from brazilian.documents.cep import CEP

try:
    from brazilian.pydantic.cep_model import CEPModel
    PYDANTIC = True
except ImportError:
    CEPModel = None
    PYDANTIC = False

VALID_CEP_MASKED = "01001-000"
VALID_CEP_RAW = "01001000"

def test_process_bind_param_string():
    t = SQLAlchemyCEPType()
    assert t.process_bind_param(VALID_CEP_MASKED, None) == VALID_CEP_RAW

def test_process_bind_param_cep_object():
    t = SQLAlchemyCEPType()
    cep = CEP(VALID_CEP_MASKED)
    assert t.process_bind_param(cep, None) == VALID_CEP_RAW

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyCEPType()
    model = CEPModel(cep=VALID_CEP_RAW)
    assert t.process_bind_param(model, None) == VALID_CEP_RAW

def test_process_result_value_without_pydantic():
    t = SQLAlchemyCEPType()
    result = t.process_result_value(VALID_CEP_RAW, None)

    if PYDANTIC:
        assert isinstance(result, CEPModel)
        assert result.cep.value == VALID_CEP_RAW
    else:
        assert isinstance(result, CEP)
        assert result.value == VALID_CEP_RAW

def test_process_literal_param():
    t = SQLAlchemyCEPType()
    assert t.process_literal_param(VALID_CEP_MASKED, None) == VALID_CEP_RAW

def test_process_bind_param_none():
    t = SQLAlchemyCEPType()
    assert t.process_bind_param(None, None) == None

def test_import_without_pydantic(monkeypatch):
    import importlib
    import sys

    sys.modules.pop('brazilian.pydantic.cep_model', None)
    monkeypatch.setitem(sys.modules, 'brazilian.pydantic.cep_model', None)

    sys.modules.pop('brazilian.sqlalchemy.cep_type', None)
    module = importlib.import_module("brazilian.sqlalchemy.cep_type")

    assert module._PYDANTIC_AVAILABLE is False
    assert module.CEPModel is None