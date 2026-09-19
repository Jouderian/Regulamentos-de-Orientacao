---
description: Lista de tarefas da conversão dos regulamentos históricos, por ano e competição
---

# Tarefas: Padronização de Regulamentos Históricos

Cada item corresponde a um PDF do acervo e ao seu `.md` em `Documentos/<ano>/`.
Concluir um item exige: converter, revisar contra o PDF original e passar na
verificação (`python .agents/scripts/verificar-documentos.py`).

## Situação atual dos documentos

| Ano | ROP | CCO | CCOS |
| :---: | :---: | :---: | :---: |
| 2012 | — | ✔ | ✔ |
| 2013 | — | X | X |
| 2014 | — | X | X |
| 2015 | — | X | X |
| 2016 | — | X | X |
| 2017 | X | ✔ | X |
| 2018 | X | X | X |
| 2019 | X | ✔ | X |
| 2020 | X | — | — |
| 2021 | X | — | — |
| 2022 | X | ✔ | X |
| 2023 | ✔ | ✔ | ✔ |
| 2024 | X | ✔ | ✔ |
| 2025 | ✔ | ✔ | — |
| 2026 | ✔ | ✔ | ✔ |
| 2027 | — | ✔ | ✔ |

**Legenda:** ✔ Feito | ✗ Não feito | — Não aplicável (sem PDF no acervo ou competição não realizada)

- **ROP:** Regras de Orientação Pedestre (documento nacional da CBO)
- **CCO:** Campeonato Cearense de Orientação
- **CCOS:** Campeonato Cearense de Orientação Sprint

## Anos sem tarefa

- **2012 a 2016 (ROP)**: não constam PDFs dessas edições no acervo.
- **2020 e 2021**: não houve campeonato estadual (COVID-19) — só existem as ROP nacionais.
- **2025 (CCOS)**: não realizado; a FECORI sediou o CamBOS.
- **2026 e 2027**: regulamento unificado (CCO e CCOS), mantido como fonte na raiz do repositório.

## Finalização

- [x] Saneamento dos artefatos de conversão dos arquivos já convertidos.
- [x] Verificação automatizada cobrindo tipografia e artefatos (`verificar-documentos.py`).
- [ ] Revisão geral de consistência entre todos os anos após a conversão completa.
- [x] Atualização do `README.md` com a tabela de cobertura do acervo.
