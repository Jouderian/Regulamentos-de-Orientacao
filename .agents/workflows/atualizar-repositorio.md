---
description: Procedimento para levar uma mudança à main por PR — branch, verificação documental, apresentação ao usuário, PR, revisão e mesclagem autorizada.
---

# Workflow: Atualizar Repositório Remoto

Este workflow detalha o *Fluxo por PR* de [`rules.md`](../rules/rules.md). A `main` é protegida: só recebe mudança por PR, com o CI verde, e o PR que toca texto normativo precisa da aprovação da equipe de regras, definida em [`.github/CODEOWNERS`](../../.github/CODEOWNERS) ([ADR-005](../wiki/decisions/ADR-005-controle-de-pendencias-por-issues.md), revisão de 2026-11-07).

Mudança no `.md` do regulamento em elaboração não regenera `.docx` nem `.pdf`: os dois só são gerados na publicação da edição ([`publicar-edicao.md`](publicar-edicao.md)). Edição vigente ou arquivada nunca é regenerada: o `.pdf` dela está congelado.

## 1. Criar o Branch

Parta da `main` atualizada. O nome do branch é `<escopo>/<N>-<resumo>`, com o escopo do commit e o número da *issue*:

```powershell
git switch main
git pull
git switch -c ci/29-revisao-por-pr
```

## 2. Verificar os Documentos

Antes de propor o commit, execute a verificação documental (a mesma checagem que o CI executa). O commit só pode ser proposto se ela passar sem problemas:

```powershell
python .agents/scripts/verificar-documentos.py
```

## 3. Apresentar Alterações ao Usuário

Antes de pedir autorização, **apresente claramente** ao usuário:

1. A **lista exata** dos arquivos modificados que serão incluídos no commit.
2. A **mensagem de commit** proposta (seguindo Conventional Commits com escopo obrigatório).

```powershell
git status --short
```

## 4. Commitar, Enviar o Branch e Abrir o PR

Após a aprovação explícita do usuário, adicione **somente** os arquivos apresentados no passo 3 (nunca `git add -A`):

```powershell
git add <arquivos apresentados ao usuário>
git commit -m "<mensagem aprovada>"
git push -u origin <branch>
gh pr create --title "<mensagem aprovada, primeira linha>" --body-file <arquivo>
```

O corpo do PR segue [`.github/pull_request_template.md`](../../.github/pull_request_template.md) e leva `Refs #N` ou `Closes #N`. Se o PR toca texto normativo, o GitHub pede a revisão da equipe de regras automaticamente.

## 5. Mesclar e Limpar Branches

Com o CI verde, a aprovação exigida e a autorização expressa do usuário:

```powershell
gh pr checks <N>
gh pr merge <N> --rebase --delete-branch
git switch main
git pull --ff-only
git fetch --prune
git branch -D <branch>
```

A mesclagem por *rebase* preserva cada commit com a mensagem em Conventional Commits, e `--delete-branch` remove o branch remoto no GitHub. O `git branch -D <branch>` conclui a limpeza local (detalhes no passo a passo [`concluir-pr.md`](concluir-pr.md)). Se o PR fecha uma *issue*, poste o comentário de fechamento ([`gestao-issues.md`](gestao-issues.md), seção 4) logo depois.

> [!CAUTION]
> **Nunca** faça push direto à `main` nem use o contorno de admin, e nunca mescle PR sem a autorização expressa do usuário. O agente não aprova PR.

## Checklist Rápido

- [ ] Branch `<escopo>/<N>-<resumo>` criado a partir da `main` atualizada
- [ ] `python .agents/scripts/verificar-documentos.py` passou sem problemas
- [ ] Arquivos e mensagem de commit apresentados e autorizados pelo usuário
- [ ] PR aberto com `Refs #N` ou `Closes #N`; CI verde e aprovação exigida
- [ ] Mesclagem e exclusão de branches (remoto e local) autorizadas e executadas, e comentário de fechamento postado
