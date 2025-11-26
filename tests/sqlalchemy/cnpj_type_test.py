import pytest
from brazilian.sqlalchemy.cnpj_type import SQLAlchemyCNPJType
from brazilian.documents.cnpj import CNPJ

try:
    from brazilian.pydantic.cnpj_model import CNPJModel
    PYDANTIC = True
except ImportError:
    CNPJModel = None
    PYDANTIC = False

VALID_CNPJ_MASKED = "01.838.723/0001-27"
VALID_CNPJ_RAW = "01838723000127"

def test_process_bind_param_string():
    t = SQLAlchemyCNPJType()
    assert t.process_bind_param(VALID_CNPJ_MASKED, None) == VALID_CNPJ_RAW

def test_process_bind_param_cnpj_object():
    t = SQLAlchemyCNPJType()
    cnpj = CNPJ(VALID_CNPJ_MASKED)
    assert t.process_bind_param(cnpj, None) == VALID_CNPJ_RAW

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyCNPJType()
    model = CNPJModel(cnpj=VALID_CNPJ_RAW)
    assert t.process_bind_param(model, None) == VALID_CNPJ_RAW

def test_process_result_value_without_pydantic():
    t = SQLAlchemyCNPJType()
    result = t.process_result_value(VALID_CNPJ_RAW, None)

    if PYDANTIC:
        assert isinstance(result, CNPJModel)
        assert result.cnpj.value == VALID_CNPJ_RAW
    else:
        assert isinstance(result, CNPJ)
        assert result.value == VALID_CNPJ_RAW

def test_process_literal_param():
    t = SQLAlchemyCNPJType()
    assert t.process_literal_param(VALID_CNPJ_MASKED, None) == VALID_CNPJ_RAW

def test_process_bind_param_none():
    t = SQLAlchemyCNPJType()
    assert t.process_bind_param(None, None) == None
    
def test_import_without_pydantic(monkeypatch):
    import importlib
    import sys

    sys.modules.pop('brazilian.pydantic.cnpj_model', None)
    monkeypatch.setitem(sys.modules, 'brazilian.pydantic.cnpj_model', None)

    sys.modules.pop('brazilian.sqlalchemy.cnpj_type', None)
    module = importlib.import_module("brazilian.sqlalchemy.cnpj_type")

    assert module._PYDANTIC_AVAILABLE is False
    assert module.CNPJModel is None