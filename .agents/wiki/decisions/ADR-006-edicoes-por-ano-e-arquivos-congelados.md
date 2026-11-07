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

## Revisão de 2026-11-06

- **Congelamento restrito aos documentos oficiais publicados.** São congelados o `.pdf` do regulamento estadual (CCO, CCOS ou unificado) de edição fechada, assinado digitalmente, e o `.pdf` da ROP publicada pela CBO. Os resultados de clubes saem do manifesto, que cai de 54 para 39 linhas; a linha de PDF congelado continua imutável, e o `verificar-documentos.py` recusa linha de PDF que não se congela.
- **Duas elaborações simultâneas.** O regulamento estadual e a ROP do ano seguinte podem estar `em-elaboracao` ao mesmo tempo, no máximo um de cada. A minuta da ROP se marca com `status` no frontmatter, fica livre enquanto em elaboração e é congelada quando a CBO publicar a versão definitiva.
- **Consequência:** a substituição da minuta da ROP pela definitiva deixa de exigir decisão própria, mas uma troca indevida do PDF de um resultado de clubes passa a não ser acusada pela verificação; a proteção dele fica no histórico do Git.

## Revisão de 2026-11-07

Decidida e implementada na [*issue* #34](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/34); substitui a parte do item 3 que mantinha `.docx` e `.pdf` do regulamento em elaboração na pasta do ano.

- **O regulamento em elaboração existe só como `.md`.** O `.docx` é gerado no fechamento, para revisão; o `.pdf` vem do `.docx` revisado e é assinado digitalmente. Regenerar os dois a cada mudança no `.md` enchia o histórico de diffs binários de arquivos sem uso antes da publicação.
- **Na revisão do fechamento,** correção de texto vai para o `.md` e o `.docx` é regenerado; no `.docx` só se faz ajuste de diagramação. Assim o `.md` e o PDF publicado não divergem.
- **O `verificar-documentos.py` recusa** `.docx` em `Documentos/<ano>/` e `.pdf` de regulamento em elaboração. A minuta da ROP, fornecida pela CBO, continua com `.pdf`.
- **O job `gerar-docx` do CI** continua gerando o `.docx` como artefato da execução, sem versioná-lo: detecta conversão quebrada e serve de prévia. A comparação com um `.docx` versionado ([#18](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/18)) perde o objeto.
- **Consequência:** entre a geração e o commit da publicação, a verificação local acusa o `.docx` e o `.pdf` ainda em elaboração; ela só passa depois da troca de status e da remoção do `.docx` (passos 5 e 6 de [`publicar-edicao.md`](../../workflows/publicar-edicao.md)).
