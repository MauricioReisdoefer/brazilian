import pytest
from brazilian.sqlalchemy.crm_type import SQLAlchemyCRMType
from brazilian.documents.crm import CRM

try:
    from brazilian.pydantic.crm_model import CRMModel
    PYDANTIC = True
except ImportError:
    CRMModel = None
    PYDANTIC = False

VALID_CRM_MASKED = "123456-SP"
VALID_CRM_RAW = "123456SP"

def test_process_bind_param_string():
    t = SQLAlchemyCRMType()
    assert t.process_bind_param(VALID_CRM_MASKED, None) == VALID_CRM_RAW

def test_process_bind_param_crm_object():
    t = SQLAlchemyCRMType()
    crm = CRM(VALID_CRM_MASKED)
    assert t.process_bind_param(crm, None) == VALID_CRM_RAW

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyCRMType()
    model = CRMModel(crm=VALID_CRM_RAW)
    assert t.process_bind_param(model, None) == VALID_CRM_RAW

def test_process_result_value_without_pydantic():
    t = SQLAlchemyCRMType()
    result = t.process_result_value(VALID_CRM_RAW, None)

    if PYDANTIC:
        assert isinstance(result, CRMModel)
        assert result.crm.value == VALID_CRM_RAW
    else:
        assert isinstance(result, CRM)
        assert result.value == VALID_CRM_RAW

def test_process_literal_param():
    t = SQLAlchemyCRMType()
    assert t.process_literal_param(VALID_CRM_MASKED, None) == VALID_CRM_RAW

def test_process_bind_param_none():
    t = SQLAlchemyCRMType()
    assert t.process_bind_param(None, None) == None
    
def test_import_without_pydantic(monkeypatch):
    import importlib
    import sys

    sys.modules.pop('brazilian.pydantic.crm_model', None)
    monkeypatch.setitem(sys.modules, 'brazilian.pydantic.crm_model', None)

    sys.modules.pop('brazilian.sqlalchemy.crm_type', None)
    module = importlib.import_module("brazilian.sqlalchemy.crm_type")

    assert module._PYDANTIC_AVAILABLE is False
    assert module.CRMModel is None