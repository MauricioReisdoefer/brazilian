import pytest
from pydantic import ValidationError
from src.brazilian.pydantic.cpf_model import CPFModel 
from src.brazilian.documents.cpf import CPF

def test_valid_cpf():
    model = CPFModel(cpf="529.982.247-25")
    assert isinstance(model.cpf, CPF)
    assert model.cpf.formatted is not None

def test_invalid_cpf():
    with pytest.raises(ValidationError):
        CPFModel(cpf="asd98ds22")

def test_json_encoder():
    model = CPFModel(cpf="529.982.247-25")
    json_output = model.model_dump_json()
    assert model.cpf.formatted in json_output 
