# Brazilian: Validação e Geração de Dados Brasileiros

**Brazilian** é uma biblioteca robusta para a manipulação, validação e geração de dados comuns no Brasil, como CPF, CRM, CNPJ e outros. Diferente de geradores simples, esta biblioteca oferece classes ricas em funcionalidades, permitindo formatação, mascaramento e extração de informações contextuais (como região de emissão).

## Instalação

Hoje, a versão mais recente é 0.3.0, e não depende de biblotecas externas.

```bash
pip install brazilian
```

## Uso Rápido

### 1. Classe CPF

A classe `CPF` permite validar, formatar e gerar números de Cadastro de Pessoas Físicas.

```python
from brazilian.documents import CPF

cpf = CPF("12345678900")

print(f"Valor limpo: {cpf.value}")        # Saída: 12345678900
print(f"Formatado: {cpf.formatted}")      # Saída: 123.456.789-00
print(f"Mascarado: {cpf.masked}")        # Saída: ***.***.***-00
print(f"É válido? {cpf.is_valid}")       # Saída: True/False
print(f"Região de emissão: {cpf.region}") # Saída: Sao Paulo

# Geração de CPF válido
novo_cpf = CPF.generate()
print(f"Novo CPF gerado: {novo_cpf.formatted}")
```

### 2. Classe CRM

A classe `CRM` permite validar, formatar e gerar números de Registro no Conselho Regional de Medicina.

```python
from brazilian.documents import CRM

# Validação e Formatação
crm = CRM("123456SP")

print(f"Valor limpo: {crm.value}")        # Saída: 123456SP
print(f"Formatado: {crm.formatted}")      # Saída: 123456-SP
print(f"Mascarado: {crm.masked}")        # Saída: ***456-SP
print(f"É válido? {crm.is_valid}")       # Saída: True/False
print(f"Estado (UF): {crm.uf}")          # Saída: Sao Paulo
print(f"Região: {crm.region}")           # Saída: Sudeste

# Geração de CRM válido para um UF específico
novo_crm = CRM.generate(uf="RJ")
print(f"Novo CRM gerado (RJ): {novo_crm.formatted}")
```

## Principais Funcionalidades

* **Validação Robusta:** Implementa a lógica de validação oficial para garantir a integridade dos dados.
* **Formatação Flexível:** Oferece métodos para formatar e mascarar os documentos (ex: `XXX.XXX.XXX-XX` ou `***.***.***-XX`).
* **Geração de Dados:** Métodos estáticos para gerar números válidos e aleatórios.
* **Informação Contextual:** Extração de dados como a região de emissão (CPF) ou o estado/região (CRM).

## Documentação Completa

Para detalhes sobre todas as propriedades e métodos disponíveis, consulte a [Documentação Completa](/docs).

---

[![PyPI version](https://badge.fury.io/py/brazilian.svg)](https://pypi.org/project/brazilian/)
