# Documentação da Classe CEP

A classe `CEP` é uma implementação robusta para manipulação, validação, formatação, geração e consulta de endereços a partir de números de Código de Endereçamento Postal (CEP) no Brasil. Ela encapsula a lógica de validação, incluindo a verificação do prefixo regional, e oferece métodos utilitários para formatação, mascaramento e consulta de localização via ViaCEP.

## Estrutura da Classe

A classe `CEP` é definida como um `dataclass` imutável (`frozen=True`), garantindo que o valor do CEP não seja alterado após a inicialização.

```python
@dataclass(frozen=True)
class CEP:
    _value: str
    # ...
```

### Inicialização

O construtor aceita um valor de CEP (que pode estar formatado ou não) e um parâmetro opcional `strict`.

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `value` | `str` ou `None` | O número do CEP a ser encapsulado. Será limpo para conter apenas dígitos. | `None` |
| `strict` | `bool` | Se `True`, a validação é executada na inicialização e um `InvalidCEPError` é levantado se o CEP for inválido (tamanho incorreto ou prefixo desconhecido). | `True` |

```python
def __init__(self, value=None, *, strict: bool = True):
    # ...
```

## Propriedades da Instância

| Propriedade | Tipo | Descrição |
| :--- | :--- | :--- |
| `value` | `str` | O valor do CEP contendo apenas os 8 dígitos. |
| `digits` | `tuple` | Uma tupla de inteiros representando cada dígito do CEP. |
| `is_valid` | `bool` | Retorna `True` se o CEP for válido (8 dígitos e prefixo regional conhecido). |
| `formatted` | `str` | O CEP formatado no padrão `XXXXX-XXX`. Retorna o valor original se não tiver 8 dígitos. |
| `masked` | `str` | O CEP mascarado no padrão `*****-XXX`, exibindo apenas os três dígitos finais. Retorna o valor original se não tiver 8 dígitos. |
| `region` | `str` | A sigla da Unidade Federativa (UF) correspondente ao prefixo do CEP (ex: 'SP'). Retorna uma string vazia se o CEP for inválido ou o prefixo for desconhecido. |
| `region_acronym` | `str` | Alias para o mesmo resultado da propriedade `region`. |

## Métodos de Instância

| Método | Descrição |
| :--- | :--- |
| `self_validate(*, raise_error: bool = False) -> bool` | Valida a instância atual. Se `raise_error` for `True` e o CEP for inválido, levanta `InvalidCEPError`. |
| `self_format() -> str` | Retorna o CEP formatado (equivalente a `self.formatted`). |
| `self_mask() -> str` | Retorna o CEP mascarado (equivalente a `self.masked`). |
| `self_to_dict() -> dict` | Retorna um dicionário com as principais informações da instância: `value`, `formatted`, `masked`, `is_valid` e `region`. |
| `self_get_location() -> dict` | Consulta a API do ViaCEP para obter os dados de endereço completos (logradouro, bairro, cidade, UF, etc.) para o CEP da instância. Levanta uma exceção em caso de erro na requisição. |

## Métodos Estáticos (Utilitários)

| Método | Descrição |
| :--- | :--- |
| `clean(value: str) -> str` | Remove todos os caracteres não numéricos de uma string, retornando apenas os dígitos. |
| `validate(value: str, raise_error: bool = False) -> bool` | Valida um CEP fornecido como string. Verifica se possui 8 dígitos e se o prefixo regional é conhecido. Se `raise_error` for `True` e o CEP for inválido, levanta `InvalidCEPError`. |
| `generate(formatted: bool = False) -> "CEP" ou "str"` | Gera um novo CEP válido e aleatório, escolhendo um prefixo de uma região conhecida. Se `formatted` for `True`, retorna a string formatada; caso contrário, retorna uma instância da classe `CEP`. |
| `random_str(formatted: bool = False) -> str` | Gera um novo CEP válido e aleatório, retornando-o sempre como string (formatada ou não). |
| `format(value: str) -> str` | Formata um CEP fornecido como string. |
| `uf_from_cep(cep: str) -> str ou None` | Retorna a sigla da UF (Unidade Federativa) correspondente ao prefixo do CEP. Retorna `None` se o prefixo for desconhecido ou o CEP for incompleto. |
| `get_location(cep: "CEP") -> dict` | Consulta a API do ViaCEP para obter os dados de endereço completos para o CEP fornecido. Levanta uma exceção em caso de erro na requisição. |

## Regiões de Endereçamento

A classe utiliza o prefixo do CEP (os 5 primeiros dígitos) para determinar a Unidade Federativa (UF) de endereçamento, conforme o mapeamento interno `PREFIX_MAP`.

| Prefixo (Primeiros 5 Dígitos) | UF |
| :--- | :--- |
| `00000` a `19999` | SP |
| `20000` a `29999` | RJ, ES |
| `30000` a `39999` | MG |
| `40000` a `49999` | BA, SE |
| `50000` a `59999` | PE, PB, RN, AL |
| `60000` a `65999` | CE, PI, MA |
| `66000` a `69999` | PA, AM, AC, AP, RO, RR |
| `70000` a `77999` | DF, GO, MT, MS, TO |
| `78000` a `79999` | MS |
| `80000` a `89999` | PR, SC |
| `90000` a `99999` | RS |

*Nota: O mapeamento interno é mais granular e pode cobrir faixas específicas dentro desses grandes blocos.*

## Métodos Mágicos (`Dunder Methods`)

A classe implementa vários métodos mágicos para facilitar a interação:

| Método | Comportamento |
| :--- | :--- |
| `__str__` | Retorna o CEP formatado. |
| `__repr__` | Retorna uma representação de string que pode ser usada para recriar o objeto (ex: `CEP('12345-678')`). |
| `__eq__` | Permite a comparação de igualdade com outra instância `CEP` ou com uma string de CEP (limpa automaticamente). |
| `__len__` | Retorna o comprimento do valor do CEP (8 dígitos). |
| `__hash__` | Permite que instâncias de `CEP` sejam usadas como chaves em dicionários ou elementos em conjuntos. |
