try:
    from sqlalchemy.types import TypeDecorator
    from sqlalchemy.dialects.postgresql import CHAR
except ImportError as e:
    raise ImportError(
        "Para usar o módulo SQLAlchemy do brazilian, instale o extra `brazilian[sqlalchemy]`."
    ) from e
from ..documents.crm import CRM

try:
    from ..pydantic.crm_model import CRMModel
    _PYDANTIC_AVAILABLE = True
except ImportError:
    CRMModel = None
    _PYDANTIC_AVAILABLE = False


class SQLAlchemyCRMType(TypeDecorator):
    """
    Armazena como string limpa (10 dígitos) e retorna como objeto CRMModel (se Pydantic disponível),
    senão retorna como objeto CRM.
    """
    impl = CHAR(10)
    cache_ok = True

    def process_bind_param(self, value, dialect):
        """Chamado ao salvar no banco."""
        if value is None:
            return None
        
        if isinstance(value, CRM):
            return value.value

        if _PYDANTIC_AVAILABLE and isinstance(value, CRMModel):
            return value.crm.value

        return CRM.clean(value)

    def process_result_value(self, value, dialect):
        """Chamado ao retornar do banco."""
        if value is None:
            return None

        if _PYDANTIC_AVAILABLE:
            return CRMModel(crm=value)

        return CRM(value, strict=False)

    def process_literal_param(self, value, dialect):
        return self.process_bind_param(value, dialect)
