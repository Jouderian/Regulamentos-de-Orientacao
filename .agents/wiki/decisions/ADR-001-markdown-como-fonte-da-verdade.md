---
description: Decisão de adotar o Markdown como fonte da verdade dos regulamentos, com Word e PDF como saídas geradas.
---

# ADR 001: Markdown como Fonte da Verdade

> Registrada retroativamente em 2026-09-13, formalizando a decisão que originou o repositório.

## Contexto
Os regulamentos do CCO e do CCOS eram mantidos em arquivos Word e distribuídos em PDF. Esse formato tornava impossível responder com precisão a perguntas básicas de governança normativa: o que exatamente mudou entre duas edições, quem alterou, quando e por quê. Cada revisão circulava como um anexo novo, sem histórico e sem garantia de que a cópia em mãos era a vigente.

## Decisão
O **Markdown** passa a ser a fonte da verdade dos regulamentos. Os arquivos `.docx` e `.pdf` são **saídas geradas** a partir dele, nunca documentos editáveis.

1. Toda adição, edição ou revogação de regra ocorre exclusivamente nos arquivos `.md`.
2. Edições feitas diretamente no Word ou no PDF **não são oficiais** e serão sobrescritas na próxima geração.
3. A geração dos documentos finais segue o workflow [`geracao-documentos.md`](../../workflows/geracao-documentos.md): Pandoc aplica `Documentos/template_estilos.docx` para preservar a identidade visual da Federação, e o PDF é produzido a partir do `.docx`.
4. A regeneração dos documentos finais é obrigatória sempre que o Markdown vigente muda, antes do commit.

## Consequências
- **Positivas:**
  * O histórico de cada regra passa a ser rastreável commit a commit (`git log -p`), atendendo à exigência de auditabilidade do [project-vision](../../specs/project-vision/spec.md).
  * A comparação entre edições vira um `diff`, em vez de leitura lado a lado de dois PDFs.
  * O texto estruturado é consumível por IAs, um dos públicos-alvo declarados do projeto.
  * A identidade visual não se perde, pois vive no template, separada do conteúdo.
- **Negativas/Atenção:**
  * Exige Pandoc e Microsoft Word (via COM, no Windows) na máquina de quem publica.
  * Cria o risco de o `.docx`/`.pdf` publicado divergir do Markdown se a regeneração for esquecida — mitigado pela regra de regeneração obrigatória em [`rules.md`](../../rules/rules.md).
  * Quem edita precisa conhecer a convenção tipográfica do projeto, descrita na [ADR-003](ADR-003-historical-regulation-standardization.md).
