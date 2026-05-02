---
description: Conversão para markdown dos regulamentos históricos (2018-2025)
---

# Especificação: Conversão de Regulamentos Históricos (2018-2025)

## Contexto
Os regulamentos dos anos anteriores (2018 a 2025) estão em formato PDF e "desorganizados" em relação ao modelo de 2026. O objetivo é padronizar todos os regulamentos de 2018 a 2025 para o formato Markdown, seguindo rigorosamente a estrutura, hierarquia e estilo visual do modelo do projeto.

## Objetivo
Converter os regulamentos de 2018 a 2025 para o formato Markdown, seguindo rigorosamente a estrutura, hierarquia e estilo visual do modelo do projeto (2026).

## Requisitos
1.  **Formato**: Todos os arquivos finais devem ser `.md`.
2.  **Estrutura**: Seguir a hierarquia de Capítulos, Artigos, Parágrafos, Incisos e Alíneas conforme o modelo do projeto.
3.  **Localização**: Os arquivos convertidos devem ser salvos em suas respectivas pastas de ano dentro de `Documentos/<ano>/markdowns`.
4.  **Nomenclatura**: Os arquivos devem ser nomeados como `regulamento<competicao>_<ano>.md`.
5.  **Conteúdo**: Preservar o conteúdo original de cada ano, mas adaptar a formatação Markdown (negritos, citações para parágrafos, tabelas para calendários, etc.).
6.  **Idioma**: Português do Brasil (pt-BR).

## Critérios de Aceitação
- [ ] Arquivo `regulamentoCCO_2018.md` criado e padronizado.
- [ ] Arquivo `regulamentoCCO_2019.md` criado e padronizado.
- [ ] Arquivo `regulamentoCCO_2020.md` criado e padronizado.
- [ ] Arquivo `regulamentoCCO_2023.md` criado e padronizado.
- [ ] Arquivo `regulamentoCCO_2024.md` criado e padronizado.
- [ ] Arquivo `regulamentoCCO_2025.md` criado e padronizado.
- [ ] Todos os arquivos seguem o estilo visual (citações para parágrafos, tabelas, etc.) do modelo de 2026.

## Passo a Passo
1.  Analisar o arquivo PDF do regulamento do ano especificado
2.  Identificar a estrutura do regulamento (capítulos, artigos, parágrafos, incisos, alíneas)
3.  Criar um arquivo Markdown com a estrutura identificada na pasta `Documentos/<ano>/markdowns
4.  Preencher o arquivo Markdown com o conteúdo do regulamento
5.  Salvar o arquivo no formato especificado
6.  Verificar se o arquivo segue todos os critérios de aceitação
