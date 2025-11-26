import pytest
from brazilian.sqlalchemy.cpf_type import SQLAlchemyCPFType
from brazilian.documents.cpf import CPF

try:
    from brazilian.pydantic.cpf_model import CPFModel
    PYDANTIC = True
except ImportError:
    CPFModel = None
    PYDANTIC = False

def test_process_bind_param_string():
    t = SQLAlchemyCPFType()
    assert t.process_bind_param("123.456.789-09", None) == "12345678909"

def test_process_bind_param_cpf_object():
    t = SQLAlchemyCPFType()
    cpf = CPF("123.456.789-09")
    assert t.process_bind_param(cpf, None) == "12345678909"

@pytest.mark.skipif(not PYDANTIC, reason="Pydantic não instalado")
def test_process_bind_param_with_pydantic():
    t = SQLAlchemyCPFType()
    model = CPFModel(cpf="12345678909")
    assert t.process_bind_param(model, None) == "12345678909"

def test_process_result_value_without_pydantic():
    t = SQLAlchemyCPFType()
    result = t.process_result_value("12345678909", None)

    if PYDANTIC:
        assert isinstance(result, CPFModel)
        assert result.cpf.value == "12345678909"
    else:
        assert isinstance(result, CPF)
        assert result.value == "12345678909"

def test_process_literal_param():
    t = SQLAlchemyCPFType()
    assert t.process_literal_param("123.456.789-09", None) == "12345678909"
