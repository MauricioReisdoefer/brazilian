try:
    from sqlalchemy.types import TypeDecorator
    from sqlalchemy.dialects.postgresql import CHAR
except ImportError as e:
    raise ImportError(
        "Para usar o módulo SQLAlchemy do brazilian, instale o extra `brazilian[sqlalchemy]`."
    ) from e
from ..documents.cpf import CPF

try:
    from ..pydantic.cpf_model import CPFModel
    _PYDANTIC_AVAILABLE = True
except ImportError:
    CPFModel = None
    _PYDANTIC_AVAILABLE = False


class CPF_SQL_Type(TypeDecorator):
    """
    Armazena como string limpa (11 dígitos) e retorna como objeto CPFModel (se Pydantic disponível),
    senão retorna como objeto CPF.
    """
    impl = CHAR(11)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Chamado ao salvar no banco."""
        if value is None:
            return None
        
        if isinstance(value, CPF):
            return value.value

        if _PYDANTIC_AVAILABLE and isinstance(value, CPFModel):
            return value.cpf.value

        return CPF.clean(value)

    def process_result_value(self, value, dialect):
        """Chamado ao retornar do banco."""
        if value is None:
            return None

        if _PYDANTIC_AVAILABLE:
            return CPFModel(cpf=value)

        return CPF(value, strict=False)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)
