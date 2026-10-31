---
description: Procedimento para abrir uma nova edição em Documentos/<ano>/ e para publicá-la, congelando o PDF final.
---

# Workflow: Abrir e Publicar uma Edição

As regras ficam em *Organização dos Documentos*, de [`rules.md`](../rules/rules.md); a decisão, na [ADR-006](../wiki/decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md).

## 1. Abrir a edição do ano seguinte

1. Copie o `.md` da edição vigente para `Documentos/<ano novo>/`, com o mesmo nome.
2. No frontmatter da cópia, ajuste `ano`, `edicao` e `description` e ponha `status: em-elaboracao`. A `edicao` vem da numeração oficial, nunca de estimativa.
3. Atualize no [`README.md`](../../README.md) os *Documentos Principais* e a tabela do acervo.
4. Rode `python .agents/scripts/verificar-documentos.py`.

## 2. Publicar a edição em elaboração

Só com autorização expressa do usuário: depois deste passo, o `.pdf` não muda mais.

1. Confira que todas as *issues* do *milestone* "Regulamento `<ano>`" estão fechadas.
2. Gere os finais com a edição ainda em elaboração: `python .agents/scripts/gerar-documentos.py`.
3. No frontmatter, passe a edição publicada de `em-elaboracao` para `vigente` e a anterior de `vigente` para `arquivado`.
4. Congele o PDF: `python .agents/scripts/verificar-documentos.py --congelar`. O comando acrescenta ao `Documentos/arquivosCongelados.sha256` o `.pdf` da edição publicada e nunca altera linha existente. Remova o `.docx` da pasta com `git rm`: ele é intermediário e não fica no acervo.
5. Atualize o `README.md` e faça um único commit com tudo, seguindo [`atualizar-repositorio.md`](atualizar-repositorio.md).
6. Com autorização, crie a tag anotada no commit da publicação e envie-a: `git tag -a v<ano> -m "Edição <ano>"` e `git push origin v<ano>`.

## 3. Documento original novo

Um PDF original recebido depois (ROP da CBO, resultado de clubes) entra na pasta do seu ano e é congelado no mesmo commit, com `--congelar`.

## 4. Arquivo congelado alterado por engano

Se a verificação acusar "arquivo congelado foi alterado", restaure o original com `git checkout -- <arquivo>`. Nunca edite o manifesto para a verificação passar: a linha alterada também é acusada, localmente e no CI.
