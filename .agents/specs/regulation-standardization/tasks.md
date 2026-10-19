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
| 2012 | ✗ | ✔ | ✔ |
| 2013 | ✗ | ✔ | ✔ |
| 2014 | ✗ | ✗ | ✗ |
| 2015 | ✗ | ✗ | ✗ |
| 2016 | ✗ | ✔ | ✔ |
| 2017 | ✗ | ✔ | ✔ |
| 2018 | ✗ | ✔ | ✔ |
| 2019 | ✗ | ✔ | ✔ |
| 2020 | ✗ | — | — |
| 2021 | ✗ | — | — |
| 2022 | ✗ | ✔ | ✔ |
| 2023 | ✔ | ✔ | ✔ |
| 2024 | ✗ | ✔ | ✔ |
| 2025 | ✔ | ✔ | — |
| 2026 | ✔ | ✔ | ✔ |
| 2027 | — | ✔ | ✔ |

**Legenda:** ✔ Feito | ✗ Não feito | — Não aplicável (sem PDF no acervo ou competição não realizada)

- **ROP:** Regras de Orientação Pedestre (documento nacional da CBO)
- **CCO:** Campeonato Cearense de Orientação
- **CCOS:** Campeonato Cearense de Orientação Sprint

## Anos sem tarefa

- **2020 e 2021**: não houve campeonato estadual (COVID-19) — só existem as ROP nacionais.
- **2025 (CCOS)**: não realizado; a FECORI sediou o CamBOS.
- **2026 e 2027**: regulamento unificado (CCO e CCOS), mantido como fonte na raiz do repositório.

## Finalização

- [x] Saneamento dos artefatos de conversão dos arquivos já convertidos.
- [x] Verificação automatizada cobrindo tipografia e artefatos (`verificar-documentos.py`).
- [ ] Revisão geral de consistência entre todos os anos após a conversão completa.
- [x] Atualização do `README.md` com a tabela de cobertura do acervo.
