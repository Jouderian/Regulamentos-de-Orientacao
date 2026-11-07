---
description: Regras gerais de idioma, nomenclatura, formato de documentos e convenções de Git do projeto
trigger: always_on
---

# Regras Gerais

> Regras de todos os agentes do projeto. Toda regra permanente vive aqui. O passo a passo fica em `.agents/workflows/`, é lido só quando a tarefa o exige e nunca contradiz nem acrescenta obrigação; isso mantém curto este arquivo, carregado em toda sessão.

## Idioma e Nomenclatura

- Conteúdo do projeto (documentos, regulamentos, manuais) e mensagens de commit em **pt-BR**.
- Arquivos e pastas do projeto em **camelCase** (`regulamentoCompeticoes.md`); dentro de `.agents/`, padrão sistêmico em **kebab-case** (`project-vision/spec.md`).
- `AGENTS.md` e `CLAUDE.md` são exceção: o nome é fixado pelas ferramentas que os leem.

## Formato de Documentos

- Todo `.md` em `.agents/` começa com frontmatter YAML com `description`: resumo de uma linha, para o agente julgar a relevância sem ler o arquivo.
- **Specs.** Todo `spec.md` tem `status` (`ativa` ou `concluída`) e aparece em [`specs/index.md`](../specs/index.md) com a mesma situação. Incluir spec ou trocar o `status` atualiza o índice no mesmo commit. Consulte o índice antes de abrir uma spec; a concluída só se lê como histórico.

## Arquivos de Entrada dos Agentes

- `AGENTS.md` e `CLAUDE.md`, na raiz, são **ponteiros finos** para este arquivo e nunca contêm regra própria, para que uma alteração aqui valha em todas as ferramentas.
- Sintaxe de uma ferramenta (como a importação com `@`) só aparece no arquivo dela; este arquivo e o `AGENTS.md` usam Markdown comum.

## Estilo de Resposta ao Usuário

**Escopo:** a resposta do agente ao usuário. **Não** vale para os documentos do repositório (regulamento, spec, ADR, wiki, README), que seguem a tipografia jurídica da [ADR-003](../wiki/decisions/ADR-003-historical-regulation-standardization.md): encurtar um artigo para cumprir esta seção é violá-la.

1. Comece pela resposta ou pela próxima ação: comando, caminho do arquivo ou trecho do documento.
2. Numere trabalhos com várias etapas, uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que caiba em menos de dois minutos, quando houver.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso em **uma linha** por turno ("etapa 3 de 5 concluída"); repetir o que já foi dito é recapitulação.
6. Estime **esforço** em unidades concretas. **Fato normativo** (ano de edição, data de etapa, árbitro, colocação de clube) nunca se estima: vem do documento.
7. Após uma alteração, mostre o que passou a funcionar.
8. Erros: local, causa e correção, sem drama.
9. No máximo 5 itens por lista.
10. Sem preâmbulo, recapitulação ou despedida.

**Exceções:** explicar por completo quando o usuário pedir; confirmar antes de ação destrutiva ou irreversível; após três correções sem sucesso, parar e apontar a suposição duvidosa; diante de pedido ambíguo, uma pergunta curta. **Continuam obrigatórios:** a lista de arquivos e a mensagem de commit antes da autorização e o resultado da verificação documental.

## Organização dos Documentos

- **Pasta do ano.** Todo documento de uma edição vive em `Documentos/<ano>/` desde o início da elaboração. Na raiz, só o `clubesCampeoes.md`, que acumula todos os anos.
- **Status.** O frontmatter diz a fase: `em-elaboracao` (a única que se altera), `vigente` (exatamente uma por documento, a última publicada) ou `arquivado`. O regulamento estadual e a ROP do ano seguinte podem estar em elaboração ao mesmo tempo, no máximo um de cada. A ROP em uso é a do ano de `rop_referencia`.
- **Abrir e publicar.** A edição nova nasce da cópia do `.md` da vigente para a pasta do ano novo. Na publicação, num só commit, a em elaboração passa a `vigente` e a anterior a `arquivado`, o `.pdf` final é congelado, o `.docx` sai da pasta e o commit recebe a tag anotada `v<ano>`. Passo a passo: [`publicar-edicao.md`](../workflows/publicar-edicao.md).
- **Congelamento.** São congelados o `.pdf` do regulamento estadual (CCO, CCOS ou unificado) de edição fechada, assinado digitalmente, e o `.pdf` da ROP publicada pela CBO; o SHA-256 de cada um fica em `Documentos/arquivosCongelados.sha256`. Nenhum agente regenera, substitui, edita ou remove PDF congelado, nem altera ou remove a linha dele. O PDF da minuta da ROP, os resultados de clubes e o `.docx` não são congelados. O regulamento em elaboração existe só como `.md`: o `.docx` e o `.pdf` dele são gerados na publicação, e o `.docx` não fica no acervo. A verificação documental e o `gerar-documentos.py` impõem isso ([ADR-006](../wiki/decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md)).
- **`.md` de edição fechada** só recebe correção de transcrição contra o PDF publicado; mudança normativa exige nova edição.
- **Mesmo nome-base.** O `.md`, o `.docx` e o `.pdf` de um documento só variam na extensão (ex.: `regulamentoDasCompeticoesCearenses`).
- **Ordem cronológica inversa.** Em tabelas, listas e notas de controle e documentação (`README.md`, specs, tarefas), anos e edições vão do mais novo para o mais velho (2027, 2026, 2025...).

## Fonte de Consulta dos Documentos

**Escopo:** quem **lê** um regulamento para consultar, responder, comparar ou resumir. A [ADR-001](../wiki/decisions/ADR-001-markdown-como-fonte-da-verdade.md) fixa o Markdown como fonte da verdade.

- **Markdown primeiro.** Leia o `.md` em `Documentos/<ano>/`; a edição vigente e a em elaboração se identificam pelo `status`. O `.docx` e o `.pdf` gerados do regulamento não são fonte.
- **Leitura por trecho.** Em documento com mais de 500 linhas (a ROP tem cerca de 2.600), localize o dispositivo por busca (número da regra ou do artigo, cabeçalho) e leia só as linhas dele. Não leia o documento inteiro para pergunta pontual.
- **Comparação só quando pedida.** Compare anos ou edições apenas a pedido do usuário, buscando o mesmo dispositivo em cada arquivo.
- **PDF só na falta do `.md`**, nunca "para conferir" nem como segunda fonte. Ao usá-lo, diga na resposta que o texto veio do PDF.
- **Exceções:** conferir ou converter o `.md` contra o PDF original; pedido expresso do usuário; `.md` ilegível ou truncado, avisando o usuário antes.

## Controle de Pendências e Sugestões de Regra

Definição dos rótulos, ciclo da sugestão, comandos e modelo de fechamento: [`gestao-issues.md`](../workflows/gestao-issues.md), lido antes de abrir, alterar ou fechar *issue*. Decisão: [ADR-005](../wiki/decisions/ADR-005-controle-de-pendencias-por-issues.md).

- **Controle único.** O que está pendente vive só como *issue* do GitHub; [`todo-done.md`](../todo-done.md) é histórico congelado até 2026-10-17. Sem acesso ao GitHub, peça o texto da *issue* ao usuário e não presuma.
- **Rótulos.** Um de tipo (`sugestão de regra`, `tarefa`, `acompanhamento`) e um de equipe (`equipe: regras`, `equipe: repositório`); na dúvida, a equipe é a que executa. A ROP é da CBO: sugestão a ela e espera por nova edição são sempre `acompanhamento`.
- **Revisão.** Texto normativo (`Documentos/**/*.md`, `clubesCampeoes.md`) só muda com revisão da equipe de regras, seja qual for a equipe da *issue*.
- **Sugestão de regra.** Só é aberta com nome completo, número CBO e clube do proponente (peça o que faltar); esses dados só aparecem nela. Tem no máximo um rótulo `situação` e fecha na deliberação; aprovada, gera uma `tarefa` com a redação final.
- **Autorização do usuário** para abrir *issue* com texto do agente (apresente a redação: ela fica pública), trocar a situação de sugestão e fechar *issue* ou *milestone*. Toda *issue* fecha com comentário de resumo, inclusive via `Closes #N`, apresentado ao usuário antes.
- **Atribuição.** Quem dirige o agente indica a *issue*; o agente não escolhe tarefa nem pega *issue* com responsável. Indicada, ele a assume (`gh issue edit <N> --add-assignee "@me"`) e comenta as considerações iniciais antes de alterar.

## Convenções de Git

- [Conventional Commits](https://www.conventionalcommits.org/): `tipo(escopo): descrição`, **escopo obrigatório**. Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore` e `spec` (artefatos SDD, ex.: `spec(cco): define regra de descarte`).
- Commit que trata de *issue* leva no rodapé `Refs #N`, ou `Closes #N` se a conclui.
- **Escopos válidos** (novos podem ser criados conforme o projeto evoluir):

  | Escopo | Quando usar |
  | :--- | :--- |
  | `cco` | Regras específicas do Campeonato Cearense de Orientação |
  | `ccos` | Regras específicas do Campeonato Cearense de Orientação Sprint |
  | `rop` | Regras de Orientação Pedestre (documento nacional da CBO) |
  | `acervo` | Organização de `Documentos/<ano>/`, edições arquivadas e manifesto de arquivos congelados |
  | `historico` | `clubesCampeoes.md` e dados de classificação de clubes |
  | `agents` | Artefatos de `.agents/` (regras, specs, workflows, wiki, scripts) |
  | `ci` | Automação em `.github/` |
  | `docs` | README, LICENSE e documentação geral do repositório |
  | `root` | Configuração na raiz (`.gitignore`, `.gitattributes`) |

- **Autoria humana exclusiva.** Nenhum rodapé de coautoria ou de geração por IA (`Co-Authored-By:`, `Generated with` ou equivalente): faria o agente constar como *Contributor* no GitHub. Confira o rodapé antes de propor o commit.
- **Antes do commit:** `python .agents/scripts/verificar-documentos.py` sem problemas (é a checagem do CI). Mudança no `.md` em elaboração não regenera `.docx` nem `.pdf`, que só são gerados na publicação; edição fechada nunca é regenerada.
- **Antes de pedir autorização:** apresente a lista exata de arquivos e a mensagem exata do commit. `git push` só com autorização expressa do usuário.
