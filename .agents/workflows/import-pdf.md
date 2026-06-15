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

Para simplificar a conversão e aplicar as regras de formatação jurídica (Capítulos, Artigos, Parágrafos e Incisos), utilize o script automatizado [.agents/scripts/import-pdf.py](../../scripts/import-pdf.py).

### Comando de Conversão
Execute o script passando o caminho do PDF de entrada e, opcionalmente, o caminho do Markdown de saída:

```bash
python .agents/scripts/import-pdf.py <caminho_do_pdf> [caminho_do_markdown_saida]
```

**Exemplo:**
```bash
python .agents/scripts/import-pdf.py Documentos/2026/regulamentoDasCompeticoesCearenses.pdf regulamentoTeste.md
```

Este script executará as seguintes tarefas automaticamente:
1. Extração do conteúdo do PDF mantendo a fidelidade das tabelas nativas do Markdown.
2. Aplicação de Expressões Regulares (Regex) para formatar a tipografia jurídica do projeto.

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