import pytest
from brazilian.documents.cnh import CNH
from brazilian.errors.invalid_cnh_error import InvalidCNHError

def test_cnh_constructor_valid():
    cnh = CNH("123.456.789-01")
    assert cnh.value == "12345678901"

def test_cnh_constructor_invalid_strict():
    with pytest.raises(InvalidCNHError):
        CNH("111.111.111-11", strict=True)

def test_cnh_constructor_non_strict():
    cnh = CNH("111.111.111-11", strict=False)
    assert cnh.value == "11111111111"
    assert not cnh.is_valid

def test_value_property():
    cnh = CNH("12345678901")
    assert cnh.value == "12345678901"

def test_digits_property():
    cnh = CNH("12345678901")
    assert cnh.digits == tuple(int(d) for d in "12345678901")

def test_is_valid_true():
    assert CNH("12345678901").is_valid

def test_is_valid_false():
    assert not CNH("11111111111", strict=False).is_valid

def test_formatted_property():
    cnh = CNH("12345678901")
    assert cnh.formatted == "123 456 789 01"

def test_masked_property():
    cnh = CNH("12345678901")
    assert cnh.masked == "*** *** *** 01"

def test_self_validate_valid():
    cnh = CNH("12345678901")
    assert cnh.self_validate() is True

def test_self_validate_invalid_raises():
    cnh = CNH("11111111111", strict=False)
    with pytest.raises(InvalidCNHError):
        cnh.self_validate(raise_error=True)

def test_self_format():
    cnh = CNH("12345678901")
    assert cnh.self_format() == "123 456 789 01"

def test_self_mask():
    cnh = CNH("12345678901")
    assert cnh.self_mask() == "*** *** *** 01"

def test_self_to_dict():
    cnh = CNH("12345678901")
    d = cnh.self_to_dict()
    assert d["value"] == "12345678901"
    assert d["formatted"] == "123 456 789 01"
    assert d["masked"] == "*** *** *** 01"
    assert d["is_valid"] is True

def test_clean():
    assert CNH.clean("123.456.789-01") == "12345678901"

def test_validate_valid():
    assert CNH.validate("12345678901") is True

def test_validate_invalid():
    assert CNH.validate("11111111111") is False

def test_validate_invalid_raises():
    with pytest.raises(InvalidCNHError):
        CNH.validate("11111111111", raise_error=True)

def test_generate_returns_valid_cnh():
    cnh = CNH.generate()
    assert isinstance(cnh, CNH)
    assert cnh.is_valid

def test_generate_formatted():
    formatted = CNH.generate(formatted=True)
    assert isinstance(formatted, str)
    assert len(formatted) == 14  # "123 456 789 01"

def test_random_str_raw():
    s = CNH.random_str(formatted=False)
    assert len(s) == 11

def test_random_str_formatted():
    s = CNH.random_str(formatted=True)
    assert len(s) == 14

def test_format_static():
    assert CNH.format("12345678901") == "123 456 789 01"

def test_str():
    assert str(CNH("12345678901")) == "123 456 789 01"

def test_repr():
    assert repr(CNH("12345678901")) == "CNH('123 456 789 01')"

def test_eq_same():
    assert CNH("12345678901") == CNH("12345678901")

def test_eq_str():
    assert CNH("12345678901") == "123 456 789 01"

def test_len():
    assert len(CNH("12345678901")) == 11

def test_hash():
    assert isinstance(hash(CNH("12345678901")), int)
