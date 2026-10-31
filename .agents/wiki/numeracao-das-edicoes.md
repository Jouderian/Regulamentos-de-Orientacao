---
description: Critério de numeração das edições do CCO e do CCOS — ano sem campeonato realizado não consome número de edição.
---

# Numeração das Edições

Última atualização: 2026-10-31

## Critério

O número da edição (algarismo romano) conta campeonatos **realizados**. Ano sem campeonato não recebe número, e o ano seguinte usa o próximo número livre. Isso vale também para campeonato cancelado depois da publicação do regulamento: o número previsto passa para o ano seguinte.

O critério foi alinhado com a FECORI em 2026-10-31, a partir do cancelamento do CCOS 2026, e confirma o que o acervo já fazia.

## Casos

| Ano | Competição | Motivo | Numeração |
| :---: | :--- | :--- | :--- |
| 2026 | CCOS | Cancelado pela FECORI após a publicação do regulamento | O XIII previsto passou para 2027 |
| 2025 | CCOS | A FECORI sediou o CamBOS | XII em 2024, XIII em 2026 |
| 2020 e 2021 | CCO e CCOS | Pandemia de COVID-19 | CCO: XV em 2019, XVI em 2022; CCOS: IX em 2019, X em 2022 |

## Onde a numeração aparece

- No campo `edicao` do frontmatter do regulamento e nos títulos dos calendários de cada competição.
- Na coluna "Edição" de [`clubesCampeoes.md`](../../clubesCampeoes.md), que mostra "-" no ano sem campeonato.
- Regulamento já publicado com o número de uma edição cancelada não muda, porque o PDF está congelado ([ADR-006](decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md)); a explicação fica na `notaHistorica.md` do ano.
