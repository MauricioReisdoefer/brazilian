import pytest
from src.brazilian.documents.cnpj import CNPJ
from src.brazilian.errors.invalid_cnpj_error import InvalidCNPJError

VALID_CNPJ = "45.723.174/0001-10"
VALID_CNPJ_RAW = "45723174000110"
INVALID_CNPJ = "11.111.111/1111-11"

def test_only_digits():
    assert CNPJ.clean("45.723.174/0001-10") == "45723174000110"
    assert CNPJ.clean("abc457") == "457"
    assert CNPJ.clean(None) == ""

def test_validate_true():
    assert CNPJ.validate(VALID_CNPJ) is True
    assert CNPJ.validate(VALID_CNPJ_RAW) is True


def test_validate_false():
    assert CNPJ.validate(INVALID_CNPJ) is False
    assert CNPJ.validate("123") is False
    assert CNPJ.validate("00000000000000") is False


def test_validate_raises():
    with pytest.raises(InvalidCNPJError):
        CNPJ.validate(INVALID_CNPJ, raise_error=True)

def test_constructor_valid():
    c = CNPJ(VALID_CNPJ)
    assert c.value == VALID_CNPJ_RAW
    assert c.is_valid is True


def test_constructor_invalid():
    with pytest.raises(InvalidCNPJError):
        CNPJ(INVALID_CNPJ)


def test_constructor_no_strict():
    c = CNPJ(INVALID_CNPJ, strict=False)
    assert c.value == "11111111111111"
    assert c.is_valid is False

def test_formatted():
    c = CNPJ(VALID_CNPJ)
    assert c.formatted == VALID_CNPJ


def test_formatted_invalid_length():
    c = CNPJ("123456", strict=False)
    assert c.formatted == "123456"

def test_masked():
    c = CNPJ(VALID_CNPJ)
    assert c.masked == "**.***.***/0001-10"

def test_masked_invalid_length():
    c = CNPJ("1234", strict=False)
    assert c.masked == "1234"

def test_is_valid():
    assert CNPJ(VALID_CNPJ).is_valid is True
    assert CNPJ(INVALID_CNPJ, strict=False).is_valid is False

def test_length():
    assert len(CNPJ(VALID_CNPJ)) == 14

def test_eq_same():
    assert CNPJ(VALID_CNPJ) == CNPJ(VALID_CNPJ_RAW)

def test_eq_string():
    assert CNPJ(VALID_CNPJ) == VALID_CNPJ_RAW


def test_eq_false():
    assert CNPJ(VALID_CNPJ) != CNPJ("12345678901234", strict=False)

def test_str():
    assert str(CNPJ(VALID_CNPJ)) == VALID_CNPJ


def test_repr():
    assert repr(CNPJ(VALID_CNPJ)) == f"CNPJ('{VALID_CNPJ}')"

def test_generate_raw():
    c = CNPJ.generate()
    assert isinstance(c, CNPJ)
    assert len(c.value) == 14
    assert c.is_valid is True

def test_generate_formatted():
    f = CNPJ.generate(formatted=True)
    assert isinstance(f, str)
    assert len(f) == 18  

def test_random_str_raw():
    r = CNPJ.random_str()
    assert isinstance(r, str)
    assert len(r) == 14


def test_random_str_formatted():
    r = CNPJ.random_str(formatted=True)
    assert isinstance(r, str)
    assert len(r) == 18

def test_digits():
    c = CNPJ(VALID_CNPJ)
    assert c.digits == tuple(int(x) for x in VALID_CNPJ_RAW)

def test_self_to_dict():
    c = CNPJ(VALID_CNPJ)
    d = c.self_to_dict()

    assert d["value"] == VALID_CNPJ_RAW
    assert d["formatted"] == VALID_CNPJ
    assert d["masked"] == "**.***.***/0001-10"
    assert d["is_valid"] is True
