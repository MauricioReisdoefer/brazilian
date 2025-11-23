import pytest
from pydantic import ValidationError
from brazilian.pydantic.crm_model import CRMModel 
from brazilian.documents.crm import CRM

def test_valid_crm():
    model = CRMModel(crm="123456/SC")
    assert isinstance(model.crm, CRM)
    assert model.crm.formatted is not None

def test_invalid_crm():
    with pytest.raises(ValidationError):
        CRMModel(crm="abc1ass2345")

def test_json_encoder():
    model = CRMModel(crm="123456/SC")
    json_output = model.model_dump_json()
    assert model.crm.formatted in json_output 
