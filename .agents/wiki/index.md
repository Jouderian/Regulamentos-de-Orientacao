---
description: Índice da base de conhecimento do projeto — decisões arquiteturais e páginas temáticas.
---

# Base de Conhecimento

Última atualização: 2026-10-31

Índice das páginas da wiki. As decisões formais ficam em `decisions/` como ADRs; specs, planos e workflows continuam sendo a fonte de verdade de cada iniciativa e não são duplicados aqui.

## Decisões Arquiteturais (ADRs)

| ADR | Assunto | Resumo |
| :--- | :--- | :--- |
| [ADR-001](decisions/ADR-001-markdown-como-fonte-da-verdade.md) | Markdown como fonte da verdade | O `.md` é o documento oficial; `.docx` e `.pdf` são saídas geradas |
| [ADR-002](decisions/ADR-002-unificacao-dos-regulamentos-cco-e-ccos.md) | Unificação CCO + CCOS | Documento único a partir da edição de 2026, com marcações de exclusividade |
| [ADR-003](decisions/ADR-003-historical-regulation-standardization.md) | Padronização do acervo histórico | MarkItDown como ferramenta primária e tipografia jurídica uniforme |
| [ADR-004](decisions/ADR-004-sugestoes-de-regra-por-issue.md) | Sugestões de regra por *issue* | Atleta sugere direto no GitHub, identificado por nome, número CBO e clube |
| [ADR-005](decisions/ADR-005-controle-de-pendencias-por-issues.md) | Controle de pendências por *issues* | *Issues* como único controle, com tipo e equipe por rótulo; sugestão fecha na deliberação e a aplicação vira `tarefa` |
| [ADR-006](decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md) | Edições por ano e arquivos congelados | Cada edição em `Documentos/<ano>/` desde a elaboração; PDF publicado congelado por manifesto de hashes |

## Páginas Temáticas

Nenhuma ainda. Criar conforme a orientação de [`wiki-maintenance.md`](../wiki-maintenance.md).

## Onde mais procurar

| Assunto | Local |
| :--- | :--- |
| Visão, atores e restrições do projeto | [`specs/project-vision/spec.md`](../specs/project-vision/spec.md) |
| Regras de idioma, nomenclatura e Git | [`rules/rules.md`](../rules/rules.md) |
| Como gerar `.docx` e `.pdf` | [`workflows/geracao-documentos.md`](../workflows/geracao-documentos.md) |
| Como importar um PDF novo | [`workflows/import-pdf.md`](../workflows/import-pdf.md) |
| Como abrir e publicar uma edição | [`workflows/publicar-edicao.md`](../workflows/publicar-edicao.md) |
| Como atualizar o repositório remoto | [`workflows/atualizar-repositorio.md`](../workflows/atualizar-repositorio.md) |
| Como abrir, conduzir e fechar *issues* | [`workflows/gestao-issues.md`](../workflows/gestao-issues.md) |
| Pendências atuais | [*Issues* do repositório](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues), conforme [`rules/rules.md`](../rules/rules.md) |
| Histórico de tarefas anterior a 2026-10-17 | [`todo-done.md`](../todo-done.md) (congelado) |
