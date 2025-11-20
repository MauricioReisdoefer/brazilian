# Guia de Contribuição para a Biblioteca `brazilian`

Agradecemos o seu interesse em contribuir para a biblioteca `brazilian`! Seu apoio é fundamental para o crescimento e a melhoria contínua deste projeto.

Este guia descreve o processo e as melhores práticas para contribuir.

## 1. Código de Conduta

Ao participar deste projeto, você concorda em seguir nosso [Código de Conduta](CODE_OF_CONDUCT.md) (se ainda não existir, considere criá-lo). Esperamos que todos os colaboradores sigam as regras de convivência e demonstrem respeito mútuo.

## 2. Como Contribuir

Existem várias maneiras de contribuir, mesmo que você não seja um desenvolvedor:

### 2.1. Relatar Bugs

Se você encontrar um erro ou comportamento inesperado:

1. Verifique se o bug já foi relatado na seção [Issues do GitHub](https://github.com/MauricioReisdoefer/brazilian/issues).
2. Se não foi, abra uma nova *Issue*.
3. Inclua o máximo de detalhes possível:
    * Versão da biblioteca `brazilian` e do Python que você está usando.
    * Passos para reproduzir o erro.
    * O comportamento esperado e o comportamento real.
    * Qualquer mensagem de erro ou *traceback* relevante.

### 2.2. Sugerir Melhorias

Se você tiver uma ideia para uma nova funcionalidade, melhoria de desempenho ou adição de um novo documento brasileiro:

1. Abra uma *Issue* na seção [Issues do GitHub](https://github.com/MauricioReisdoefer/brazilian/issues).
2. Descreva a funcionalidade, o caso de uso e por que ela seria valiosa para a biblioteca.

### 2.3. Contribuição de Código (Pull Requests)

Para enviar alterações de código, siga estes passos:

1. **Faça um Fork** do repositório para sua conta pessoal.
2. **Clone** o repositório forkeado para sua máquina local.

    ```bash
    git clone https://github.com/SEU_USUARIO/brazilian.git
    cd brazilian
    ```

3.**Crie um Ambiente Virtual** e instale as dependências de desenvolvimento.
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Linux/macOS
    # venv\Scripts\activate   # No Windows
    pip install -r requirements-dev.txt # Assumindo que existe um arquivo de dependências de desenvolvimento
    ```
4.  **Crie um Branch** para sua contribuição.
    ```bash
    git checkout -b feature/nome-da-sua-feature
    # ou
    git checkout -b fix/correcao-do-bug
    ```
5.  **Implemente** suas alterações.
6.  **Escreva Testes** para cobrir seu novo código ou a correção do bug.
7.  **Execute os Testes** para garantir que nada foi quebrado.
    ```bash
    # Comando para rodar os testes (exemplo)
    pytest
    ```
8.  **Faça o Commit** das suas alterações (veja a seção 3 para o formato de mensagem).
9.  **Envie** o branch para o seu *fork* no GitHub.
    ```bash
    git push origin nome-da-sua-feature
    ```
10. **Abra um Pull Request (PR)** do seu *branch* para o *branch* `main` do repositório original.

## 3. Formato das Mensagens de Commit

Para manter o histórico do projeto limpo e legível, pedimos que você siga um formato simples para as mensagens de *commit*:

```bash
<tipo>: <descrição concisa>
```

**Tipos Comuns:**

* `feat`: Uma nova funcionalidade.
* `fix`: Uma correção de bug.
* `docs`: Alterações na documentação.
* `style`: Alterações que não afetam o significado do código (espaços em branco, formatação, ponto e vírgula ausente, etc.).
* `refactor`: Uma mudança de código que não corrige um bug nem adiciona uma funcionalidade.
* `test`: Adição ou correção de testes.
* `chore`: Outras alterações que não modificam o código-fonte ou os testes (ex: atualização de dependências).

Obrigado novamente por dedicar seu tempo para contribuir!
