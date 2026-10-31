---
description: Decisão de manter cada edição em Documentos/<ano>/ desde a elaboração e de congelar o PDF publicado, com manifesto de hashes verificado localmente e no CI.
---

# ADR 006: Edições por Ano e Arquivos Publicados Congelados

> Registrada em 2026-10-31. Substitui a política "raiz = edição em trabalho; cópia em `Documentos/<ano>/` na virada" de [`rules.md`](../../rules/rules.md). Decidida na [*issue* #22](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/22) e implementada na [#31](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/31).

## Contexto
A raiz guardava a edição vigente ou em elaboração, e a cópia em `Documentos/<ano>/` só era criada quando a edição seguinte a superava. Isso gerou três problemas:

- **Duas edições valem ao mesmo tempo.** O regulamento de 2026 continua regendo a temporada em andamento enquanto o de 2027 é elaborado. O de 2026 estava em `Documentos/2026/` como `arquivado`, porque a verificação proibia outro status fora da raiz.
- **A cópia na virada falhou.** É um passo manual, e a ROP 2026 chegou a existir na raiz e em `Documentos/2026/`, byte a byte igual.
- **Nada protegia o que já foi publicado.** Era possível regenerar ou substituir o `.pdf` de uma edição já distribuída, que deve permanecer exatamente como foi publicado.

## Decisão
1. Toda edição vive em `Documentos/<ano>/` desde o início da elaboração. A raiz não guarda texto normativo; `clubesCampeoes.md`, que acumula todos os anos, continua nela.
2. O `status` do frontmatter do regulamento identifica a fase: no máximo uma edição `em-elaboracao`, exatamente uma `vigente` (a última publicada) e as demais `arquivado`. A ROP em uso é a do ano de `rop_referencia`.
3. Todo `.pdf` de `Documentos/<ano>/`, exceto o gerado do regulamento em elaboração, está congelado: o SHA-256 de cada PDF fica em `Documentos/arquivosCongelados.sha256`, no formato do `sha256sum`, e o manifesto só recebe linhas novas. O `.docx` é só intermediário da geração do PDF: não é congelado e sai da pasta na publicação, como já acontece no acervo.
4. A garantia tem três camadas:
   - o `gerar-documentos.py` recusa edição que não esteja em elaboração;
   - o `verificar-documentos.py` recusa arquivo congelado alterado, removido ou sem registro, e linha do manifesto alterada ou removida. Localmente, compara com o `HEAD`; no CI, com o commit anterior ao push ou com a base do PR;
   - o [`rules.md`](../../rules/rules.md) proíbe agentes de mexer nesses arquivos.
5. O `.md` de edição fechada só recebe correção de transcrição contra o PDF publicado; mudança normativa exige nova edição.

## Consequências
- **Positivas:**
  * Cada edição tem endereço estável, e a vigente e a em elaboração coexistem sem contradição de status.
  * Desaparece a cópia na virada: abrir uma edição é copiar o `.md` da vigente para a pasta do ano novo.
  * PDF publicado não muda sem que a verificação acuse, e qualquer pessoa confere com `sha256sum -c arquivosCongelados.sha256` dentro de `Documentos/`.
  * O ano deixa de ser fixo nos scripts e no CI: vem da pasta e do status.
- **Negativas/Atenção:**
  * Enquanto a `main` aceitar push direto ([#29](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/29)), o CI acusa a alteração depois do push, mas não a impede. A garantia só fica completa com a proteção da `main`.
  * Republicação oficial de um documento já congelado (uma errata da federação, por exemplo) não tem caminho previsto e exigirá decisão própria.
  * O `git log` de um único arquivo deixa de atravessar os anos. A comparação entre edições passa a ser feita entre pastas (`git diff --no-index`) ou pelas tags `v<ano>`.
  * Deixa de existir o link fixo para "a edição atual": o `README.md` aponta a vigente e a em elaboração e precisa ser atualizado a cada publicação.
  * O CI passa a baixar o histórico completo, hoje cerca de 40 MiB.
