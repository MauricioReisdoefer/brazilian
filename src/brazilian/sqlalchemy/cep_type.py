try:
    from sqlalchemy.types import TypeDecorator
    from sqlalchemy.dialects.postgresql import CHAR
except ImportError as e:
    raise ImportError(
        "Para usar o módulo SQLAlchemy do brazilian, instale o extra `brazilian[sqlalchemy]`."
    ) from e
from ..documents.cep import CEP

try:
    from ..pydantic.cep_model import CEPModel
    _PYDANTIC_AVAILABLE = True
except ImportError:
    CEPModel = None
    _PYDANTIC_AVAILABLE = False


class SQLAlchemyCEPType(TypeDecorator):
    """
    Armazena como string limpa (8 dígitos) e retorna como objeto CEPModel (se Pydantic disponível),
    senão retorna como objeto CEP.
    """
    impl = CHAR(8)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Chamado ao salvar no banco."""
        if value is None:
            return None
        
        if isinstance(value, CEP):
            return value.value

        if _PYDANTIC_AVAILABLE and isinstance(value, CEPModel):
            return value.cep.value

        return CEP.clean(value)

    def process_result_value(self, value, dialect):
        """Chamado ao retornar do banco."""
        if value is None:
            return None

        if _PYDANTIC_AVAILABLE:
            return CEPModel(cep=value)

        return CEP(value, strict=False)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)
