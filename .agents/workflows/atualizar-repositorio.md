---
description: Procedimento para atualizar o repositório remoto — verificação documental, apresentação das alterações e push autorizado.
---

# Workflow: Atualizar Repositório Remoto

Este workflow define o procedimento obrigatório para sincronizar o repositório local com o remoto (GitHub). Mudança no `.md` do regulamento em elaboração não regenera `.docx` nem `.pdf`: os dois só são gerados na publicação da edição ([`publicar-edicao.md`](publicar-edicao.md)). Edição vigente ou arquivada nunca é regenerada: o `.pdf` dela está congelado.

## 1. Verificar os Documentos

Antes de propor o commit, execute a verificação documental (a mesma checagem que o CI executa). O commit só pode ser proposto se ela passar sem problemas:

```powershell
python .agents/scripts/verificar-documentos.py
```

## 2. Apresentar Alterações ao Usuário

Antes de solicitar autorização para o push, **apresente claramente** ao usuário:

1. A **lista exata** dos arquivos modificados que serão incluídos no commit.
2. A **mensagem de commit** proposta (seguindo Conventional Commits com escopo obrigatório).

```powershell
git status --short
```

## 3. Solicitar Autorização e Executar

Após a aprovação explícita do usuário, adicione **somente** os arquivos apresentados no passo 2 (nunca `git add -A`):

```powershell
git add <arquivos apresentados ao usuário>
git commit -m "<mensagem aprovada>"
git push origin main
```

> [!CAUTION]
> **Nunca** execute `git push` sem a autorização expressa do usuário. Esta é uma regra inegociável definida em `.agents/rules/rules.md`.

## Checklist Rápido

- [ ] `python .agents/scripts/verificar-documentos.py` passou sem problemas
- [ ] Apresentar arquivos modificados e mensagem de commit ao usuário
- [ ] Obter autorização expressa do usuário
- [ ] Executar `git add`, `git commit` e `git push`
