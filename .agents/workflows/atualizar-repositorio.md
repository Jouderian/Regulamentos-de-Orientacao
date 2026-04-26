---
description: Procedimento para atualizar o repositório remoto, incluindo regeneração automática dos documentos finais (.docx e .pdf) quando o Markdown fonte tiver sido modificado.
---

# Workflow: Atualizar Repositório Remoto

Este workflow define o procedimento obrigatório para sincronizar o repositório local com o remoto (GitHub). Antes do push, o agente **deve** verificar se o arquivo `regulamentoCompeticoesCearenses.md` foi alterado e, em caso afirmativo, regenerar os documentos finais.

## 1. Verificar Alterações no Markdown

Antes de qualquer operação de commit, verifique se o arquivo `regulamentoCompeticoesCearenses.md` sofreu alterações desde o último commit:

```powershell
git diff --name-only HEAD -- regulamentoCompeticoesCearenses.md
```

Se o arquivo **aparecer na lista** (ou se for um arquivo novo/não rastreado), o passo 2 é **obrigatório**.

Se o arquivo **não aparecer**, pule diretamente para o passo 3.

## 2. Regenerar Documentos Finais (.docx e .pdf)

Execute o workflow [`/geracao-documentos`](.agents/workflows/geracao-documentos.md) (passos 3 e 4) para regenerar o `.docx` e o `.pdf`.

## 3. Apresentar Alterações ao Usuário

Antes de solicitar autorização para o push, **apresente claramente** ao usuário:

1. A **lista exata** dos arquivos modificados que serão incluídos no commit.
2. A **mensagem de commit** proposta (seguindo Conventional Commits com escopo obrigatório).

```powershell
# // turbo
git status --short
```

## 4. Solicitar Autorização e Executar

Após a aprovação explícita do usuário:

```powershell
git add -A
git commit -m "<mensagem aprovada>"
git push origin main
```

> [!CAUTION]
> **Nunca** execute `git push` sem a autorização expressa do usuário. Esta é uma regra inegociável definida em `.agents/rules/rules.md`.

## Checklist Rápido

- [ ] `regulamentoCompeticoesCearenses.md` alterado? → Regenerar `.docx` e `.pdf`
- [ ] Apresentar arquivos modificados e mensagem de commit ao usuário
- [ ] Obter autorização expressa do usuário
- [ ] Executar `git add`, `git commit` e `git push`
