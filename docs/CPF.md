# Documentação da Classe CPF

A classe `CPF` é uma implementação robusta para manipulação, validação, formatação e geração de números de Cadastro de Pessoas Físicas (CPF) no Brasil. Ela encapsula a lógica de validação de acordo com as regras oficiais e oferece métodos utilitários para formatação, mascaramento e identificação da região de emissão.

## Estrutura da Classe

A classe `CPF` é definida como um `dataclass` imutável (`frozen=True`), garantindo que o valor do CPF não seja alterado após a inicialização.

```python
@dataclass(frozen=True)
class CPF:
    _value: str
    # ...
```

### Inicialização

O construtor aceita um valor de CPF (que pode estar formatado ou não) e um parâmetro opcional `strict`.

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `value` | `str` ou `None` | O número do CPF a ser encapsulado. Será limpo para conter apenas dígitos. | `None` |
| `strict` | `bool` | Se `True`, a validação é executada na inicialização e um `InvalidCPFError` é levantado se o CPF for inválido. | `True` |

```python
def __init__(self, value=None, *, strict: bool = True):
    # ...
```

## Propriedades da Instância

| Propriedade | Tipo | Descrição |
| :--- | :--- | :--- |
| `value` | `str` | O valor do CPF contendo apenas os 11 dígitos. |
| `digits` | `tuple` | Uma tupla de inteiros representando cada dígito do CPF. |
| `is_valid` | `bool` | Retorna `True` se o CPF for válido de acordo com as regras de cálculo. |
| `formatted` | `str` | O CPF formatado no padrão `XXX.XXX.XXX-XX`. Retorna o valor original se não tiver 11 dígitos. |
| `masked` | `str` | O CPF mascarado no padrão `***.***.***-XX`, exibindo apenas os dois dígitos verificadores. Retorna o valor original se não tiver 11 dígitos. |
| `region` | `str` ou `None` | O nome da região/estado de emissão (ex: 'Sao Paulo'). Baseado no 9º dígito. Retorna `None` se o CPF for incompleto. |
| `region_acronym` | `str` ou `None` | A sigla da região/estado de emissão (ex: 'SP'). Baseado no 9º dígito. Retorna `None` se o CPF for incompleto. |

## Métodos de Instância

| Método | Descrição |
| :--- | :--- |
| `self_validate(*, raise_error: bool = False) -> bool` | Valida a instância atual. Se `raise_error` for `True` e o CPF for inválido, levanta `InvalidCPFError`. |
| `self_format() -> str` | Retorna o CPF formatado (equivalente a `self.formatted`). |
| `self_mask() -> str` | Retorna o CPF mascarado (equivalente a `self.masked`). |
| `self_to_dict() -> dict` | Retorna um dicionário com as principais informações da instância: `value`, `formatted`, `masked`, `is_valid` e `region`. |

## Métodos Estáticos (Utilitários)

| Método | Descrição |
| :--- | :--- |
| `clean(value: str) -> str` | Remove todos os caracteres não numéricos de uma string, retornando apenas os dígitos. |
| `validate(value: str, raise_error: bool = False) -> bool` | Valida um CPF fornecido como string. Se `raise_error` for `True` e o CPF for inválido, levanta `InvalidCPFError`. |
| `generate(formatted: bool = False) -> "CPF" ou "str"` | Gera um novo CPF válido e aleatório. Se `formatted` for `True`, retorna a string formatada; caso contrário, retorna uma instância da classe `CPF`. |
| `random_str(formatted: bool = False) -> str` | Gera um novo CPF válido e aleatório, retornando-o sempre como string (formatada ou não). |
| `format(value: str) -> str` | Formata um CPF fornecido como string. |

## Regiões de Emissão

A classe utiliza o 9º dígito do CPF para determinar a região de emissão, conforme a tabela a seguir:

| 9º Dígito | Região | Sigla(s) |
| :--- | :--- | :--- |
| **0** | Rio Grande do Sul | RS |
| **1** | Distrito Federal, Goias, Mato Grosso, Mato Grosso do Sul, Tocantins | DF, GO, MT, MS, TO |
| **2** | Para, Amazonas, Acre, Amapa, Rondonia, Roraima | PA, AM, AC, AP, RO, RR |
| **3** | Ceara, Maranhao, Piaui | CE, MA, PI |
| **4** | Pernambuco, Rio Grande do Norte, Paraiba, Alagoas | PE, RN, PB, AL |
| **5** | Bahia, Sergipe | BA, SE |
| **6** | Minas Gerais | MG |
| **7** | Rio de Janeiro, Espirito Santo | RJ, ES |
| **8** | Sao Paulo | SP |
| **9** | Parana, Santa Catarina | PR, SC |

## Métodos Mágicos (`Dunder Methods`)

A classe implementa vários métodos mágicos para facilitar a interação:

| Método | Comportamento |
| :--- | :--- |
| `__str__` | Retorna o CPF formatado. |
| `__repr__` | Retorna uma representação de string que pode ser usada para recriar o objeto (ex: `CPF('123.456.789-00')`). |
| `__eq__` | Permite a comparação de igualdade com outra instância `CPF` ou com uma string de CPF (limpa automaticamente). |
| `__len__` | Retorna o comprimento do valor do CPF (11 dígitos). |
| `__hash__` | Permite que instâncias de `CPF` sejam usadas como chaves em dicionários ou elementos em conjuntos. |
