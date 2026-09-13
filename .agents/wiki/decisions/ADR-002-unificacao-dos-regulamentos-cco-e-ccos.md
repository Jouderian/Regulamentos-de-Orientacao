---
description: Decisão de unificar os regulamentos do CCO e do CCOS em um documento único a partir da edição de 2026.
---

# ADR 002: Unificação dos Regulamentos do CCO e do CCOS

> Registrada retroativamente em 2026-09-13, formalizando a decisão implementada na edição de 2026.

## Contexto
Até 2025, CCO e CCOS tinham regulamentos separados. A análise comparativa registrada em [`unified-regulations/plan.md`](../../specs/unified-regulations/plan.md) mostrou que a maior parte do texto era idêntica entre os dois: filiação, categorias, inscrições, a lista de motivos de desclassificação (alíneas *a* a *p*), reclamações e protestos, júri técnico, segurança, tabela de pontuação e critérios de desempate.

Manter dois documentos com o mesmo conteúdo significava corrigir cada regra duas vezes — e conviver com o risco de divergência silenciosa entre eles, em que uma correção entrava em um regulamento e não no outro.

## Decisão
A partir da edição de **2026**, CCO e CCOS passam a ser regidos por um documento unificado, `regulamentoDasCompeticoesCearenses.md`, organizado por assunto e não por competição.

1. As regras comuns são redigidas uma única vez.
2. As diferenças entre as competições ficam explícitas no próprio artigo, marcadas como **Exclusivo do CCO** ou **Exclusivo do CCOS** (ex.: a regra de descarte do Art. 34, exclusiva do CCO).
3. Calendário, extensão de percurso e requisitos de organização continuam separados por competição, em seções próprias.
4. Os regulamentos separados de 2025 e anteriores permanecem intactos no acervo — a unificação vale da edição de 2026 em diante e não é retroativa.

## Consequências
- **Positivas:**
  * Uma correção de redação passa a ser feita em um lugar só.
  * As diferenças reais entre as duas competições ficam visíveis lado a lado, em vez de exigirem a leitura comparada de dois documentos.
  * Reduz pela metade o esforço de revisão a cada ciclo anual.
- **Negativas/Atenção:**
  * O atleta que compete em apenas uma das modalidades lê um documento maior, com artigos que não se aplicam a ele — daí a necessidade das marcações de exclusividade serem inequívocas.
  * A comparação com edições anteriores a 2026 deixa de ser um `diff` direto, já que a estrutura mudou.
  * Um artigo sem marcação de exclusividade vale para ambas as competições; a ausência da marca é, portanto, uma decisão normativa e não um esquecimento de formatação.
