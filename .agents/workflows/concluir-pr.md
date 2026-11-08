---
description: Procedimento para concluir e mesclar um PR por rebase, sincronizar a main, podar o remoto e remover os branches locais e remotos.
---

# Workflow: Concluir PR, Rebasear e Limpar Branches

Este workflow detalha a etapa de conclusão do ciclo de PR de [`atualizar-repositorio.md`](atualizar-repositorio.md) e o *Fluxo por PR* de [`rules.md`](../rules/rules.md).

Após o desenvolvimento, a verificação documental e a aprovação no PR (pela equipe de regras em texto normativo, via CODEOWNERS), a incorporação na `main` é feita exclusivamente via *rebase*, seguida pela exclusão dos branches remoto e local para evitar acúmulo de referências órfãs.

## 1. Conferir Pré-requisitos do PR

Antes de solicitar a mesclagem:

1. **Status dos checks do CI:** o pipeline precisa estar totalmente verde.
2. **Aprovações necessárias:** para texto normativo, aprovação formal exigida em `.github/CODEOWNERS`.
3. **Autorização expressa do usuário:** o agente nunca mescla PR sem autorização prévia.

```powershell
gh pr view <N>
gh pr checks <N>
```

## 2. Mesclar com Rebase e Excluir o Branch Remoto

Com os checks verdes e autorização expressa:

```powershell
gh pr merge <N> --rebase --delete-branch
```

> [!NOTE]
> A flag `--rebase` preserva mensagens atômicas no padrão Conventional Commits sem criar commits de merge desnecessários. A flag `--delete-branch` remove automaticamente o branch no GitHub (`origin/<branch>`).

## 3. Sincronizar o Branch Principal Local (`main`)

Volte para a branch `main` e receba os commits rebaseados:

```powershell
git switch main
git pull --ff-only
```

## 4. Podar Referências Remotas e Deletar o Branch Local

Após a mesclagem por rebase, o branch remoto foi apagado e o branch local não é mais necessário.

1. **Podar referências remotas:**
   ```powershell
   git fetch --prune
   ```

2. **Excluir o branch local:**
   Como a mesclagem por *rebase* recalcula os hashes SHA dos commits ao aplicá-los sobre a `main`, o Git não reconhece o branch local como incorporado diretamente via `git branch -d`. Utilize `-D` para a exclusão segura:
   ```powershell
   git branch -D <branch>
   ```

3. **Limpeza opcional de outros branches locais já excluídos no remoto:**
   Para listar e remover branches locais cujas contrapartes remotas já foram deletadas (`[gone]`):
   ```powershell
   git branch -vv
   # Para remover cada branch com status [gone]:
   git branch -D <branch-antigo>
   ```

## 5. Fechamento de Issues e Pós-Mesclagem

Se o PR conclui ou referencia issues:

1. Verifique se a issue foi fechada automaticamente ou se precisa de fechamento manual.
2. Poste o comentário de resumo de fechamento conforme estabelecido no workflow de gestão de issues ([`gestao-issues.md`](gestao-issues.md), seção 4).
3. Verifique o estado final do repositório:
   ```powershell
   git status -sb
   python .agents/scripts/verificar-documentos.py
   ```

## Checklist Rápido

- [ ] `gh pr checks <N>` com CI verde e aprovações do CODEOWNERS concedidas
- [ ] Autorização expressa do usuário confirmada
- [ ] `gh pr merge <N> --rebase --delete-branch` executado
- [ ] `git switch main` e `git pull --ff-only` executados
- [ ] `git fetch --prune` executado
- [ ] `git branch -D <branch>` removido localmente
- [ ] Comentário de encerramento da issue postado (quando aplicável)
- [ ] Árvore limpa em `git status -sb` e `verificar-documentos.py` validado

