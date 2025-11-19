import pytest
from src.brazilian.documents.crm import CRM, _clean_crm, UF_LIST
from src.brazilian.errors.invalid_crm_error import InvalidCRMError

def test_clean_crm():
    assert _clean_crm(" 12345-sp ") == "12345SP"
    assert _clean_crm("12.345/SC") == "12345SC"
    assert _clean_crm("") == ""
    assert _clean_crm(None) == ""

def test_crm_number_extraction():
    crm = CRM("123456SP")
    assert crm.number == "123456"

def test_crm_uf_acronym():
    crm = CRM("123456SP")
    assert crm.uf_acronym == "SP"

def test_crm_uf_name():
    crm = CRM("123456MG")
    assert crm.uf == "Minas Gerais"

def test_crm_region():
    crm = CRM("123456RJ")
    assert crm.region == "Sudeste"
    
def test_crm_valid():
    crm = CRM("12345SP", strict=True)
    assert crm.is_valid is True

def test_crm_invalid_no_number():
    with pytest.raises(InvalidCRMError):
        CRM("SP", strict=True)

def test_crm_invalid_no_letters():
    with pytest.raises(InvalidCRMError):
        CRM("12345", strict=True)

def test_crm_invalid_uf():
    with pytest.raises(InvalidCRMError):
        CRM("12345XX", strict=True)

def test_crm_invalid_too_short_number():
    with pytest.raises(InvalidCRMError):
        CRM("123SP", strict=True)

def test_crm_invalid_too_long_number():
    with pytest.raises(InvalidCRMError):
        CRM("1234567SP", strict=True)

def test_crm_formatted():
    crm = CRM("123456SP")
    assert crm.formatted == "123456-Sao Paulo"

def test_crm_format_static():
    assert CRM.format("123456SP") == "123456-Sao Paulo"

def test_crm_masked():
    crm = CRM("123456SP")
    assert crm.masked == "***456-Sao Paulo"

def test_crm_masked_short_number():
    crm = CRM("1234SP")
    assert crm.masked == "*234-Sao Paulo"

    crm = CRM.generate()
    assert len(crm.number) >= 4
    assert len(crm.number) <= 6
    assert crm.uf_acronym in UF_LIST
    assert crm.is_valid

def test_crm_generate_specific_uf():
    crm = CRM.generate("RJ")
    assert crm.uf_acronym == "RJ"
    assert crm.uf == "Rio de Janeiro"

def test_crm_random_str():
    s = CRM.random_str()
    assert isinstance(s, str)
    assert len(s) >= 6  
    
def test_crm_to_dict():
    crm = CRM("123456SP")
    d = crm.self_to_dict()

    assert d["value"] == "123456SP"
    assert d["formatted"] == "123456-Sao Paulo"
    assert d["masked"] == "***456-Sao Paulo"
    assert d["is_valid"] is True
    assert d["uf"] == "Sao Paulo"
    assert d["region"] == "Sudeste"

def test_crm_equality():
    a = CRM("123456SP")
    b = CRM("123456sp")
    assert a == b

def test_crm_hash():
    a = CRM("123456SP")
    b = CRM("123456SP")
    assert hash(a) == hash(b)
