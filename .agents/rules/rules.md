---
trigger: always_on
---

# Regras Gerais

> Regras aplicáveis a todo o código e todos os agentes do projeto.

---

## Idioma

- Use preferencialmente o **Português do Brasil (pt-BR)**
- **Nomes de arquivos e diretórios**: Use o formato `camelCase` (ex: `userProfile.md`, `authService/`).
- **Mensagens de commit**: **Português do Brasil (pt-BR)**.

## Formato de Documentos

- Todo arquivo Markdown dentro de `.agents/` **deve** começar com YAML frontmatter contendo pelo menos o campo `description`.
- O `description` deve ser um resumo curto e objetivo do conteúdo do arquivo (uma linha).
- Isso permite que agentes identifiquem rapidamente a relevância do arquivo sem ler todo o conteúdo.

```yaml
---
description: Resumo curto do conteúdo do arquivo
---
```

## Convenções de Git

- **Mensagens de commit** seguem [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): descrição`
- **Escopo é obrigatório.** Não usar commits sem escopo.
- Tipos comuns: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `spec`.
- Use o tipo `spec` para alterações em artefatos SDD (ex: `spec(auth): define fluxo de login`).
- **Escopos válidos:** `frontend`, `backend`, `db`, `infra`, `docs`, `root`.
  Novos escopos podem ser adicionados conforme o projeto evoluir.
