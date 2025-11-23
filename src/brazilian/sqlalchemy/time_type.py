try:
    from sqlalchemy.types import TypeDecorator
    from sqlalchemy.dialects.postgresql import CHAR
except ImportError as e:
    raise ImportError(
        "Para usar o módulo SQLAlchemy do brazilian, instale o extra `brazilian[sqlalchemy]`."
    ) from e
from ..utils.brazilian_time import Time

try:
    from ..pydantic.time_model import TimeModel
    _PYDANTIC_AVAILABLE = True
except ImportError:
    TimeModel = None
    _PYDANTIC_AVAILABLE = False


class SQLAlchemyTimeType(TypeDecorator):
    """
    Armazena como string limpa (11 dígitos) e retorna como objeto TimeModel (se Pydantic disponível),
    senão retorna como objeto Time.
    """
    impl = CHAR(11)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Chamado ao salvar no banco."""
        if value is None:
            return None
        
        if isinstance(value, Time):
            return value.value

        if _PYDANTIC_AVAILABLE and isinstance(value, TimeModel):
            return value.time.value

        return Time.clean(value)

    def process_result_value(self, value, dialect):
        """Chamado ao retornar do banco."""
        if value is None:
            return None

        if _PYDANTIC_AVAILABLE:
            return TimeModel(time=value)

        return Time(value, strict=False)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)
