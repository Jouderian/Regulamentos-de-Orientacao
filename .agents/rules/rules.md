---
description: Regras gerais de idioma, nomenclatura, formato de documentos e convenções de Git do projeto
trigger: always_on
---

# Regras Gerais

> Regras aplicáveis a todo o código e todos os agentes do projeto.

---

## Idioma e Nomenclatura

- **Conteúdo do Projeto** (documentos, regulamentos, manuais): **Português do Brasil (pt-BR)**.
- **Nomes de arquivos e diretórios de projeto**: Use o formato **camelCase** (ex: `regulamentoCompeticoes.md`, `listaPresenca.md`).
- **Arquivos Sistêmicos** (dentro de `.agents/`): Mantêm o padrão **Inglês** e **kebab-case** (ex: `spec.md`, `project-vision/`) para garantir a compatibilidade com o sistema.
- **Mensagens de commit**: **Português do Brasil (pt-BR)**.

## Formato de Documentos

- Todo arquivo Markdown dentro de `.agents/` **deve** começar com YAML frontmatter contendo pelo menos o campo `description`.
- O `description` deve ser um resumo curto e objetivo do conteúdo do arquivo (uma linha).
- Isso permite que agentes identifiquem rapidamente a relevância do arquivo sem ler todo o conteúdo.

```yaml
---
description: Resumo curto do conteúdo do arquivo
---
```

## Organização dos Documentos

- **Raiz = edição em trabalho.** Os arquivos `.md` na raiz do repositório são sempre a edição **vigente ou em elaboração**. É neles que toda alteração acontece.
- **`Documentos/<ano>/` = acervo.** Contém os documentos já superados, mais os PDFs originais de cada ano.
- **Arquivamento na virada.** A cópia de um documento em `Documentos/<ano>/` é criada **no momento em que a edição é superada pela seguinte**, e não antes. Enquanto uma edição for a vigente, ela existe em um único lugar: a raiz. Isso evita duas cópias divergentes do mesmo texto e elimina a dúvida sobre qual vale.
  - Exemplo: quando a CBO publicar a ROP 2027, copie o `regrasOrientacaoPedestre.md` da raiz para `Documentos/2026/` e só então substitua o da raiz pelo texto de 2027.
- **Nome do arquivo-fonte igual ao do documento publicado.** O `.md`, o `.docx` e o `.pdf` de um mesmo documento compartilham o nome-base (ex.: `regulamentoDasCompeticoesCearenses`), variando apenas a extensão.
- **Tags de edição.** Toda edição publicada recebe uma tag anotada `v<ano>` no commit em que se tornou definitiva, dando um endereço permanente ao texto que valeu naquele ano. Edições em aberto não recebem tag.

## Convenções de Git

- **Mensagens de commit** seguem [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): descrição`
- **Escopo é obrigatório.** Não usar commits sem escopo.
- Tipos comuns: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `spec`.
- Use o tipo `spec` para alterações em artefatos SDD (ex: `spec(cco): define regra de descarte`).
- **Escopos válidos:**

  | Escopo | Quando usar |
  | :--- | :--- |
  | `cco` | Regras específicas do Campeonato Cearense de Orientação |
  | `ccos` | Regras específicas do Campeonato Cearense de Orientação Sprint |
  | `rop` | Regras de Orientação Pedestre (documento nacional da CBO) |
  | `acervo` | Documentos históricos em `Documentos/<ano>/` |
  | `historico` | `clubesCampeoes.md` e dados de classificação de clubes |
  | `agents` | Artefatos de `.agents/` (regras, specs, workflows, wiki, scripts) |
  | `ci` | Automação em `.github/` |
  | `docs` | README, LICENSE e documentação geral do repositório |
  | `root` | Configuração na raiz (`.gitignore`, `.gitattributes`) |

  Novos escopos podem ser adicionados conforme o projeto evoluir.
- **Autorização para Push:** É **obrigatório** solicitar a autorização expressa do usuário antes de realizar qualquer envio para o repositório remoto (`git push`).
- **Verificação Documental:** Antes de qualquer commit, execute `python .agents/scripts/verificar-documentos.py`. O commit só pode ser proposto se a verificação passar sem problemas — é a mesma checagem que o CI executa e que barra um *Pull Request*.
- **Regeneração de Documentos Finais:** Sempre que o arquivo `regulamentoDasCompeticoesCearenses.md` tiver sido modificado, é **obrigatório** regenerar os documentos finais (`.docx` e `.pdf`) **antes** do commit/push. Siga o workflow `.agents/workflows/atualizar-repositorio.md` para o procedimento completo.
- **Pré-requisito do Commit/Push:** Antes de solicitar a autorização para atualizar o repositório, você deve apresentar claramente ao usuário:
  1. A lista exata dos arquivos que foram modificados e estão sendo incluídos na atualização.
  2. A exata mensagem de *commit* que será utilizada.
