---
description: Especificação para unificação dos regulamentos dos campeonatos cearenses (CCO e CCOS)
---

# Especificação: Regulamento Unificado (CCO e CCOS)

## Contexto
Anteriormente, o Campeonato Cearense de Orientação (CCO) e o Campeonato Cearense de Orientação Sprint (CCOS) possuíam regulamentos separados publicados a cada ano. Como grande parte dos dispositivos normativos (inscrições, segurança, infrações, desclassificações, recursos e responsabilidades) eram idênticos, a manutenção em arquivos distintos gerava redundância e risco de divergência não intencional entre textos.

## Objetivo
Unificar os regulamentos das duas competições em um único documento normativo (`regulamentoDasCompeticoesCearenses.md`), consolidando as regras comuns e delimitando com precisão as especificidades técnicas, esportivas e logísticas de cada modalidade.

## Requisitos
1. **Estrutura Unificada**: Consolidar as normas administrativas e comuns (Capítulos 1, 4, 6 e 7) e manter seções ou marcações explícitas onde houver regras distintas para CCO e CCOS (Capítulos 2, 3 e 5).
2. **Especificidades Preservadas**:
   - **CCO**: Múltiplas etapas ao longo do ano, proibição de áreas mapeadas nos últimos 3 anos, uniforme com mangas e caneleira recomendados, ordem de partida padrão CBO e descarte de etapas (quando houver mais de 3 etapas realizadas).
   - **CCOS**: Evento único em fim de semana com múltiplos percursos, uniforme leve permitido (com número de peito fixado), ordem inversa de partida no último percurso e categorias acompanhadas restritas ao último percurso.
3. **Premiação**: Atletas recebem medalhas e clubes disputam troféus gerais em ambas as competições.
4. **Formato**: Markdown codificado em UTF-8 sem BOM, tipografia jurídica alinhada à [ADR-003](../../wiki/decisions/ADR-003-historical-regulation-standardization.md) e metadados frontmatter obrigatórios.
5. **Localização**: O documento vigente é mantido na raiz do repositório como `regulamentoDasCompeticoesCearenses.md`.

## Critérios de Aceitação
- [x] O regulamento unificado substitui os arquivos separados e reside na raiz em `regulamentoDasCompeticoesCearenses.md`.
- [x] Contempla regras comuns e disposições específicas devidamente demarcadas para CCO e CCOS.
- [x] Estrutura padronizada em capítulos, artigos, parágrafos, incisos e alíneas conforme a tipografia jurídica do projeto.
- [x] Aprovado e validado pela verificação documental automatizada (`python .agents/scripts/verificar-documentos.py`).
