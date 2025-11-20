# Documentação da Classe Date

A classe `Date` é uma implementação para manipulação, validação e formatação de datas. Ela encapsula a lógica de validação de datas (incluindo anos bissextos) e oferece métodos utilitários para formatação nos padrões brasileiro e ISO.

## Estrutura da Classe

A classe `Date` é definida como um `dataclass` imutável (`frozen=True`), garantindo que os componentes da data (dia, mês e ano) não sejam alterados após a inicialização.

```python
@dataclass(frozen=True)
class Date:
    _day: str
    _month: str
    _year: str
    # ...
```

### Inicialização

O construtor aceita uma string de data (que pode estar em diferentes formatos) e um parâmetro opcional `strict`.

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `value` | `str` | A string de data a ser encapsulada. Formatos aceitos: `DD-MM-YYYY`, `DD/MM/YYYY`, `YYYY-MM-DD`, `YYYY/MM/DD`. | (Obrigatório) |
| `strict` | `bool` | Se `True`, a validação completa é executada na inicialização e um `InvalidDateError` é levantado se a data for inválida. | `True` |

```python
def __init__(self, value: str, *, strict: bool = True):
    # ...
```

**Exceção:**

- `InvalidDateError`: Levantada se a string de data não puder ser parseada ou se a data for inválida (e `strict=True`).

## Propriedades da Instância

As propriedades fornecem acesso aos componentes da data e suas representações formatadas.

| Propriedade | Tipo | Descrição |
| :--- | :--- | :--- |
| `day` | `str` | O dia da data como string. |
| `month` | `str` | O mês da data como string. |
| `year` | `str` | O ano da data como string. |
| `formatted` | `str` | A data formatada no padrão brasileiro `DD-MM-YYYY`. |
| `iso` | `str` | A data formatada no padrão ISO `YYYY-MM-DD`. |
| `is_valid` | `bool` | Retorna `True` se a data for válida de acordo com as regras de validação. |

## Métodos de Instância

| Método | Descrição |
| :--- | :--- |
| `self_validate(*, raise_error: bool = False) -> bool` | Valida a instância atual. Se `raise_error` for `True` e a data for inválida, levanta `InvalidDateError`. |
| `self_to_dict() -> dict` | Retorna um dicionário com as principais informações da instância: `day`, `month`, `year`, `formatted`, `iso` e `is_valid`. |

## Métodos Estáticos (Utilitários)

| Método | Descrição |
| :--- | :--- |
| `validate(value: str, raise_error: bool = False) -> bool` | Valida uma data fornecida como string. Se `raise_error` for `True` e a data for inválida, levanta `InvalidDateError`. |
| `clean(value: str) -> str` | Remove todos os caracteres não numéricos de uma string, retornando apenas os dígitos da data. |

## Métodos Mágicos (`Dunder Methods`)

A classe implementa vários métodos mágicos para facilitar a interação e comparação.

| Método | Comportamento |
| :--- | :--- |
| `__str__` | Retorna a data formatada no padrão `DD-MM-YYYY`. |
| `__repr__` | Retorna uma representação de string que pode ser usada para recriar o objeto (ex: `Date('DD-MM-YYYY')`). |
| `__eq__` | Permite a comparação de igualdade com outra instância `Date` ou com uma string de data (que é automaticamente convertida para `Date` para comparação). |
| `__hash__` | Permite que instâncias de `Date` sejam usadas como chaves em dicionários ou elementos em conjuntos, baseado na representação ISO. |
