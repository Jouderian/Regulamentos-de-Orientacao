---
description: Decisão sobre o método de extração e padronização dos regulamentos históricos (2018-2025).
---

# ADR 003: Padronização de Regulamentos Históricos (2018-2025)

## Contexto
O projeto precisava incorporar regulamentos antigos (2018 a 2025) que estavam disponíveis apenas no formato PDF ou DOCX. A exigência era que o repositório inteiro mantivesse um padrão de Markdown estrito, para permitir rastreabilidade, versionamento e manutenção limpa.

## Problemas
1. Extração direta de PDFs pode perder a formatação de tabelas (ex: calendário de etapas).
2. PDFs comprimidos sem camada de texto clara dificultam a importação.
3. A conversão nativa do MS Word em background bloqueia a automação devido a prompts de segurança interativos ("Reflow").
4. **Lacuna Temporal (2020-2021):** Identificação de que não houve campeonatos nestes anos devido à pandemia de COVID-19, justificando a ausência de arquivos para processamento nestes períodos específicos.

## Decisão
A partir de 2026, a abordagem para conversão e padronização foi evoluída para priorizar o uso do **MarkItDown** (Microsoft) devido à sua superioridade no tratamento de tabelas nativas de Markdown e suporte direto a `.docx` e PDFs estruturados. A estratégia de conversão divide-se em:

1. **Abordagem Primária (Automatizada):** Utilização do script Python [.agents/scripts/import-pdf.py](file:///c:/Users/joude/.gemini/antigravity-ide/scratch/Regulamentos-de-Orientacao/.agents/scripts/import-pdf.py) (que usa a biblioteca `markitdown`) para realizar a extração do PDF diretamente para um arquivo Markdown contendo tabelas estruturadas nativas (`|---|`) e aplicar Regex automáticas de padronização jurídica:
   - Capítulos (`CAPÍTULO X - ...`) -> `## CAPÍTULO X - ...`
   - Artigos (`Art. Xº - ...`) -> `**Art. Xº** – ...`
   - Parágrafos (`Parágrafo 1º:`) -> `> **Parágrafo 1º:**`
   - Incisos (`a)`) -> `>> **a)**`
2. **Abordagem Secundária (Legado/Fallback):** Utilização da ferramenta `pdftotext` com a flag `-layout` para arquivos mais antigos onde o MarkItDown não consiga processar adequadamente a estrutura semântica ou que exijam uma extração puramente espacial.
3. **Abordagem Terciária:** Conversão manual de PDF para DOCX pelo MS Word seguida de conversão pelo `Pandoc` (`pandoc -f docx -t gfm`).

## Consequências
- **Positivas:**
  * Redução significativa no retrabalho de formatação de tabelas (que agora são geradas nativamente com as marcações `|---|` pelo MarkItDown).
  * Automatização das substituições de Regex (Capítulos, Artigos, Parágrafos) direto na extração pelo script [import-pdf.py](file:///c:/Users/joude/.gemini/antigravity-ide/scratch/Regulamentos-de-Orientacao/.agents/scripts/import-pdf.py).
  * Todo o acervo histórico e futuros regulamentos seguem a tipografia idêntica do repositório.
- **Negativas/Atenção:**
  * Adição de dependência do ambiente Python local e do pacote `markitdown` para os contribuidores executarem a automação.
  * O pós-processamento e revisão manual continuam necessários para eliminar artefatos comuns de conversão (títulos repetidos de topo, rodapés e quebras de linha/hifens órfãos).

