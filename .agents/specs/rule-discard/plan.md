---
description: Plano de implementação para a regra de descarte no CCO
---
# Plano: Regra de Descarte (CCO)

## 1. Alterações no Regulamento (`regulamentoCompeticoesCearenses.md`)

A implementação será feita na seção correspondente à apuração e classificação do campeonato.

**Art. 34 (Classificação Individual Geral):**
- **Atual:** "A classificação individual geral será o somatório de todos os pontos obtidos (em todas as etapas/percursos), sem descartes."
- **Proposto:** Substituir pela seguinte redação do caput e §1º para deixar o cancelamento inquestionável:
  > *"Art. 34 – **Exclusivo do CCO:** A classificação individual geral do CCO será calculada com base no somatório dos pontos obtidos pelo atleta em todas as etapas, descartando-se obrigatoriamente 1 (uma) etapa, aquela com a menor pontuação, desde que o campeonato tenha sido disputado em mais de 3 (três) etapas."*
  > *"§ 1º: Caso o campeonato, **inclusive por motivo de cancelamento de etapas pela organização**, venha a ser disputado em 3 (três) etapas ou menos, não haverá descarte e a classificação será dada pelo somatório de todas as etapas efetivamente realizadas."*
- Adicionar os demais parágrafos de proteção (exceções de descarte para desclassificação por não registrar chegada ou categorias anuladas) e os critérios de desempate (que hoje estão no parágrafo único).

**Art. 33 (Pontuação de Voluntários):**
- **Atual:** A pontuação do voluntário é a média conquistada nas outras etapas.
- **Proposto:** Atualizar o § 1º com a seguinte redação para blindar a regra de participações e cancelamentos:
  > *"§ 1º (CCO) - O atleta deve competir em, no mínimo, metade das etapas do campeonato anual — **considerando para este cálculo apenas as etapas efetivamente realizadas (excluindo-se eventuais etapas canceladas) e arredondando-se o valor fracionário para baixo** — para ter direito aos pontos. A média é calculada sobre o conjunto das etapas em que o atleta efetivamente competiu (excluída a etapa de voluntário), aplicando-se previamente o descarte previsto no Art. 34 a esse conjunto, quando aplicável."*

**Art. 23 (Penalidades de Chegada):**
- O parágrafo único atual já diz que o descumprimento gera penalização "tornando a etapa/percurso não passível de descarte". Esta redação já está pronta e perfeitamente alinhada com a volta do descarte, não requerendo alteração.

## 2. Solução Matemática para Cancelamentos

A condição de "mais de 3 etapas" resolve o problema da divisão por zero para voluntários. Caso um CCO de 4 etapas perca 1 etapa e caia para 3 etapas, o descarte é totalmente desativado (3 não é maior que 3). Assim, a média do voluntário será a média simples das etapas que ele correu, sem remover nenhuma nota, resolvendo organicamente o edge case e validando os princípios SDD exigidos.
