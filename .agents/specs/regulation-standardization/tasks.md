---
description: Lista de tarefas da conversão dos regulamentos históricos, por ano e competição
status: concluída
---

# Tarefas: Padronização de Regulamentos Históricos

Cada item corresponde a um PDF do acervo e ao seu `.md` em `Documentos/<ano>/`.
Concluir um item exige: converter, revisar contra o PDF original e passar na
verificação (`python .agents/scripts/verificar-documentos.py`).

## Situação atual dos documentos

A conversão foi concluída: todo regulamento e toda ROP do acervo têm o `.md` ao lado do PDF.

## Anos sem tarefa

- **2026 e 2027**: regulamento unificado (CCO e CCOS), escrito direto em Markdown, sem conversão de PDF.
- **2025 (CCOS)**: não realizado; a FECORI sediou o CamBOS.
- **2020 e 2021**: não houve campeonato estadual (COVID-19) — só existem as ROP nacionais.

## Finalização

- [x] Saneamento dos artefatos de conversão dos arquivos já convertidos.
- [x] Verificação automatizada cobrindo tipografia e artefatos (`verificar-documentos.py`).
- [ ] Revisão geral de consistência entre todos os anos após a conversão completa — registrada na [*issue* #30](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/30).
- [x] Atualização do `README.md` com a tabela de cobertura do acervo.
