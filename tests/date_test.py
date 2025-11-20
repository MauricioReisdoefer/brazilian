import pytest
from src.brazilian.utils.brazilian_date import (
    _only_digits,
    _split_date,
    _is_leap_year,
    Date
)
from src.brazilian.errors.invalid_date_error import InvalidDateError

def test_only_digits():
    assert _only_digits("12-03-2025") == "12032025"
    assert _only_digits("abc2025") == "2025"
    assert _only_digits(None) == ""
    assert _only_digits("") == ""

@pytest.mark.parametrize("value,expected", [
    ("12-03-2025", ("12", "03", "2025")),
    ("12/03/2025", ("12", "03", "2025")),
    ("2025-03-12", ("12", "03", "2025")),
    ("2025/03/12", ("12", "03", "2025")),
    ("12.03.2025", ("12", "03", "2025")),
    ("03-2025", None),
    ("", None),
    (None, None),
])
def test_split_date(value, expected):
    assert _split_date(value) == expected

@pytest.mark.parametrize("year,is_leap", [
    (2000, True),  
    (2020, True), 
    (1900, False), 
    (2021, False),
])
def test_is_leap_year(year, is_leap):
    assert _is_leap_year(year) == is_leap

def test_date_constructor_valid():
    d = Date("12-03-2025")
    assert d.day == "12"
    assert d.month == "03"
    assert d.year == "2025"

def test_date_constructor_invalid():
    with pytest.raises(InvalidDateError):
        Date("99-99-9999")

@pytest.mark.parametrize("value,is_valid", [
    ("29-02-2020", True),  
    ("29-02-2021", False),
    ("31-04-2024", False),
    ("15-13-2024", False),
    ("01-01-0000", True),
])
def test_date_is_valid(value, is_valid):
    assert Date.validate(value) == is_valid

def test_date_raise_error():
    with pytest.raises(InvalidDateError):
        Date.validate("31-04-2024", raise_error=True)

def test_date_formatted():
    d = Date("1/1/2024")
    assert d.formatted == "01-01-2024"

def test_date_iso():
    d = Date("1/1/2024")
    assert d.iso == "2024-01-01"

def test_date_self_validate():
    d = Date("29/02/2020")
    assert d.self_validate() is True

def test_date_self_to_dict():
    d = Date("12-03-2025")
    data = d.self_to_dict()
    assert data["day"] == "12"
    assert data["month"] == "03"
    assert data["year"] == "2025"
    assert data["formatted"] == "12-03-2025"
    assert data["iso"] == "2025-03-12"
    assert data["is_valid"] is True

def test_date_clean():
    assert Date.clean("12/03/2025") == "12032025"

def test_date_str():
    assert str(Date("1/1/2024")) == "01-01-2024"

def test_date_repr():
    assert repr(Date("1/1/2024")) == "Date('01-01-2024')"

def test_date_eq_with_date():
    assert Date("01-01-2024") == Date("2024-01-01")

def test_date_eq_with_str():
    assert Date("01-01-2024") == "2024/01/01"

def test_date_eq_invalid_str():
    assert Date("01-01-2024") != "invalid"

def test_date_hash():
    d1 = Date("01-01-2024")
    d2 = Date("2024-01-01")
    assert hash(d1) == hash(d2)

def test_date_strict_false():
    d = Date("99-99-9999", strict=False)
    assert d.day == "99"
    assert d.is_valid is False
