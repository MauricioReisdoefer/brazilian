import pytest
from pydantic import ValidationError
from brazilian.pydantic.cnpj_model import CNPJModel 
from brazilian.documents.cnpj import CNPJ

def test_valid_cnpj():
    model = CNPJModel(cnpj="45.723.174/0001-10")
    assert isinstance(model.cnpj, CNPJ)
    assert model.cnpj.formatted is not None

def test_invalid_cnpj():
    with pytest.raises(ValidationError):
        CNPJModel(cnpj="asd98ds22")

def test_json_encoder():
    model = CNPJModel(cnpj="45.723.174/0001-10")
    json_output = model.model_dump_json()
    assert model.cnpj.formatted in json_output 

def test_receive_model():
    model = CNPJModel(cnpj=CNPJ("45.723.174/0001-10"))
    assert isinstance(model.cnpj, CNPJ)
    assert model.cnpj.formatted is not None