---
description: Plano técnico para a conversão e padronização dos regulamentos
---

# Plano: Conversão e Padronização de Regulamentos Históricos

## Abordagem Técnica
Como os arquivos originais são PDFs, utilizaremos o navegador para abrir os arquivos e extrair o texto, ou tentaremos ler o conteúdo se o sistema permitir. Em seguida, aplicaremos a estrutura do modelo de 2026 (CCO).

## Fases de Implementação

### 1. Extração de Conteúdo
Para cada ano (2018, 2019, 2020, 2023, 2024, 2025):
1.  Localizar o arquivo PDF original em `Documentos/<ano>/Originais/`.
2.  Converter o PDF em Markdown usando PowerShell.

### 2. Formatação Markdown
Para cada texto extraído:
1.  Respeitar a estrutura e hierarquia original do arquivo.
2.  Formatar títulos de seções como `## <titulo do capitulo> `.
3.  Formatar artigos como `**Art. <N>º** – <Texto>`.
4.  Formatar parágrafos como citações `> **Paragrafo <N>º:** <Texto>`.
5.  Formatar incisos e alíneas com indentação superior `>> **<letra>.** <Texto>`.
6.  Converter tabelas de calendário para o formato Markdown.

### 3. Revisão e Validação
1.  Comparar o arquivo gerado com o PDF original para garantir que nenhuma regra foi perdida ou alterada.
2.  Garantir que o arquivo segue a estrutura e hierarquia original do arquivo.

## Decisões de Arquitetura
- **Armazenamento**: Os novos arquivos ficarão em `Documentos/<ano>/markdowns/regulamentoCCO_<ANO>.md`.

## Riscos e Mitigações
- **Erro na Extração de PDF**: Caracteres especiais podem vir quebrados. *Mitigação*: Revisão manual rigorosa após a conversão.
