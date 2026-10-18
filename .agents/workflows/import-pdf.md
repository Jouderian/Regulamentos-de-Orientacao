---
description: Guia de importação e conversão de PDFs de regulamentos em Markdown usando MarkItDown.
---

# Workflow: Importação de Regulamentos em PDF para Markdown

Este guia descreve o procedimento operacional para converter novos regulamentos oficiais (geralmente distribuídos em PDF, como a ROP nacional da CBO) em arquivos Markdown limpos e padronizados com a tipografia jurídica adotada pelo projeto.

---

## 1. Instalação e Preparação

O processo automatizado depende de **Python (versão 3.9 ou superior)**.

### Instalar Dependências
Navegue até a raiz do projeto e execute o comando abaixo para instalar o Microsoft **MarkItDown** e suas extensões para PDF:

```bash
pip install -r .agents/requirements.txt
```

> [!NOTE]
> Se você precisar converter arquivos que requerem reconhecimento óptico de caracteres (OCR) — como PDFs escaneados que não possuem camada de texto selecionável —, instale também a extensão de OCR do MarkItDown:
> `pip install markitdown-ocr`

---

## 2. Execução Automatizada

Para simplificar a conversão e aplicar as regras de formatação jurídica (Capítulos, Artigos, Parágrafos e Incisos), utilize o script automatizado [.agents/scripts/import-pdf.py](../scripts/import-pdf.py).

### Comando de Conversão
Execute o script passando o caminho do PDF de entrada e, opcionalmente, o caminho do Markdown de saída:

```bash
python .agents/scripts/import-pdf.py <caminho_do_pdf> [caminho_do_markdown_saida]
```

**Exemplo:**
```bash
python .agents/scripts/import-pdf.py Documentos/2014/regulamentoCCO.pdf regulamentoTeste.md
```

Este script executará as seguintes tarefas automaticamente:
1. Extração do conteúdo do PDF mantendo a fidelidade das tabelas nativas do Markdown.
2. Limpeza do timbre da Federação, dos rodapés e das letras duplicadas do negrito simulado (`RREEGGUULLAAMMEENNTTOO`).
3. Aplicação de Expressões Regulares (Regex) para formatar a tipografia jurídica do projeto: título, capítulos numerados (`## 1. DA ...`), artigos (ordinal até o 9º, cardinal do 10 em diante), `Parágrafo Único`, parágrafos numerados, alíneas (`>> **a.**`) e o calendário de etapas em tabela.
4. Junção das linhas de cada artigo, parágrafo e alínea em uma linha só, com linha em branco entre eles, e correção do acento combinante (`será́`) e do ordinal `44o` nas referências.
5. Geração do frontmatter exigido pelo verificador (`ano`, `edicao`, `status: arquivado`, `rop_referencia`, `description`).

O arquivo sai com LF. Se o calendário de etapas não virar tabela (colunas em linhas separadas, célula mesclada), o script grava o arquivo e avisa na saída de erro; a tabela se monta à mão, como na [ADR-003](../wiki/decisions/ADR-003-historical-regulation-standardization.md).

### Opções
| Opção | Quando usar |
| :--- | :--- |
| `--ano <AAAA>` | PDF fora de uma pasta `Documentos/<ano>/` (o ano normalmente vem da pasta) |
| `--edicao "<N> CCO"` | O título do PDF não traz o numeral romano da edição, ou o layout é diferente do de 2014 (ex.: `"XIII CCO"`, `"VII CCOS"`) |
| `--rop-referencia <AAAA>` | A ROP citada não é a do próprio ano (padrão: o ano da edição) |
| `--sem-frontmatter` | Documento que não é regulamento de competição |

Ano e edição não são estimados: se não houver origem identificável e a opção não for dada, o script para sem gravar o arquivo.

---

## 3. Conversão Manual Alternativa (CLI Direta)

Se preferir não usar o script customizado ou precisar fazer uma conversão direta sem filtros prévios, você pode usar a CLI nativa do MarkItDown:

```bash
markitdown caminho/para/regulamento.pdf > saida.md
```

> [!WARNING]
> Ao utilizar a CLI direta, as formatações jurídicas (como a estilização de Capítulos e Artigos) não serão aplicadas. Você precisará revisar e formatar manualmente seguindo os padrões definidos na [ADR 003](../wiki/decisions/ADR-003-historical-regulation-standardization.md).

---

## 4. Revisão Manual (Obrigatório)

Mesmo utilizando o script automatizado, a conversão de PDFs pode gerar pequenas imperfeições. Sempre realize uma verificação manual das seguintes seções após a conversão:

1. **Cabeçalhos e Rodapés:** Remova números de páginas, títulos repetidos de topo e notas de rodapé que foram extraídos no meio do texto das páginas.
2. **Tabelas:** O MarkItDown extrai tabelas de forma estruturada, mas verifique se não há distorção de colunas ou células mescladas incorretamente.
3. **Quebras de Linha Hifenizadas:** Palavras hifenizadas no final da linha do PDF original podem ser salvas com o hífen incorreto (ex: `orien- tação` em vez de `orientação`). Faça uma rápida busca no texto.
4. **Layout de outros anos:** as heurísticas foram calibradas nos PDFs de 2014, 2019 e 2022. Em PDFs de outros anos, confira se o título virou `# Regulamento do ...`, se todos os artigos viraram `**Art. N** –` (o número pode vir isolado na linha) e se o calendário virou tabela. Quando o script avisar que não virou, monte a tabela contra o PDF; célula mesclada (um árbitro para duas etapas) se repete em cada linha.
5. **Palavra partida no fim da linha:** o script só fecha o hífen de sigla composta (`SI-Card`). Os demais hifens de fim de linha ficam, e o `verificar-documentos.py` aponta a palavra partida: confira no PDF se o hífen é da palavra.
6. **Tabelas e incisos:** só o calendário é convertido em tabela pelo script. Tabelas de categorias e de taxas costumam sair deformadas do MarkItDown, e incisos numéricos (`1.`) e referências cruzadas no texto ("Art 11º") não são alterados: ajuste à mão.