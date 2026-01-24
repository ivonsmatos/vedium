# Contribuindo para o Vedium

## Fluxo de Trabalho Git

Utilizamos um fluxo de trabalho baseado em branches de funcionalidade (feature-branch). Por favor, siga estas convenções:

### Nomenclatura de Branches

- **Funcionalidades (Features)**: `feat/descricao-da-funcionalidade` (ex.: `feat/integracao-stripe`)
- **Correções (Fixes)**: `fix/descricao-do-bug` (ex.: `fix/erro-login`)
- **Documentação**: `docs/atualizar-api-docs`
- **Manutenção (Chore)**: `chore/atualizar-dependencias`

### Pull Requests

1. **Título**: Use mensagens de commit semânticas (ex.: `feat: adicionar integração stripe`).
2. **Descrição**: Descrição detalhada das mudanças.
3. **Requisitos**:
    - Todas as verificações de CI devem passar (Lint, Testes, Segurança).
    - Pelo menos uma aprovação de code review.
    - Sem conflitos de merge com a `main`.

### Estilo de Código

- **Python**: Siga PEP 8. Forçamos o uso do `flake8` no CI.
- **JavaScript/CSS**: Siga os padrões do projeto (Tailwind para CSS).

## Configuração de Desenvolvimento

Veja o `README.md` para começar localmente.
