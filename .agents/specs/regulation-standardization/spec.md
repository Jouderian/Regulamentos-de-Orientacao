---
description: Conversão e padronização em Markdown dos regulamentos históricos do acervo (2012-2025)
status: concluída
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
8. **Nomenclatura histórica**: as atuais *Regras de Orientação Pedestre* (ROP) da CBO chamavam-se antes *Regras Gerais de Orientação Pedestre* (RGOP). Nos regulamentos antigos, a sigla RGOP é mantida como no original, sem trocar por ROP. Ela designa o mesmo documento nacional, e por isso o campo `rop_referencia` do frontmatter se aplica normalmente a esses regulamentos.

## Critérios de Aceitação
- [x] Todo regulamento com PDF no acervo possui o `.md` correspondente na mesma pasta.
- [x] Os `.md` existentes seguem o padrão `**Art. Nº** – Texto` e `> **Parágrafo Nº:** Texto`.
- [x] Nenhum `.md` do acervo contém artefatos de conversão (U+00AD, BOM, hifenização de fim de linha, palavras sem acento).
- [x] A verificação `python .agents/scripts/verificar-documentos.py` passa sem problemas.

## Cobertura do Acervo
A conversão do acervo foi concluída em 2026-10-31 ([*issue* #15](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/15)). A situação de cada ano fica **somente** na tabela do [`README.md`](../../../README.md), para não haver cópias divergentes.

## Passo a Passo
1. Converter o PDF do ano com `python .agents/scripts/import-pdf.py Documentos/<ano>/<arquivo>.pdf`.
2. Revisar manualmente os pontos listados no workflow [`import-pdf.md`](../../workflows/import-pdf.md) (cabeçalhos, rodapés, tabelas, hifenização).
3. Comparar o Markdown com o PDF original artigo a artigo, confirmando que nenhuma regra foi perdida ou alterada.
4. Rodar `python .agents/scripts/verificar-documentos.py` e corrigir o que for apontado.
5. Atualizar a tabela de cobertura do `README.md`.
