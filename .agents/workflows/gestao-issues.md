---
description: Passo a passo para abrir, conduzir e fechar issues — formulários, ciclo da sugestão de regra, dependências, milestone e comentário de fechamento.
---

# Workflow: Gestão de *Issues*

As regras ficam em *Controle de Pendências e Sugestões de Regra*, de [`rules.md`](../rules/rules.md); este workflow só detalha como cumpri-las e não acrescenta obrigação. A decisão está na [ADR-005](../wiki/decisions/ADR-005-controle-de-pendencias-por-issues.md).

## 1. Abrir

| Tipo | Formulário | Rótulos que o formulário aplica |
| :--- | :--- | :--- |
| `sugestão de regra` | [`sugestao-regra.yml`](../../.github/ISSUE_TEMPLATE/sugestao-regra.yml) | `sugestão de regra`, `equipe: regras` |
| `tarefa` da equipe de regras | [`tarefa-regras.yml`](../../.github/ISSUE_TEMPLATE/tarefa-regras.yml) | `tarefa`, `equipe: regras` |
| `tarefa` da equipe do repositório | [`tarefa-repositorio.yml`](../../.github/ISSUE_TEMPLATE/tarefa-repositorio.yml) | `tarefa`, `equipe: repositório` |
| `acompanhamento` | [`acompanhamento.yml`](../../.github/ISSUE_TEMPLATE/acompanhamento.yml) | `acompanhamento`, `equipe: regras` |

- Pela linha de comando, os rótulos são informados à mão: `gh issue create --title "..." --body-file <arquivo> --label "tarefa" --label "equipe: repositório"`.
- Sugestão e tarefa da edição em elaboração entram no *milestone* "Regulamento `<ano>`" (`--milestone "Regulamento <ano>"`).
- O texto redigido pelo agente é apresentado ao usuário antes de a *issue* ser aberta.

## 2. Ciclo da Sugestão de Regra

A sugestão aberta significa **decisão pendente**; a regra aprovada e ainda não aplicada vive em uma `tarefa`.

1. **Triagem** (sem rótulo de situação): confere a identificação do proponente e se a sugestão é clara.
2. `situação: em análise`: a equipe de regras elabora o parecer, em comentário, com a redação proposta, o impacto e eventual conflito com a ROP ou com outro artigo.
3. `situação: parecer pronto`: o parecer está registrado e a sugestão espera entrar na pauta.
4. `situação: na pauta`: aguarda a deliberação da comissão de regras. Só entra na pauta sugestão com parecer.
5. **Deliberada**: a *issue* fecha com o resumo da seção 4.
   - **Aprovada:** abre-se uma `tarefa` (`equipe: regras`) com a redação final aprovada, ligada à sugestão pelo número (`Refs #N`). A tarefa fecha quando o texto entra no regulamento em elaboração.
   - **Rejeitada:** fecha com a justificativa.
   - **Adiada:** continua aberta, com a data de retorno em comentário.

O rótulo de situação é **trocado**, nunca acumulado, e só com autorização do usuário:

```bash
gh issue edit <N> --remove-label "situação: em análise" --add-label "situação: parecer pronto"
```

Ao fechar, a sugestão mantém o último rótulo de situação; o estado final fica no comentário de fechamento.

## 3. Dependências

A *issue* que aguarda outra recebe o vínculo nativo "Bloqueada por", pela interface da *issue* ou pela API, e explica o motivo no corpo, em uma seção "Bloqueada porque". Não há rótulo de bloqueio.

```bash
# id interno (não o número) da issue que bloqueia
gh api repos/Jouderian/Regulamentos-de-Orientacao/issues/<bloqueadora> --jq .id
gh api -X POST repos/Jouderian/Regulamentos-de-Orientacao/issues/<bloqueada>/dependencies/blocked_by -F issue_id=<id>
```

O vínculo não aparece no `gh issue list`; consulte-o com `gh issue view <N> --json blockedBy,blocking`.

## 4. Fechar

Quem fecha deixa um comentário com:

- **Resumo:** o que foi feito, em até 3 linhas.
- **Mudanças:** arquivos alterados ou decisão tomada.
- **Referência:** hash do commit ou número do PR.
- **Fica de fora:** o que não foi feito e em qual *issue* está registrado, ou "nada".

Na `sugestão de regra`, o resumo traz o resultado da deliberação e a redação final aprovada, ou a justificativa da rejeição. No `acompanhamento`, traz a decisão do terceiro e o que ela gerou (por exemplo, a `tarefa` aberta). Se o fechamento vem de `Closes #N` em PR ou commit, o comentário é postado no mesmo momento, porque o fechamento automático não registra o que foi feito.

O *milestone* "Regulamento `<ano>`" só fecha quando todas as suas *issues* estiverem fechadas, e só com autorização do usuário.

## 5. Consultar

- Pela web: *issues* abertas da [equipe de regras](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues?q=is%3Aissue+is%3Aopen+label%3A%22equipe%3A+regras%22) e da [equipe do repositório](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues?q=is%3Aissue+is%3Aopen+label%3A%22equipe%3A+reposit%C3%B3rio%22).
- Pela linha de comando: `gh issue list --label "equipe: regras"`, `gh issue list --milestone "Regulamento <ano>"`.
- `acompanhamento` pode ficar aberto por meses: filtre por tipo para enxergar o que é trabalho da equipe.
