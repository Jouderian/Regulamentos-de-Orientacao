---
description: Lista de tarefas da conversão dos regulamentos históricos, por ano e competição
---

# Tarefas: Padronização de Regulamentos Históricos

Cada item corresponde a um PDF do acervo e ao seu `.md` em `Documentos/<ano>/`.
Concluir um item exige: converter, revisar contra o PDF original e passar na
verificação (`python .agents/scripts/verificar-documentos.py`).

## Campeonato Cearense de Orientação (CCO)

- [x] 2012 — `Documentos/2012/regulamentoCCO.md`
- [ ] 2013 — `Documentos/2013/regulamentoCCO.md`
- [ ] 2014 — `Documentos/2014/regulamentoCCO.md`
- [ ] 2015 — `Documentos/2015/regulamentoCCO.md`
- [ ] 2016 — `Documentos/2016/regulamentoCCO.md`
- [x] 2017 — `Documentos/2017/regulamentoCCO.md`
- [ ] 2018 — `Documentos/2018/regulamentoCCO.md`
- [x] 2019 — `Documentos/2019/regulamentoCCO.md`
- [x] 2022 — `Documentos/2022/regulamentoCCO.md`
- [x] 2023 — `Documentos/2023/regulamentoCCO.md`
- [x] 2024 — `Documentos/2024/regulamentoCCO.md`
- [x] 2025 — `Documentos/2025/regulamentoCCO.md`

## Campeonato Cearense de Orientação Sprint (CCOS)

- [x] 2012 — `Documentos/2012/regulamentoCCOS.md`
- [ ] 2013 — `Documentos/2013/regulamentoCCOS.md`
- [ ] 2014 — `Documentos/2014/regulamentoCCOS.md`
- [ ] 2015 — `Documentos/2015/regulamentoCCOS.md`
- [ ] 2016 — `Documentos/2016/regulamentoCCOS.md`
- [ ] 2017 — `Documentos/2017/regulamentoCCOS.md`
- [ ] 2018 — `Documentos/2018/regulamentoCCOS.md`
- [ ] 2019 — `Documentos/2019/regulamentoCCOS.md`
- [ ] 2022 — `Documentos/2022/regulamentoCCOS.md`
- [x] 2023 — `Documentos/2023/regulamentoCCOS.md`
- [x] 2024 — `Documentos/2024/regulamentoCCOS.md`

## Regras de Orientação Pedestre (ROP — documento nacional da CBO)

- [ ] 2017 — `Documentos/2017/regrasGeraisDeOrientacaoPedestre.md`
- [ ] 2018 — `Documentos/2018/regrasOrientacaoPedestre.md`
- [ ] 2019 — `Documentos/2019/regrasOrientacaoPedestre.md`
- [ ] 2020 — `Documentos/2020-2021/regrasOrientacaoPedestre_2020.md`
- [ ] 2021 — `Documentos/2020-2021/regrasOrientacaoPedestre_2021.md`
- [ ] 2022 — `Documentos/2022/regrasOrientacaoPedestre.md`
- [x] 2023 — `Documentos/2023/regrasOrientacaoPedestre.md`
- [ ] 2024 — `Documentos/2024/regrasOrientacaoPedestre.md`
- [x] 2025 — `Documentos/2025/regrasOrientacaoPedestre.md`
- [x] 2026 — `regrasOrientacaoPedestre.md` (na raiz: é a edição vigente; será arquivada em `Documentos/2026/` quando a ROP 2027 sair)

## Anos sem tarefa

- **2020 e 2021**: não houve campeonato estadual (COVID-19) — só existem as ROP nacionais.
- **2025 (CCOS)**: não realizado; a FECORI sediou o CamBOS.
- **2026 e 2027**: regulamento unificado, mantido como fonte na raiz do repositório.

## Finalização

- [x] Saneamento dos artefatos de conversão dos arquivos já convertidos.
- [x] Verificação automatizada cobrindo tipografia e artefatos (`verificar-documentos.py`).
- [ ] Revisão geral de consistência entre todos os anos após a conversão completa.
- [x] `README.md` com a tabela de cobertura do acervo.
