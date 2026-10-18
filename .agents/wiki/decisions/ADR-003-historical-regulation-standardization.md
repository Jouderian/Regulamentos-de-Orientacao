---
description: Decisão sobre o método de extração e padronização dos regulamentos históricos do acervo.
---

# ADR 003: Padronização de Regulamentos Históricos

## Contexto
O projeto precisava incorporar ao acervo os regulamentos antigos (2012 em diante), disponíveis apenas em PDF ou DOCX. A exigência era que o repositório inteiro mantivesse um padrão de Markdown estrito, para permitir rastreabilidade, versionamento e manutenção limpa.

## Problemas
1. Extração direta de PDFs pode perder a formatação de tabelas (ex: calendário de etapas).
2. PDFs comprimidos sem camada de texto clara dificultam a importação.
3. A conversão nativa do MS Word em background bloqueia a automação devido a prompts de segurança interativos ("Reflow").
4. **Lacuna Temporal (2020-2021):** Identificação de que não houve campeonatos nestes anos devido à pandemia de COVID-19, justificando a ausência de arquivos para processamento nestes períodos específicos.

## Decisão
A partir de 2026, a abordagem para conversão e padronização foi evoluída para priorizar o uso do **MarkItDown** (Microsoft) devido à sua superioridade no tratamento de tabelas nativas de Markdown e suporte direto a `.docx` e PDFs estruturados. A estratégia de conversão divide-se em:

1. **Abordagem Primária (Automatizada):** Utilização do script Python [.agents/scripts/import-pdf.py](../../scripts/import-pdf.py) (que usa a biblioteca `markitdown`) para realizar a extração do PDF diretamente para um arquivo Markdown contendo tabelas estruturadas nativas (`|---|`) e aplicar Regex automáticas de padronização jurídica:
   - Capítulos (`CAPÍTULO X - ...`) -> `## CAPÍTULO X - ...`
   - Artigos (`Art. Xº - ...`) -> `**Art. Xº** – ...`
   - Parágrafos (`Parágrafo 1º:`) -> `> **Parágrafo 1º:**`
   - Incisos (`a)`) -> `>> **a)**`
2. **Abordagem Secundária (Legado/Fallback):** Utilização da ferramenta `pdftotext` com a flag `-layout` para arquivos mais antigos onde o MarkItDown não consiga processar adequadamente a estrutura semântica ou que exijam uma extração puramente espacial.
3. **Abordagem Terciária:** Conversão manual de PDF para DOCX pelo MS Word seguida de conversão pelo `Pandoc` (`pandoc -f docx -t gfm`).

## Consequências
- **Positivas:**
  * Redução significativa no retrabalho de formatação de tabelas (que agora são geradas nativamente com as marcações `|---|` pelo MarkItDown).
  * Automatização das substituições de Regex (Capítulos, Artigos, Parágrafos) direto na extração pelo script [import-pdf.py](../../scripts/import-pdf.py).
  * Todo o acervo histórico e futuros regulamentos seguem a tipografia idêntica do repositório.
- **Negativas/Atenção:**
  * Adição de dependência do ambiente Python local e do pacote `markitdown` para os contribuidores executarem a automação.
  * O pós-processamento e revisão manual continuam necessários para eliminar artefatos comuns de conversão (títulos repetidos de topo, rodapés e quebras de linha/hifens órfãos).

## Revisão de 2026-09-13
A revisão do acervo mostrou que a revisão manual, sozinha, não segurou a qualidade: sobraram 41 hifens condicionais invisíveis (U+00AD), 228 ocorrências de `Paragrafo` sem acento, 162 palavras partidas por hifenização de fim de linha na ROP 2023 e diversos trechos sem acento no regulamento de 2019 — todos corrigidos. A decisão de ferramenta permanece, acrescida de uma salvaguarda: a conversão só é aceita depois de passar em [`verificar-documentos.py`](../../scripts/verificar-documentos.py), executado também pelo CI. O escopo desta ADR passa a ser todo o acervo (2012 em diante), e não apenas 2018-2025: 2017 já foi convertido e 2018 ainda não.

## Revisão de 2026-10-17: Numeração de Artigos (Ordinal vs. Cardinal)
Ficou formalizada a convenção da técnica legislativa brasileira (Lei Complementar nº 95/1998, art. 10, inciso I) para a numeração de artigos em todos os regulamentos:
- **Art. 1º a Art. 9º**: grafados com número ordinal e indicador ordinal `º` (U+00BA), seguido de espaço, meia-risca (*en dash* `–`) e texto. Exemplo: `**Art. 1º** – ...`
- **Art. 10 em diante**: grafados com número cardinal (sem indicador ordinal), seguido de espaço, meia-risca (*en dash* `–`) e texto. Exemplo: `**Art. 10** – ...`

Essa convenção consolida a prática vigente do regulamento unificado de 2026 e da maioria dos documentos históricos do acervo, servindo como critério para o saneamento das inconsistências remanescentes (definido na issue #12).

## Revisão de 2026-10-17: Alinhamento do `import-pdf.py` ao padrão tipográfico
Testado com `Documentos/2014/regulamentoCCO.pdf`, o [import-pdf.py](../../scripts/import-pdf.py) ainda entregava um rascunho fora do padrão do acervo (issue #10). A escolha do MarkItDown permanece; mudou o que o script produz, e a lista de regras da *Decisão* acima passa a valer com estas diferenças:
- **Alínea:** `>> **a.**`, e não `>> **a)**`. O script reconhece `a)` e `a.` no PDF.
- **Parágrafo único:** `> **Parágrafo Único:**`, com maiúscula, como no restante do acervo. O separador `.` (`Parágrafo 1º.`) passa a ser reconhecido.
- **Artigo:** aceita `Art 8º -`, sem ponto, e aplica a convenção da revisão anterior: `**Art. 9º**` até o nono e `**Art. 12**` do décimo em diante.
- **Capítulo numerado:** `1. DA REGULAMENTAÇÃO GERAL` vira `## 1. DA REGULAMENTAÇÃO GERAL`. Só se aplica à linha sem minúsculas, para não confundir com inciso numerado (`1. Alunos matriculados...`).
- **Calendário:** o bloco `ETAPA DATA ORGANIZADOR` seguido de linhas `1ª 13/Abr COFORT` vira tabela Markdown.
- **Título e timbre:** as letras duplicadas do negrito simulado (`RREEGGUULLAAMMEENNTTOO`) são desfeitas, o título vira `# Regulamento do X Campeonato Cearense de Orientação` e o timbre de três linhas da Federação é removido por inteiro.
- **Frontmatter:** o Markdown sai com `ano`, `edicao`, `status: arquivado`, `rop_referencia` e `description`, os campos que o verificador exige. `ano` vem da pasta `Documentos/<ano>/` do PDF e `edicao`, do numeral romano do título; `rop_referencia` repete o ano, como em todo o acervo convertido. Ano e edição são fatos normativos e não se estimam: sem origem identificável, o script para e pede `--ano` ou `--edicao`.

**Limites conhecidos**, a tratar na revisão manual ou na conversão do acervo pendente (issue #15):
- as heurísticas foram calibradas no layout de 2014; alguns PDFs de 2015 a 2017 trazem título partido por linhas em branco, número do artigo isolado na linha ou calendário em colunas separadas, e o script deixa esses trechos como estão;
- tabelas além do calendário (categorias, taxas) saem deformadas do MarkItDown;
- incisos numéricos (`1.`) e referências cruzadas no corpo do texto ("Art 11º") não são alterados.

## Revisão de 2026-10-18: `import-pdf.py` em PDFs de layout diferente do de 2014
A conversão dos regulamentos do CCOS de 2022 e de 2019 (issue #27) mostrou que o script, calibrado no layout de 2014, ainda deixava a saída fora do padrão do acervo em outros layouts. A escolha do MarkItDown permanece; o script passa a:
- **Timbre:** remover o nome da Federação só quando ele está sozinho na linha ou seguido do "Fundada em" do timbre (inclusive com o timbre inteiro em uma linha). No meio de uma frase, como no Art. 6º do CCOS 2022 ("filiado à FEDERAÇÃO CEARENSE DE ORIENTAÇÃO (FECORI)"), o nome é texto do regulamento e fica. Antes, o script o apagava.
- **Título:** juntar as linhas do título mesmo quando separadas por linha em branco. Isso encerra o limite "título partido por linhas em branco" da revisão anterior, e a edição passa a ser derivada do título.
- **Capítulo:** aceitar `10.DA SEGURANÇA`, sem espaço depois do ponto.
- **Linhas:** gravar cada artigo, parágrafo e alínea em uma linha só, com linha em branco entre eles, como no restante do acervo. Tabelas, calendário solto, assinatura, anexo, incisos numéricos e marcadores não são tocados, para não misturar conteúdo. O hífen de fim de linha só é fechado em sigla composta (`SI-` e `Card` viram `SI-Card`); nos demais casos a quebra fica, e o verificador aponta a palavra partida, porque só o PDF mostra se o hífen é da palavra.
- **Caracteres:** descartar o acento combinante U+0301 que o PDF deixa depois de vogal já acentuada (`será́`) e normalizar o ordinal `o` ou `°` em referência cruzada (`Art. 44o` vira `Art. 44º`).
- **Gravação:** usar LF em qualquer sistema, como o repositório (`.gitattributes`). No Windows o padrão gravaria CRLF.
- **Calendário:** continuar sem converter calendários de colunas separadas ou com células mescladas (CCOS 2019 e 2022), mas avisar na saída de erro, para o trecho não passar despercebido. A tabela se monta à mão contra o PDF.

A validação comparou a saída do script antigo e a do novo sobre os 23 PDFs de regulamento do acervo: nenhuma palavra mudou, fora o nome da Federação preservado nas frases, o timbre de 2018 antes deixado pela metade e a normalização de ordinais e capítulos. Sobre o CCOS 2022, o script reproduz o `.md` já revisado, exceto pela tabela do calendário.


