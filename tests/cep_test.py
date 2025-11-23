import pytest
from dataclasses import FrozenInstanceError
from unittest.mock import patch, MagicMock
from brazilian.errors.invalid_cep_error import InvalidCEPError
from brazilian.documents.cep import CEP, _only_digits

def test__only_digits():
    assert _only_digits("12a-3.4") == "1234"
    assert _only_digits(None) == ""
    assert _only_digits("") == ""

def test_constructor_valid():
    cep = CEP("12345678")
    assert cep.value == "12345678"

def test_constructor_invalid_strict():
    with pytest.raises(InvalidCEPError):
        CEP("1234", strict=True)

def test_constructor_non_strict():
    cep = CEP("1234", strict=False)
    assert cep.value == "1234"

def test_digits_property():
    cep = CEP("12345678")
    assert cep.digits == (1, 2, 3, 4, 5, 6, 7, 8)

def test_formatted_property():
    assert CEP("12345678").formatted == "12345-678"
    assert CEP("1234", strict=False).formatted == "1234"

def test_masked_property():
    assert CEP("12345678").masked == "*****-678"
    assert CEP("1234", strict=False).masked == "1234"

def test_region_property():
    assert CEP("01001000").region == "SP"

def test_is_valid_property():
    assert CEP("12345678", strict=False).is_valid is True
    assert CEP("01001000", strict=False).is_valid is True

def test_clean():
    assert CEP.clean("12-345") == "12345"

def test_validate_true():
    assert CEP.validate("01001000") is True

def test_validate_false():
    assert CEP.validate("000") is False

def test_validate_raise_error():
    with pytest.raises(InvalidCEPError):
        CEP.validate("000", raise_error=True)

def test_generate():
    cep = CEP.generate()
    assert isinstance(cep, CEP)
    assert len(cep.value) == 8

def test_random_str():
    s = CEP.random_str()
    assert isinstance(s, str)
    assert len(s) == 8

def test_format():
    assert CEP.format("12345678") == "12345-678"

def test_self_format():
    assert CEP("12345678").self_format() == "12345-678"

def test_self_mask():
    assert CEP("12345678").self_mask() == "*****-678"

def test_self_to_dict():
    cep = CEP("12345678")
    d = cep.self_to_dict()
    assert d["value"] == "12345678"
    assert d["formatted"] == "12345-678"
    assert d["masked"] == "*****-678"
    assert d["is_valid"] is True
    assert d["region"] == "SP"

# ---------- Testes com requests (mock) ----------
@patch("src.brazilian.documents.cep.requests.get")
def test_self_get_location(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"localidade": "São Paulo"})
    cep = CEP("01001000")
    result = cep.self_get_location()
    assert result["localidade"] == "São Paulo"

@patch("src.brazilian.documents.cep.requests.get")
def test_self_get_location_error(mock_get):
    mock_get.return_value = MagicMock(status_code=500)
    cep = CEP("01001000")
    with pytest.raises(Exception):
        cep.self_get_location()

@patch("src.brazilian.documents.cep.requests.get")
def test_static_get_location(mock_get):
    mock_get.return_value = MagicMock(status_code=200, json=lambda: {"uf": "SP"})
    result = CEP.get_location(CEP("01001000"))
    assert result["uf"] == "SP"

def test_str_and_repr():
    cep = CEP("12345678")
    assert str(cep) == "12345-678"
    assert repr(cep) == "CEP('12345-678')"

def test_eq():
    cep = CEP("12345678")
    assert cep == CEP("12345678")
    assert cep == "12345678"
    assert cep != "87654321"

def test_len():
    assert len(CEP("12345678")) == 8

def test_hash():
    cep = CEP("12345678")
    assert hash(cep) == hash("12345678")


def test_frozen_class():
    cep = CEP("12345678")
    with pytest.raises(FrozenInstanceError):
        cep._value = "87654321"