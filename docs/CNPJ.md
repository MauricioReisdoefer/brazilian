# Documentação da Classe CNPJ

A classe `CNPJ` é uma implementação robusta para manipulação, validação, formatação e geração de números de Cadastro Nacional da Pessoa Jurídica (CNPJ) no Brasil. Ela encapsula a lógica de validação de acordo com as regras oficiais e oferece métodos utilitários para formatação, mascaramento e geração.

## Estrutura da Classe

A classe `CNPJ` é definida como um `dataclass` imutável (`frozen=True`), garantindo que o valor do CNPJ não seja alterado após a inicialização.

```python
@dataclass(frozen=True)
class CNPJ:
    _value: str
    # ...
```

### Inicialização

O construtor aceita um valor de CNPJ (que pode estar formatado ou não) e um parâmetro opcional `strict`.

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `value` | `str` ou `None` | O número do CNPJ a ser encapsulado. Será limpo para conter apenas dígitos. | `None` |
| `strict` | `bool` | Se `True`, a validação é executada na inicialização e um `InvalidCNPJError` é levantado se o CNPJ for inválido. | `True` |

```python
def __init__(self, value=None, *, strict: bool = True):
    # ...
```

## Propriedades da Instância

| Propriedade | Tipo | Descrição |
| :--- | :--- | :--- |
| `value` | `str` | O valor do CNPJ contendo apenas os 14 dígitos. |
| `digits` | `tuple` | Uma tupla de inteiros representando cada dígito do CNPJ. |
| `is_valid` | `bool` | Retorna `True` se o CNPJ for válido de acordo com as regras de cálculo. |
| `formatted` | `str` | O CNPJ formatado no padrão `XX.XXX.XXX/XXXX-XX`. Retorna o valor original se não tiver 14 dígitos. |
| `masked` | `str` | O CNPJ mascarado no padrão `**.***.***/XXXX-XX`, exibindo apenas a raiz e os dois dígitos verificadores. Retorna o valor original se não tiver 14 dígitos. |

## Métodos de Instância

| Método | Descrição |
| :--- | :--- |
| `self_validate(*, raise_error: bool = False) -> bool` | Valida a instância atual. Se `raise_error` for `True` e o CNPJ for inválido, levanta `InvalidCNPJError`. |
| `self_format() -> str` | Retorna o CNPJ formatado (equivalente a `self.formatted`). |
| `self_mask() -> str` | Retorna o CNPJ mascarado (equivalente a `self.masked`). |
| `self_to_dict() -> dict` | Retorna um dicionário com as principais informações da instância: `value`, `formatted`, `masked` e `is_valid`. |

## Métodos Estáticos (Utilitários)

| Método | Descrição |
| :--- | :--- |
| `clean(value: str) -> str` | Remove todos os caracteres não numéricos de uma string, retornando apenas os dígitos. |
| `validate(value: str, raise_error: bool = False) -> bool` | Valida um CNPJ fornecido como string. Se `raise_error` for `True` e o CNPJ for inválido, levanta `InvalidCNPJError`. |
| `generate(formatted: bool = False) -> "CNPJ" ou "str"` | Gera um novo CNPJ válido e aleatório. Se `formatted` for `True`, retorna a string formatada; caso contrário, retorna uma instância da classe `CNPJ`. |
| `random_str(formatted: bool = False) -> str` | Gera um novo CNPJ válido e aleatório, retornando-o sempre como string (formatada ou não). |
| `format(value: str) -> str` | Formata um CNPJ fornecido como string. |

## Métodos Mágicos (`Dunder Methods`)

A classe implementa vários métodos mágicos para facilitar a interação:

| Método | Comportamento |
| :--- | :--- |
| `__str__` | Retorna o CNPJ formatado. |
| `__repr__` | Retorna uma representação de string que pode ser usada para recriar o objeto (ex: `CNPJ('12.345.678/0001-90')`). |
| `__eq__` | Permite a comparação de igualdade com outra instância `CNPJ` ou com uma string de CNPJ (limpa automaticamente). |
| `__len__` | Retorna o comprimento do valor do CNPJ (14 dígitos). |
| `__hash__` | Permite que instâncias de `CNPJ` sejam usadas como chaves em dicionários ou elementos em conjuntos. |

---
*Documentação gerada por **Manus AI***
