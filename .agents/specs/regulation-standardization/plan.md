---
description: Plano técnico e padrão tipográfico para a conversão dos regulamentos históricos
---

# Plano: Conversão e Padronização de Regulamentos Históricos

## Abordagem Técnica
A extração é feita pelo script [`import-pdf.py`](../../scripts/import-pdf.py), que usa a biblioteca **MarkItDown** e aplica automaticamente as regras tipográficas descritas abaixo. As alternativas de contingência (`pdftotext -layout` e a rota PDF → DOCX → Pandoc) e o porquê dessa escolha estão registrados na [ADR-003](../../wiki/decisions/ADR-003-historical-regulation-standardization.md).

## Fases de Implementação

### 1. Extração
```bash
python .agents/scripts/import-pdf.py Documentos/<ano>/regulamentoCCO.pdf
```
O Markdown é gravado ao lado do PDF, com o mesmo nome-base.

### 2. Padrão Tipográfico
| Elemento | Formato |
| :--- | :--- |
| Título do documento | `# Regulamento do <N> Campeonato Cearense de Orientação` |
| Capítulo/Seção | `## <N>. <Título do capítulo>` |
| Artigo | `**Art. <N>º** – <Texto>` |
| Parágrafo numerado | `> **Parágrafo <N>º:** <Texto>` |
| Parágrafo único | `> **Parágrafo Único:** <Texto>` |
| Alínea/Inciso | `>> **<letra>.** <Texto>` |
| Calendário de etapas | tabela Markdown nativa (`\|---\|`) |

O travessão do artigo é o **en dash** (`–`, U+2013), não o hífen. O indicador ordinal é `º` (U+00BA), não a letra `o`.

### 3. Revisão Manual
Obrigatória mesmo com o script. Revisar os itens listados no workflow [`import-pdf.md`](../../workflows/import-pdf.md) e confrontar o resultado com o PDF original artigo a artigo.

### 4. Validação
```bash
python .agents/scripts/verificar-documentos.py
```
A verificação recusa artefatos de conversão (U+00AD, BOM, U+00A0, palavras partidas por hifenização, `Paragrafo` sem acento, ordinais grafados `1o`) e artigos fora do padrão. É a mesma checagem executada pelo CI.

## Decisões de Armazenamento
- O `.md` fica em `Documentos/<ano>/`, ao lado do PDF de origem, com o mesmo nome-base.
- O regulamento **vigente** fica na raiz do repositório; a cópia em `Documentos/<ano>/` é criada quando a edição é superada pela seguinte.

## Riscos e Mitigações
| Risco | Mitigação |
| :--- | :--- |
| Extração quebra acentos e junta/parte palavras | Revisão manual + verificação automatizada bloqueando o commit |
| Tabela de calendário deformada | Conferência visual contra o PDF; a verificação não detecta colunas trocadas |
| Alteração involuntária do conteúdo normativo | Comparação artigo a artigo com o PDF antes do commit |
| PDF antigo sem camada de texto | `pip install markitdown-ocr` e revisão reforçada |
