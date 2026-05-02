---
description: Decisão sobre o método de extração e padronização dos regulamentos históricos (2018-2025).
---

# ADR 003: Padronização de Regulamentos Históricos (2018-2025)

## Contexto
O projeto precisava incorporar regulamentos antigos (2018 a 2025) que estavam disponíveis apenas no formato PDF ou DOCX. A exigência era que o repositório inteiro mantivesse um padrão de Markdown estrito, semelhante ao regulamento vigente de 2026, para permitir rastreabilidade, versionamento e manutenção limpa.

## Problemas
1. Extração direta de PDFs pode perder a formatação de tabelas (ex: calendário de etapas).
2. PDFs comprimidos sem camada de texto clara dificultam a importação.
3. A conversão nativa do MS Word em background bloqueia a automação devido a prompts de segurança interativos ("Reflow").
4. **Lacuna Temporal (2020-2021):** Identificação de que não houve campeonatos nestes anos devido à pandemia de COVID-19, justificando a ausência de arquivos para processamento nestes períodos específicos.

## Decisão
A conversão e padronização foram divididas em duas abordagens dependendo do estado do arquivo:
1. **Abordagem Primária (Automatizada):** Utilização da ferramenta `pdftotext` (proveniente do pacote xpdf/Poppler, e nativamente incluída na instalação do Git for Windows) com a flag `-layout` para extrair os textos mantendo a estrutura original, preservando visualmente as tabelas e espaçamentos.
2. **Abordagem Secundária (Fallback):** Conversão manual do PDF para DOCX usando o MS Word, seguida pela utilização do utilitário `Pandoc` (`pandoc -f docx -t gfm`) para a conversão em Markdown. (Utilizado para o arquivo de 2017/2018).

Após a extração, foi aplicado um motor de Expressões Regulares (Regex) via PowerShell para converter padronizadamente a tipografia jurídica do CCO:
- Capítulos (`CAPÍTULO X - ...`) -> `## CAPÍTULO X - ...`
- Artigos (`Art. Xº - ...`) -> `**Art. Xº** – ...`
- Parágrafos (`Parágrafo 1º:`) -> `> **Paragrafo 1º:**`
- Incisos (`a)`) -> `>> **a)**`

## Consequências
- **Positivas:** Todo o acervo histórico (2018-2025) agora está legível, indexável via git e segue a tipografia do repositório, permitindo diffs claros entre os anos.
- **Negativas/Atenção:** As tabelas (calendário de etapas) convertidas via `pdftotext` mantêm o alinhamento visual com espaços, mas não as marcações oficiais do Markdown (`|---|`). Uma revisão visual ou ajustes finos manuais serão necessários nas tabelas.
