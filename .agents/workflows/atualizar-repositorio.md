---
description: Procedimento para levar uma mudança à main por PR — branch, verificação documental, apresentação ao usuário, PR, revisão, mesclagem autorizada e a exceção do contorno de admin, do usuário.
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

**Um tipo de caminho por PR.** O texto normativo (`Documentos/**/*.md`, `clubesCampeoes.md`) vai em branch e PR próprios; scripts, CI, ADRs, regras e workflows vão em outro. Basta um arquivo coberto pelo `CODEOWNERS` para o PR inteiro esperar a aprovação do dono, e separar evita que o atraso dela trave o que não precisa de revisão. Quando um PR depende do outro, mescle primeiro o que não espera aprovação.

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
> **Nunca** faça push direto à `main` nem execute o contorno de admin, e nunca mescle PR sem a autorização expressa do usuário. O agente não aprova PR.

## 6. Contorno de Admin (Exceção do Usuário)

Só quando o PR toca texto normativo, o outro dono do código está indisponível e o **usuário** decidiu não esperar. O agente não executa o contorno: informa que o PR está bloqueado pela falta da aprovação e entrega o comando.

1. **Motivo no PR, antes do contorno.** O comentário registra quem não aprovou, por que o contorno foi necessário e o pedido de revisão posterior. O agente pode redigi-lo e, com autorização do usuário, postá-lo:
   ```powershell
   gh pr comment <N> --body "Mesclado sem a aprovação de <dono>: <motivo>. Revisão posterior solicitada."
   ```
2. **Contorno pelo usuário**, no terminal dele, como administrador:
   ```powershell
   gh pr merge <N> --rebase --delete-branch --admin
   ```
3. **Revisão posterior.** O dono ausente revisa o que foi mesclado e registra o resultado em comentário no PR; se corrigir algo, a correção entra por novo PR.
4. Depois do contorno, o agente conclui a limpeza do passo 5 (`git switch main`, `git pull --ff-only`, `git fetch --prune`, `git branch -D <branch>`).

PR sem texto normativo (scripts, CI, `.agents/`) não precisa de contorno: não há aprovação a esperar.

## Checklist Rápido

- [ ] Branch `<escopo>/<N>-<resumo>` criado a partir da `main` atualizada, com texto normativo separado dos demais caminhos
- [ ] `python .agents/scripts/verificar-documentos.py` passou sem problemas
- [ ] Arquivos e mensagem de commit apresentados e autorizados pelo usuário
- [ ] PR aberto com `Refs #N` ou `Closes #N`; CI verde e aprovação exigida
- [ ] Mesclagem e exclusão de branches (remoto e local) autorizadas e executadas, e comentário de fechamento postado
- [ ] Se houve contorno de admin: motivo comentado no PR antes e revisão posterior do dono ausente registrada
