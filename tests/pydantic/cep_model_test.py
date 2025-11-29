import pytest
from pydantic import ValidationError
from brazilian.pydantic.cep_model import CEPModel 
from brazilian.documents.cep import CEP

def test_valid_cep():
    model = CEPModel(cep="12345678")
    assert isinstance(model.cep, CEP)
    assert model.cep.formatted is not None

def test_invalid_cep():
    with pytest.raises(ValidationError):
        CEPModel(cep="abc12345")

def test_json_encoder():
    model = CEPModel(cep="12345678")
    json_output = model.model_dump_json()
    assert model.cep.formatted in json_output 

def test_receive_model():
    model = CEPModel(cep=CEP("12345678"))
    assert isinstance(model.cep, CEP)
    assert model.cep.formatted is not None