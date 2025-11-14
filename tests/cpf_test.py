import pytest
from brazilian.documents.cpf import CPF
from brazilian.errors.invalid_cpf_error import InvalidCPFError

def test_cpf_constructor_valid():
    cpf = CPF("529.982.247-25")
    assert cpf.value == "52998224725"


def test_cpf_constructor_invalid_strict():
    with pytest.raises(InvalidCPFError):
        CPF("111.111.111-11", strict=True)


def test_cpf_constructor_non_strict():
    cpf = CPF("111.111.111-11", strict=False)
    assert cpf.value == "11111111111"
    assert not cpf.is_valid

def test_value_property():
    cpf = CPF("52998224725")
    assert cpf.value == "52998224725"


def test_digits_property():
    cpf = CPF("52998224725")
    assert cpf.digits == tuple(int(d) for d in "52998224725")


def test_is_valid_true():
    assert CPF("52998224725").is_valid


def test_is_valid_false():
    assert not CPF("11111111111", strict=False).is_valid


def test_region_property():
    cpf = CPF("52998224725") 
    assert cpf.region == "Rio de Janeiro, Espirito Santo"


def test_region_acronym_property():
    cpf = CPF("52998224725")  
    assert cpf.region_acronym == "RJ, ES"


def test_formatted_property():
    cpf = CPF("52998224725")
    assert cpf.formatted == "529.982.247-25"


def test_masked_property():
    cpf = CPF("52998224725")
    assert cpf.masked == "***.***.***-25"

def test_self_validate_valid():
    cpf = CPF("52998224725")
    assert cpf.self_validate() is True


def test_self_validate_invalid_raises():
    cpf = CPF("11111111111", strict=False)
    with pytest.raises(InvalidCPFError):
        cpf.self_validate(raise_error=True)

def test_self_format():
    cpf = CPF("52998224725")
    assert cpf.self_format() == "529.982.247-25"


def test_self_mask():
    cpf = CPF("52998224725")
    assert cpf.self_mask() == "***.***.***-25"


def test_self_to_dict():
    cpf = CPF("52998224725")
    d = cpf.self_to_dict()
    assert d["value"] == "52998224725"
    assert d["formatted"] == "529.982.247-25"
    assert d["masked"] == "***.***.***-25"
    assert d["is_valid"] is True
    assert "region" in d

def test_clean():
    assert CPF.clean("529.982.247-25") == "52998224725"


def test_validate_valid():
    assert CPF.validate("52998224725") is True


def test_validate_invalid():
    assert CPF.validate("11111111111") is False


def test_validate_invalid_raises():
    with pytest.raises(InvalidCPFError):
        CPF.validate("11111111111", raise_error=True)


def test_generate_returns_valid_cpf():
    cpf = CPF.generate()
    assert isinstance(cpf, CPF)
    assert cpf.is_valid


def test_generate_formatted():
    formatted = CPF.generate(formatted=True)
    assert isinstance(formatted, str)
    assert len(formatted) == 14


def test_random_str_raw():
    s = CPF.random_str(formatted=False)
    assert len(s) == 11


def test_random_str_formatted():
    s = CPF.random_str(formatted=True)
    assert len(s) == 14

def test_format_static():
    assert CPF.format("52998224725") == "529.982.247-25"

def test_str():
    assert str(CPF("52998224725")) == "529.982.247-25"


def test_repr():
    assert repr(CPF("52998224725")) == "CPF('529.982.247-25')"


def test_eq_same():
    assert CPF("52998224725") == CPF("52998224725")


def test_eq_str():
    assert CPF("52998224725") == "529.982.247-25"


def test_len():
    assert len(CPF("52998224725")) == 11


def test_hash():
    assert isinstance(hash(CPF("52998224725")), int)
