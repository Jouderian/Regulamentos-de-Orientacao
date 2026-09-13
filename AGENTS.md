# Regulamentos de Orientação — Instruções para Agentes

Este repositório é mantido com apoio de agentes de IA de mais de uma ferramenta. Para que a regra valha igual em todas, ela vive em **um único arquivo canônico**:

> **[`.agents/rules/rules.md`](.agents/rules/rules.md) — leia por inteiro antes de qualquer tarefa.**

Não duplique regra aqui nem em arquivo de ferramenta específica. Toda alteração de regra permanente vai no arquivo canônico; os arquivos de entrada (este e os equivalentes de cada ferramenta) apenas apontam para ele.

## Contexto mínimo

| Para saber | Leia |
| :--- | :--- |
| O que é o projeto e o estado do acervo | [`README.md`](README.md) |
| Visão, atores e restrições inegociáveis | [`.agents/specs/project-vision/spec.md`](.agents/specs/project-vision/spec.md) |
| Decisões arquiteturais já tomadas | [`.agents/wiki/index.md`](.agents/wiki/index.md) |
| O que está pendente | [`.agents/todo.md`](.agents/todo.md) |

## Antes de qualquer commit

```bash
python .agents/scripts/verificar-documentos.py
```

O commit só pode ser proposto se a verificação passar. É a mesma checagem que o CI executa.
