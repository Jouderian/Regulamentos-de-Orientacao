---
description: Decisão de controlar as pendências por issues do GitHub, com tipo e equipe identificados por rótulo, em vez de um arquivo todo.md.
---

# ADR 005: Controle de Pendências por *Issues*

> Registrada em 2026-10-17.

## Contexto
O backlog vivia em um único arquivo, `todo.md`. Numa só revisão do repositório ele passou de 3 para 15 itens longos, sem identificador: não havia como se referir a uma pendência pelo nome curto, e duas pessoas editando o arquivo ao mesmo tempo gerariam conflito de *merge*.

O contexto de trabalho também mudou:
- Há duas equipes — uma só de **regras** e outra de **manutenção do repositório** — e é preciso saber de relance de quem é cada pendência.
- O repositório é mantido com agentes de mais de uma ferramenta (hoje o Claude Code e o Antigravity) e terá membros futuros cujas ferramentas não conhecemos.
- Parte do que estava no backlog não era tarefa, e sim controle de algo que só um terceiro decide: a ROP só pode ser alterada pela CBO, e a nós cabe sugerir e acompanhar.
- O requisito declarado é um **único controle**: a mesma pendência não pode existir em dois lugares.

A [ADR-004](ADR-004-sugestoes-de-regra-por-issue.md) já adotou *issues* para as sugestões de regra e deixou em aberto um modelo próprio para o que não é sugestão.

## Decisão
1. As *issues* do GitHub são o **único** controle de pendências. O `todo.md` é removido e o `todo-done.md` fica congelado como histórico anterior a esta decisão.
2. Há **três tipos**, cada um com formulário e rótulo próprios:
   - `sugestão de regra`: proposta de mudança em dispositivo do regulamento (formulário já existente).
   - `tarefa`: trabalho que a própria equipe executa e fecha.
   - `acompanhamento`: item que depende de terceiro, como a CBO, e só se fecha quando ele decidir. Sugestão à CBO e espera por nova edição da ROP são sempre `acompanhamento`.
3. Há **duas equipes**, identificadas por rótulo: `equipe: regras` e `equipe: repositório`. Toda *issue* tem um rótulo de tipo e um de equipe, aplicados pelo formulário. A equipe é a que **executa**.
4. A dependência entre *issues* é registrada pelo vínculo nativo "Bloqueada por" do GitHub, que aparece nos dois lados, e o corpo da *issue* que aguarda explica o motivo em "Bloqueada porque". Não há rótulo de bloqueio: o vínculo é a única fonte.
5. Texto normativo (regulamento, ROP, `Documentos/**/*.md`, `clubesCampeoes.md`) só é alterado com revisão da equipe de regras, seja qual for a equipe da *issue*.
6. As regras de uso ficam **somente** em [`rules.md`](../../rules/rules.md), em Markdown comum e sem pressupor um cliente específico: o backlog se consulta pela web ou por qualquer cliente do GitHub. A pessoa que dirige o agente se atribui à *issue* antes de começar, e o agente não abre nem fecha *issue* sem autorização.

## Consequências
- **Positivas:**
  * Cada pendência tem identificador único e estável (`#N`), citável em commit e em PR.
  * A equipe e o tipo aparecem como rótulo colorido e viram filtro, sem abrir a *issue*.
  * Responsável, estado e discussão ficam na própria pendência, e duas pessoas não disputam o mesmo arquivo.
  * O `acompanhamento` separa o que depende de terceiro do que é nossa tarefa, e o backlog deixa de acusar como atrasado o que só a CBO pode resolver.
  * Preenche a lacuna deixada pela [ADR-004](ADR-004-sugestoes-de-regra-por-issue.md): relatos que não são sugestão de regra passam a ter formulário.
- **Negativas/Atenção:**
  * O backlog passa a depender do GitHub (rede e conta). O `todo.md` se lia offline; agente ou pessoa sem acesso precisa pedir o texto da *issue*.
  * *Issues* são públicas: tarefa e acompanhamento não podem conter dado pessoal.
  * Os rótulos precisam existir **antes** dos formulários: o GitHub não aplica rótulo inexistente.
  * O vínculo "Bloqueada por" não é criado pelo formulário e não aparece no `gh issue list`: só na interface web e na API. Quem abre uma *issue* com dependência cria o vínculo depois.
  * O repositório pertence a uma conta pessoal, sem *Teams* do GitHub. Os rótulos identificam a equipe, mas **não restringem** quem pode atuar nem substituem permissão por equipe.
  * A revisão cruzada do texto normativo depende de disciplina até existir um `CODEOWNERS` por caminho, que exigirá o usuário do GitHub de cada pessoa.
  * Item na fronteira entre as equipes (como a conversão do acervo, executada pelo repositório e revisada pelas regras) fica com a equipe que executa; a outra entra como revisora do PR.
  * `acompanhamento` pode ficar aberto por meses e polui a lista de abertas; deve-se filtrar por tipo.

## Revisão de 2026-10-17
Passou a ser regra que todo fechamento de *issue* leve um comentário-resumo (resumo, mudanças, referência e o que ficou de fora), para que o histórico seja legível sem abrir o PR que a fechou. O custo é redigir o resumo a cada fechamento, e a regra depende de disciplina: `Closes #N` fecha a *issue* sem registrar o que foi feito, então o comentário precisa ser postado junto. Os detalhes estão em [`rules.md`](../../rules/rules.md).
