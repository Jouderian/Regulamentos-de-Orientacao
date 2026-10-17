---
description: Decisão de aceitar sugestões de regra de atletas diretamente por issue no GitHub, com identificação obrigatória do proponente.
---

# ADR 004: Sugestões de Regra por *Issue* no GitHub

> Registrada em 2026-10-11.

## Contexto
O fluxo de atualização das regras previa um único caminho para a sugestão de um atleta: ele a levava ao diretor técnico do seu clube, que a encaminhava ao diretor técnico da federação. A sugestão chegava em formato livre — conversa, mensagem ou e-mail —, e a deliberação precisava primeiro reconstruir qual dispositivo seria alterado e com qual redação.

Além disso, uma sugestão que dependia do clube para chegar à federação podia ficar retida no caminho, sem registro de que tinha existido.

## Decisão
As sugestões de regra passam a ter um segundo canal, além do clube: a *issue* no repositório, aberta pelo formulário [`sugestao-regra.yml`](../../../.github/ISSUE_TEMPLATE/sugestao-regra.yml).

1. O atleta pode abrir a *issue* diretamente, sem passar pelo diretor técnico do clube. O canal pelo clube continua valendo.
2. O formulário exige a identificação do proponente — **nome completo**, **número CBO** e **clube** — e os campos usados na deliberação: artigo afetado, redação atual, redação proposta e justificativa.
3. O formulário exige que o proponente declare ciência de que seus dados ficarão públicos.
4. A *issue* em branco fica desativada (`config.yml`), para que toda *issue* chegue no formato do formulário.
5. O resultado da deliberação é registrado na própria *issue*, que é fechada com referência ao *commit* ou com a justificativa da rejeição.

O fluxo completo está em [`specs/project-vision/spec.md`](../../specs/project-vision/spec.md).

## Consequências
- **Positivas:**
  * A sugestão chega pronta para a deliberação, com o dispositivo e a redação proposta já escritos.
  * Toda sugestão feita por *issue* fica registrada, com autor, data e desfecho, mesmo quando rejeitada.
  * A identificação pelo número CBO permite à federação confirmar que o proponente é atleta e a qual clube pertence.
- **Negativas/Atenção:**
  * Nome completo, número CBO e clube do proponente ficam **públicos** no GitHub. O atleta que não quiser se expor continua tendo o canal pelo clube.
  * O canal exige conta no GitHub, o que afasta parte dos atletas. Por isso o canal pelo clube não foi extinto.
  * O diretor técnico do clube pode só tomar conhecimento da sugestão de um atleta seu na deliberação, e não antes.
  * O formulário não valida o número CBO nem o clube informados. A conferência é manual, feita pela federação.
  * Desativar a *issue* em branco obriga também relatos que não são sugestão de regra (erro de digitação, link quebrado) a passar pelo formulário, até que se crie um modelo próprio para eles.

## Revisão de 2026-10-17
O modelo próprio previsto na última consequência acima passou a existir: a [ADR-005](ADR-005-controle-de-pendencias-por-issues.md) criou os formulários de `tarefa` (das equipes de regras e do repositório) e de `acompanhamento`. A decisão desta ADR permanece, e o formulário de sugestão de regra passou a aplicar também o rótulo `equipe: regras`.
