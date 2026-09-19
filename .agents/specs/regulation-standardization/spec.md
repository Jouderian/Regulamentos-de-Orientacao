---
description: Conversão e padronização em Markdown dos regulamentos históricos do acervo (2012-2025)
---

# Especificação: Padronização de Regulamentos Históricos

## Contexto
O acervo do repositório reúne os regulamentos do CCO e do CCOS desde 2012, originalmente distribuídos apenas em PDF e sem estrutura uniforme entre as edições. Para que o acervo seja pesquisável, comparável entre anos e consumível por IAs, cada regulamento precisa existir também em Markdown, seguindo a mesma tipografia jurídica do regulamento vigente.

## Objetivo
Converter os regulamentos históricos para Markdown preservando integralmente o conteúdo normativo de cada ano e aplicando a estrutura, a hierarquia e o estilo visual do modelo unificado de 2026.

## Requisitos
1. **Formato**: arquivos `.md` codificados em UTF-8 **sem BOM**, com finais de linha LF.
2. **Localização**: o Markdown fica **ao lado do PDF de origem**, na própria pasta do ano — `Documentos/<ano>/`. Não há subpasta `markdowns/`.
3. **Nomenclatura**: mesmo nome-base do PDF de origem, em camelCase — `regulamentoCCO.md`, `regulamentoCCOS.md`, `regrasOrientacaoPedestre.md`. O ano **não** entra no nome do arquivo, pois já é dado pelo diretório.
4. **Estrutura**: hierarquia de Capítulos, Artigos, Parágrafos, Incisos e Alíneas conforme o modelo do projeto (ver `plan.md`).
5. **Fidelidade**: o conteúdo normativo do ano é preservado sem reinterpretação. Só se corrige o que é comprovadamente artefato de conversão (palavra partida, acento perdido, tabela deformada).
6. **Idioma**: Português do Brasil (pt-BR).
7. **Ferramenta**: conforme a [ADR-003](../../wiki/decisions/ADR-003-historical-regulation-standardization.md).

## Critérios de Aceitação
- [ ] Todo regulamento com PDF no acervo possui o `.md` correspondente na mesma pasta.
- [x] Os `.md` existentes seguem o padrão `**Art. Nº** – Texto` e `> **Parágrafo Nº:** Texto`.
- [x] Nenhum `.md` do acervo contém artefatos de conversão (U+00AD, BOM, hifenização de fim de linha, palavras sem acento).
- [x] A verificação `python .agents/scripts/verificar-documentos.py` passa sem problemas.

## Cobertura Atual do Acervo
Estado em 2026-09-19. O `—` indica ausência do documento no acervo; "não realizado" indica que a competição não ocorreu naquele ano.

| Ano | CCO | CCOS | Observação |
| :---: | :---: | :---: | :--- |
| 2012 | **MD** + PDF | **MD** + PDF | completo |
| 2013 a 2016 | PDF | PDF | pendente de conversão |
| 2017 | **MD** + PDF | PDF | CCOS pendente |
| 2018 | PDF | PDF | pendente de conversão |
| 2019 | **MD** + PDF | PDF | CCOS pendente |
| 2020-2021 | — | — | sem competição (COVID-19) |
| 2022 | **MD** + PDF | PDF | CCOS pendente |
| 2023 | **MD** + PDF | **MD** + PDF | completo |
| 2024 | **MD** + PDF | **MD** + PDF | completo |
| 2025 | **MD** + PDF | — | CCOS não realizado (CamBOS) |
| 2026 | **MD** + PDF | **MD** + PDF | documento unificado (evento CCOS cancelado após publicação); a ROP 2026 vigente está na raiz |
| 2027 | PDF/DOCX | PDF/DOCX | fonte é o `.md` da raiz |

## Passo a Passo
1. Converter o PDF do ano com `python .agents/scripts/import-pdf.py Documentos/<ano>/<arquivo>.pdf`.
2. Revisar manualmente os pontos listados no workflow [`import-pdf.md`](../../workflows/import-pdf.md) (cabeçalhos, rodapés, tabelas, hifenização).
3. Comparar o Markdown com o PDF original artigo a artigo, confirmando que nenhuma regra foi perdida ou alterada.
4. Rodar `python .agents/scripts/verificar-documentos.py` e corrigir o que for apontado.
5. Atualizar a tabela de cobertura acima e a do `README.md`.
