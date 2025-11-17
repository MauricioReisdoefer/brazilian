# Documentação da Classe CRM

A classe `CRM` é uma implementação robusta para manipulação, validação, formatação e geração de números de Registro no Conselho Regional de Medicina (CRM) no Brasil. Ela encapsula a lógica de validação e oferece métodos utilitários para formatação, mascaramento e identificação do estado (UF) e região associados ao registro.

## Estrutura da Classe

A classe `CRM` é definida como um `dataclass` imutável (`frozen=True`), garantindo que o valor do CRM não seja alterado após a inicialização.

```python
@dataclass(frozen=True)
class CRM:
    _value: str
    # ...
```

### Inicialização

O construtor aceita um valor de CRM (que pode estar formatado ou não) e um parâmetro opcional `strict`.

| Parâmetro | Tipo | Descrição | Padrão |
| :--- | :--- | :--- | :--- |
| `value` | `str` ou `None` | O número do CRM a ser encapsulado. Será limpo para conter apenas caracteres alfanuméricos e convertido para maiúsculas. | `None` |
| `strict` | `bool` | Se `True`, a validação é executada na inicialização e um `InvalidCRMError` é levantado se o CRM for inválido. | `True` |

```python
def __init__(self, value=None, *, strict: bool = True):
    # ...
```

## Propriedades da Instância

| Propriedade | Tipo | Descrição |
| :--- | :--- | :--- |
| `value` | `str` | O valor do CRM limpo, contendo apenas números e a sigla do UF em maiúsculas (ex: "123456SP"). |
| `number` | `str` | A parte numérica do CRM. |
| `uf_acronym` | `str` ou `None` | A sigla do UF associada ao CRM (ex: "SP"). Retorna `None` se a sigla não for válida. |
| `uf` | `str` ou `None` | O nome completo do estado (UF) associado ao CRM (ex: "Sao Paulo"). Retorna `None` se a sigla não for válida. |
| `region` | `str` ou `None` | A região geográfica do Brasil associada ao UF (ex: "Sudeste"). Retorna `None` se a sigla não for válida. |
| `is_valid` | `bool` | Retorna `True` se o CRM for válido de acordo com as regras de validação. |
| `formatted` | `str` | O CRM formatado no padrão `[número]-[UF]` (ex: "123456-SP"). Retorna o valor limpo (`value`) se não for possível formatar. |
| `masked` | `str` | O CRM mascarado no padrão `***[últimos 3 dígitos]-[UF]` (ex: "***456-SP"). Retorna o valor limpo (`value`) se não for possível mascarar. |

## Métodos de Instância

| Método | Descrição |
| :--- | :--- |
| `self_validate(*, raise_error: bool = False) -> bool` | Valida a instância atual. Se `raise_error` for `True` e o CRM for inválido, levanta `InvalidCRMError`. |
| `self_format() -> str` | Retorna o CRM formatado (equivalente a `self.formatted`). |
| `self_mask() -> str` | Retorna o CRM mascarado (equivalente a `self.masked`). |
| `self_to_dict() -> dict` | Retorna um dicionário com as principais informações da instância: `value`, `formatted`, `masked`, `is_valid`, `uf` e `region`. |

## Métodos Estáticos (Utilitários)

| Método | Descrição |
| :--- | :--- |
| `clean(value: str) -> str` | Remove todos os caracteres não alfanuméricos de uma string e converte para maiúsculas, retornando o valor limpo. |
| `validate(value: str, raise_error: bool = False) -> bool` | Valida um CRM fornecido como string. Verifica se possui parte numérica (4 a 6 dígitos) e uma sigla de UF válida. Se `raise_error` for `True` e o CRM for inválido, levanta `InvalidCRMError`. |
| `generate(uf: str = None, formatted: bool = False) -> "CRM" ou "str"` | Gera um novo CRM válido e aleatório. Opcionalmente, pode-se especificar o UF. Se `formatted` for `True`, retorna a string formatada; caso contrário, retorna uma instância da classe `CRM`. |
| `random_str(formatted: bool = False) -> str` | Gera um novo CRM válido e aleatório, retornando-o sempre como string (formatada ou não). |
| `format(value: str) -> str` | Formata um CRM fornecido como string. |

## Regras de Validação

O método estático `CRM.validate(value)` aplica as seguintes regras:

1. **Limpeza:** O valor é limpo para conter apenas caracteres alfanuméricos e convertido para maiúsculas.
2. **Presença de Componentes:** Deve conter tanto uma parte numérica quanto uma parte de letras (UF).
3. **UF Válido:** A parte de letras deve ser uma sigla de UF válida presente na lista `UF_LIST`.
4. **Tamanho do Número:** A parte numérica deve ter entre 4 e 6 dígitos (inclusive).

## Mapeamento de UF e Região

A classe utiliza os seguintes mapeamentos para identificar o estado e a região geográfica:

| Sigla | Estado | Região |
| :--- | :--- | :--- |
| AC | Acre | Norte |
| AL | Alagoas | Nordeste |
| AP | Amapá | Norte |
| AM | Amazonas | Norte |
| BA | Bahia | Nordeste |
| CE | Ceará | Nordeste |
| DF | Distrito Federal | Centro-Oeste |
| ES | Espírito Santo | Sudeste |
| GO | Goiás | Centro-Oeste |
| MA | Maranhão | Nordeste |
| MT | Mato Grosso | Centro-Oeste |
| MS | Mato Grosso do Sul | Centro-Oeste |
| MG | Minas Gerais | Sudeste |
| PA | Pará | Norte |
| PB | Paraíba | Nordeste |
| PR | Paraná | Sul |
| PE | Pernambuco | Nordeste |
| PI | Piauí | Nordeste |
| RJ | Rio de Janeiro | Sudeste |
| RN | Rio Grande do Norte | Nordeste |
| RS | Rio Grande do Sul | Sul |
| RO | Rondônia | Norte |
| RR | Roraima | Norte |
| SC | Santa Catarina | Sul |
| SP | São Paulo | Sudeste |
| SE | Sergipe | Nordeste |
| TO | Tocantins | Norte |

## Métodos Mágicos (`Dunder Methods`)

A classe implementa vários métodos mágicos para facilitar a interação:

| Método | Comportamento |
| :--- | :--- |
| `__str__` | Retorna o CRM formatado (ou o valor limpo se a formatação falhar). |
| `__repr__` | Retorna uma representação de string que pode ser usada para recriar o objeto (ex: `CRM('123456-SP')`). |
| `__eq__` | Permite a comparação de igualdade com outra instância `CRM` ou com uma string de CRM (limpa automaticamente). |
| `__len__` | Retorna o comprimento do valor limpo do CRM. |
| `__hash__` | Permite que instâncias de `CRM` sejam usadas como chaves em dicionários ou elementos em conjuntos. |
