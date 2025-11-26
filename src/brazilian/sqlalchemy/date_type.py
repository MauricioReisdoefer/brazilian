try:
    from sqlalchemy.types import TypeDecorator
    from sqlalchemy.dialects.postgresql import CHAR
except ImportError as e:
    raise ImportError(
        "Para usar o módulo SQLAlchemy do brazilian, instale o extra `brazilian[sqlalchemy]`."
    ) from e
from ..utils.brazilian_date import Date

try:
    from ..pydantic.date_model import DateModel
    _PYDANTIC_AVAILABLE = True
except ImportError:
    DateModel = None
    _PYDANTIC_AVAILABLE = False


class SQLAlchemyDateType(TypeDecorator):
    """
    Armazena como string limpa (11 dígitos) e retorna como objeto DateModel (se Pydantic disponível),
    senão retorna como objeto Date.
    """
    impl = CHAR(11)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Chamado ao salvar no banco."""
        if value is None:
            return None
        
        if isinstance(value, Date):
            return value.formatted

        if _PYDANTIC_AVAILABLE and isinstance(value, DateModel):
            return value.date.formatted

        return Date(value).formatted

    def process_result_value(self, value, dialect):
        """Chamado ao retornar do banco."""
        if value is None:
            return None

        if _PYDANTIC_AVAILABLE:
            return DateModel(date=value)

        return Date(value, strict=False)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)
