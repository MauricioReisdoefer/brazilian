import pytest
from brazilian.utils.brazilian_time import (
    _only_digits,
    _split_time,
    Time
)
from brazilian.errors.invalid_time_error import InvalidTimeError

def test_only_digits():
    assert _only_digits("12:30") == "1230"
    assert _only_digits("ab12c30") == "1230"
    assert _only_digits(None) == ""
    assert _only_digits("") == ""

@pytest.mark.parametrize("value,expected", [
    ("12:30", ("12", "30")),
    ("12-30", ("12", "30")),
    ("1230", ("12", "30")),
    ("07:05", ("07", "05")),
    ("0705", ("07", "05")),
    ("7:5", ("7", "5")),
    ("", None),
    (None, None),
    ("abc", None),
])
def test_split_time(value, expected):
    assert _split_time(value) == expected

def test_time_constructor_valid():
    t = Time("12:30")
    assert t.hour == "12"
    assert t.minute == "30"

def test_time_constructor_invalid():
    with pytest.raises(InvalidTimeError):
        Time("25:00")
        
@pytest.mark.parametrize("value,is_valid", [
    ("00:00", True),
    ("23:59", True),
    ("24:00", False),
    ("12:60", False),
    ("99:99", False),
    ("1230", True),
    ("7:5", True),
])
def test_time_is_valid(value, is_valid):
    assert Time.validate(value) == is_valid

def test_time_raise_error():
    with pytest.raises(InvalidTimeError):
        Time.validate("99:99", raise_error=True)

def test_time_formatted():
    t = Time("7:5")
    assert t.formatted == "07:05"

def test_time_iso():
    t = Time("7-5")
    assert t.iso == "07:05"

def test_time_self_validate():
    t = Time("23:59")
    assert t.self_validate() is True

def test_time_self_to_dict():
    t = Time("12:30")
    data = t.self_to_dict()

    assert data["hour"] == "12"
    assert data["minute"] == "30"
    assert data["formatted"] == "12:30"
    assert data["iso"] == "12:30"
    assert data["is_valid"] is True

def test_time_clean():
    assert Time.clean("12:30") == "1230"

def test_time_str():
    assert str(Time("7:5")) == "07:05"

def test_time_repr():
    assert repr(Time("7:5")) == "Time('07:05')"

def test_time_eq_with_time():
    assert Time("12:30") == Time("12-30")

def test_time_eq_with_str():
    assert Time("12:30") == "1230"

def test_time_eq_invalid_str():
    assert Time("12:30") != "invalid"

def test_time_hash():
    t1 = Time("12:30")
    t2 = Time("1230")
    assert hash(t1) == hash(t2)

def test_time_strict_false():
    t = Time("99:99", strict=False)
    assert t.hour == "99"
    assert t.minute == "99"
    assert t.is_valid is False
