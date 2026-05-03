---
trigger: always_on
---

# Regras Gerais

> Regras aplicáveis a todo o código e todos os agentes do projeto.

---

## Idioma e Nomenclatura

- **Conteúdo do Projeto** (documentos, regulamentos, manuais): **Português do Brasil (pt-BR)**.
- **Nomes de arquivos e diretórios de projeto**: Use o formato **camelCase** (ex: `regulamentoCompeticoes.md`, `listaPresenca.md`).
- **Arquivos Sistêmicos** (dentro de `.agents/`): Mantêm o padrão **Inglês** e **kebab-case** (ex: `spec.md`, `project-vision/`) para garantir a compatibilidade com o sistema.
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
- **Autorização para Push:** É **obrigatório** solicitar a autorização expressa do usuário antes de realizar qualquer envio para o repositório remoto (`git push`).
- **Regeneração de Documentos Finais:** Sempre que o arquivo `regulamentoCompeticoesCearenses.md` tiver sido modificado, é **obrigatório** regenerar os documentos finais (`.docx` e `.pdf`) **antes** do commit/push. Siga o workflow `.agents/workflows/atualizar-repositorio.md` para o procedimento completo.
- **Pré-requisito do Commit/Push:** Antes de solicitar a autorização para atualizar o repositório, você deve apresentar claramente ao usuário:
  1. A lista exata dos arquivos que foram modificados e estão sendo incluídos na atualização.
  2. A exata mensagem de *commit* que será utilizada.
