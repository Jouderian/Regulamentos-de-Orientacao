---
description: Backlog persistente e tarefas pendentes do projeto
---

# Tarefas Pendentes (Backlog)

- [x] **Bloco de metadados nos regulamentos:** Adicionado frontmatter YAML no topo de todos os 12 regulamentos declarando `ano`, `edicao`, `status` (`vigente`/`arquivado`) e `rop_referencia`. Criado o script `python .agents/scripts/gerar-documentos.py` que remove o frontmatter antes do Pandoc (impedindo vazamentos no `.docx`/`.pdf`) e compila ambos os formatos de forma integrada. O script `verificar-documentos.py` foi estendido para validar a obrigatoriedade dos campos e exigir exatamente 1 regulamento com `status: vigente`.
- [ ] Melhorar a redação para contemplar a obrigatoriedade de estar inscrito na etapa de descarte para pode descarta-la.
- [ ] **Atualizar as ações do CI (Node.js 20 descontinuado):** O GitHub descontinuou o Node.js 20 e passou a forçar `actions/checkout@v4` e `actions/setup-python@v5` a rodar em Node.js 24, emitindo aviso em toda execução de `.github/workflows/verificacao-documental.yml`. Quando as versões seguintes dessas ações estiverem estáveis, atualizá-las no workflow. Não há urgência: é apenas um aviso e o CI continua passando. ([anúncio do GitHub](https://github.blog/changelog/2025-09-19-deprecation-of-node-20-on-github-actions-runners/))
- [ ] **Lembrete de Atualização da ROP 2027:** Atualizar o arquivo `regrasOrientacaoPedestre.md` na raiz com o regulamento oficial de 2027 assim que for publicado pela CBO. **Antes de substituir**, copiar a versão atual da raiz para `Documentos/2026/regrasOrientacaoPedestre.md`, conforme a regra de arquivamento na virada (`.agents/rules/rules.md`).
- [ ] **Conversão do acervo pendente:** Converter os 23 documentos listados em [`specs/regulation-standardization/tasks.md`](specs/regulation-standardization/tasks.md): 6 regulamentos do CCO (2012-2016 e 2018), 9 do CCOS (2012-2019 e 2022) e 8 ROPs nacionais. Cada conversão exige revisão do usuário contra o PDF original antes do commit, por ser texto normativo. A limpeza do [`import-pdf.py`](scripts/import-pdf.py), que era pré-requisito desta tarefa, está concluída.
  - **Dois PDFs não convertem direto** — levantamento feito rodando o script sobre os 23 pendentes:
    - `Documentos/2018/regulamentoCCO.pdf`: escaneado, sem camada de texto. Exige OCR (`pip install markitdown-ocr`, nota em [`workflows/import-pdf.md`](workflows/import-pdf.md)) ou redigitação.
    - `Documentos/2018/regulamentoCCOS.pdf`: tem camada de texto, mas sem quebras de linha — o documento inteiro sai como uma única linha com tabulações no lugar dos espaços. Precisa de reconstrução manual das quebras.
  - Os outros 21 extraem texto estruturado e estão prontos para conversão e revisão.
- [ ] **Habilitar issues no GitHub para sugestões de regra:** Ativar as *Issues* no repositório e criar um formulário (`.github/ISSUE_TEMPLATE/sugestao-regra.yml`) com campos fixos — artigo afetado, redação atual, redação proposta e justificativa — para que clubes e atletas encaminhem sugestões já no formato usado na deliberação, conforme o fluxo descrito em `.agents/specs/project-vision/spec.md`.
- [ ] **Sugestões para a CBO (ROP 2027 - Tabelas de Idades):** Encaminhar a proposta de atualização dos anos-limite de nascimento na tabela do item 2.1.3 da ROP para o ciclo de 2027:
  - INFANTIL (H10/D10): nascidos em 2017 ou após (anterior: 2016)
  - INFANTIL (H12/D12): nascidos em 2015 ou após (anterior: 2014)
  - JUVENIL (H14/D14): nascidos em 2013 ou após (anterior: 2012)
  - JUVENIL (H16/D16): nascidos em 2011 ou após (anterior: 2010)
  - JUVENIL (H18/D18): nascidos em 2009 ou após (anterior: 2008)
  - JÚNIOR (H20/D20): nascidos em 2007 ou após (anterior: 2006)
  - MASTER (H35/D35): nascidos em 1992 ou antes (anterior: 1991)
  - MASTER (H40/D40): nascidos em 1987 ou antes (anterior: 1986)
  - SENIOR (H45/D45): nascidos em 1982 ou antes (anterior: 1981)
  - SENIOR (H50/D50): nascidos em 1977 ou antes (anterior: 1976)
  - VETERANO (H55/D55): nascidos em 1972 ou antes (anterior: 1971)
  - VETERANO (H60/D60): nascidos em 1967 ou antes (anterior: 1966)
  - VIP (H65/D65): nascidos em 1962 ou antes (anterior: 1961)
  - VIP (H70/D70): nascidos em 1957 ou antes (anterior: 1956)
  - VIP (H75/D75): nascidos em 1952 ou antes (anterior: 1951)
  - VIP (H80/D80): nascidos em 1947 ou antes (anterior: 1946)
  - VIP (H85/D85): nascidos em 1942 ou antes (anterior: 1941)
  - VIP (H90/D90): nascidos em 1937 ou antes (anterior: 1936)
  - VIP (H95/D95): nascidos em 1932 ou antes (anterior: 1931)
