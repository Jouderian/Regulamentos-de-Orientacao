---
description: Procedimento para atualizar o repositório remoto, incluindo regeneração automática dos documentos finais (.docx e .pdf) quando o Markdown fonte tiver sido modificado.
---

# Workflow: Atualizar Repositório Remoto

Este workflow define o procedimento obrigatório para sincronizar o repositório local com o remoto (GitHub). Antes do push, o agente **deve** verificar se o regulamento em elaboração foi alterado e, em caso afirmativo, regenerar os documentos finais. Edição vigente ou arquivada nunca é regenerada: o `.pdf` dela está congelado.

## 1. Verificar Alterações no Markdown

Antes de qualquer operação de commit, verifique se algum regulamento sofreu alterações desde o último commit:

```powershell
git diff --name-only HEAD -- 'Documentos/*/regulamentoDasCompeticoesCearenses.md'
```

Se aparecer o regulamento da edição **em elaboração** (ou se for um arquivo novo/não rastreado), o passo 2 é **obrigatório**. Se aparecer o de uma edição vigente ou arquivada, só cabe correção de transcrição no `.md`, e o passo 2 não se aplica.

Se o arquivo **não aparecer**, pule diretamente para o passo 3.

## 2. Regenerar Documentos Finais (.docx e .pdf)

Execute o workflow [`/geracao-documentos`](geracao-documentos.md) (passo 3) para regenerar o `.docx` e o `.pdf`.

## 3. Verificar os Documentos

Antes de propor o commit, execute a verificação documental (a mesma checagem que o CI executa). O commit só pode ser proposto se ela passar sem problemas:

```powershell
python .agents/scripts/verificar-documentos.py
```

## 4. Apresentar Alterações ao Usuário

Antes de solicitar autorização para o push, **apresente claramente** ao usuário:

1. A **lista exata** dos arquivos modificados que serão incluídos no commit.
2. A **mensagem de commit** proposta (seguindo Conventional Commits com escopo obrigatório).

```powershell
git status --short
```

## 5. Solicitar Autorização e Executar

Após a aprovação explícita do usuário, adicione **somente** os arquivos apresentados no passo 4 (nunca `git add -A`):

```powershell
git add <arquivos apresentados ao usuário>
git commit -m "<mensagem aprovada>"
git push origin main
```

> [!CAUTION]
> **Nunca** execute `git push` sem a autorização expressa do usuário. Esta é uma regra inegociável definida em `.agents/rules/rules.md`.

## Checklist Rápido

- [ ] Regulamento em elaboração alterado? → Regenerar `.docx` e `.pdf` (edição fechada, nunca)
- [ ] `python .agents/scripts/verificar-documentos.py` passou sem problemas
- [ ] Apresentar arquivos modificados e mensagem de commit ao usuário
- [ ] Obter autorização expressa do usuário
- [ ] Executar `git add`, `git commit` e `git push`
