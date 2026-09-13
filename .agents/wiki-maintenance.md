---
description: Quando e como atualizar a base de conhecimento (wiki) e registrar decisões (ADRs) do projeto.
---

# Manutenção da Base de Conhecimento (Wiki)

## Quando atualizar
Ao final de qualquer sessão que envolva:

- Decisão sobre **estrutura normativa** — unificar ou separar regulamentos, mudar a hierarquia de Capítulos/Artigos, alterar a tipografia jurídica do projeto.
- Decisão sobre **ferramenta ou processo** — trocar o conversor de PDF, mudar o fluxo de geração do `.docx`/`.pdf`, alterar o que o CI verifica.
- Decisão sobre **organização do acervo** — convenção de nomes, política de arquivamento em `Documentos/<ano>/`, o que entra e o que não entra no repositório.
- **Interpretação normativa não óbvia** que precisou ser investigada e que reaparecerá — por exemplo, como uma regra estadual se concilia com a ROP nacional, ou por que determinada edição não tem regulamento.
- Mudança em **licenciamento, autoria ou distribuição** dos documentos.
- Resolução de um problema que exigiu investigação e que provavelmente voltará a acontecer.

Correção de redação, atualização de calendário, troca de árbitro e conversão de mais um ano do acervo **não** geram página de wiki — o `git log` e as specs já registram isso.

## Como atualizar
1. Leia [`wiki/index.md`](wiki/index.md) para ver o que já existe.
2. Atualize as páginas afetadas ou crie novas, se o tópico ainda não existir.
3. Atualize o `index.md` quando criar uma página ou uma ADR.
4. Faça commit da wiki junto com a alteração que a motivou, no escopo `agents`.

## Decisões formais (ADRs)
Decisões arquiteturais vão para `wiki/decisions/` como ADRs, não para páginas temáticas.

- Nome do arquivo: `ADR-<NNN>-<assunto-em-kebab-case>.md`, numeração sequencial.
- Seções: **Contexto**, **Decisão**, **Consequências** (positivas e negativas/atenção). Use **Problemas** quando o contexto tiver obstáculos técnicos específicos.
- Uma ADR registra a decisão **e o que se abriu mão ao tomá-la**. Uma ADR sem consequências negativas provavelmente não descreve uma decisão real.
- ADR não se reescreve quando a realidade muda: acrescente uma seção `## Revisão de AAAA-MM-DD` ou registre uma nova ADR que a supere.

## Formato das páginas
- Markdown com referências cruzadas por **links relativos** — caminhos absolutos são recusados pela verificação documental.
- Cabeçalho YAML com `description`, conforme [`rules/rules.md`](rules/rules.md).
- Linha `Última atualização: AAAA-MM-DD` nas páginas temáticas e no índice.
- Sintetize, não copie: specs, planos e ADRs continuam sendo a fonte de verdade.

## O que NÃO deve ir na wiki
- Conteúdo normativo — ele vive nos regulamentos, não aqui.
- Cópia literal de specs, planos ou ADRs.
- Informação temporária ou específica de uma sessão de trabalho.
- Tarefas pendentes — vão para [`todo.md`](todo.md).
