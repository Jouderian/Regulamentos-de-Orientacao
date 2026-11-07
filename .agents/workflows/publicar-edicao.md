---
description: Procedimento para abrir uma nova edição em Documentos/<ano>/ e para publicá-la, congelando o PDF final.
---

# Workflow: Abrir e Publicar uma Edição

As regras ficam em *Organização dos Documentos*, de [`rules.md`](../rules/rules.md); a decisão, na [ADR-006](../wiki/decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md).

## 1. Abrir a edição do ano seguinte

1. Copie o `.md` da edição vigente para `Documentos/<ano novo>/`, com o mesmo nome.
2. No frontmatter da cópia, ajuste `ano`, `edicao` e `description` e ponha `status: em-elaboracao`. A `edicao` vem da numeração oficial, nunca de estimativa: ano sem campeonato realizado não consome número ([Numeração das edições](../wiki/numeracao-das-edicoes.md)).
3. Atualize no [`README.md`](../../README.md) a seção *Próxima edição*.
4. Rode `python .agents/scripts/verificar-documentos.py`.

## 2. Publicar a edição em elaboração

Só com autorização expressa do usuário: depois deste passo, o `.pdf` não muda mais.

1. Confira que todas as *issues* do *milestone* "Regulamento `<ano>`" estão fechadas.
2. Gere o `.docx` e o `.pdf` com a edição ainda em elaboração: `python .agents/scripts/gerar-documentos.py`. É a primeira vez que eles existem: durante a elaboração, o regulamento é só `.md`.
3. Revise o `.docx` com a equipe de regras. Toda correção de texto vai para o `.md`, e o script é rodado de novo; no `.docx` só se faz ajuste de diagramação, e o `.pdf` é então exportado dele pelo Word ([`geracao-documentos.md`](geracao-documentos.md), passo 4.2). Assim o `.md` e o PDF publicado não divergem.
4. Assine digitalmente o `.pdf`.
5. No frontmatter, passe a edição publicada de `em-elaboracao` para `vigente` e a anterior de `vigente` para `arquivado`.
6. Congele o PDF assinado: `python .agents/scripts/verificar-documentos.py --congelar`. O comando acrescenta ao `Documentos/arquivosCongelados.sha256` o `.pdf` do regulamento estadual publicado e nunca altera linha existente. Apague o `.docx` da pasta: ele é intermediário, não fica no acervo, e a verificação o recusa.
7. Atualize no `README.md` as seções *Regulamento em vigor*, *Próxima edição* e *Edições anteriores* e faça um único commit com tudo, seguindo [`atualizar-repositorio.md`](atualizar-repositorio.md).
8. Com autorização, crie a tag anotada no commit da publicação e envie-a: `git tag -a v<ano> -m "Edição <ano>"` e `git push origin v<ano>`.

## 3. Documento original novo

- **ROP publicada pela CBO:** entra na pasta do seu ano e é congelada no mesmo commit, com `--congelar`.
- **Minuta da ROP:** fica com `status: em-elaboracao` no `.md` e não é congelada. Quando a CBO publicar a versão definitiva, substitua o `.pdf` e o `.md` pelos oficiais, retire o `status` do frontmatter e congele com `--congelar` no mesmo commit.
- **Resultado de clubes:** entra na pasta do seu ano e não é congelado.

## 4. Arquivo congelado alterado por engano

Se a verificação acusar "arquivo congelado foi alterado", restaure o original com `git checkout -- <arquivo>`. Nunca edite o manifesto para a verificação passar: a linha alterada também é acusada, localmente e no CI.
