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

## Arquivos de Entrada dos Agentes

- Este arquivo é o **canônico**: toda regra permanente vive aqui e em nenhum outro lugar.
- O passo a passo que executa uma regra fica em `.agents/workflows/` e é lido só quando a tarefa o exige. O workflow detalha a regra, nunca a contradiz nem cria obrigação nova; isso mantém este arquivo curto, porque ele é carregado em toda sessão.
- Os arquivos de entrada de cada ferramenta (`AGENTS.md` e `CLAUDE.md`, na raiz) são **ponteiros finos** para este. Nunca contêm regra própria — só apontam, para que uma alteração aqui valha em todas as ferramentas ao mesmo tempo.
- `AGENTS.md` e `CLAUDE.md` são exceções à regra de nomenclatura *camelCase*: seus nomes são fixados pelas ferramentas que os leem e não podem ser alterados.
- Sintaxe específica de uma ferramenta (como a importação com `@`) só pode aparecer dentro do arquivo daquela ferramenta. Este arquivo e o `AGENTS.md` usam apenas Markdown comum.

## Estilo de Resposta ao Usuário

**Escopo:** vale para a **resposta do agente ao usuário**. **Não** vale para o conteúdo dos documentos do repositório — regulamento, spec, ADR, página de wiki, README —, que seguem o *Formato de Documentos* acima e a tipografia jurídica da [ADR-003](../wiki/decisions/ADR-003-historical-regulation-standardization.md). Um artigo de regulamento exige forma completa e fórmula fixa: encurtá-lo para cumprir esta seção é violá-la.

Estruture cada resposta para que o usuário possa agir:

1. Comece pela resposta ou pela próxima ação: o comando, o caminho do arquivo ou o trecho do documento primeiro.
2. Numere trabalhos com várias etapas; uma ação bem delimitada por etapa.
3. Termine com uma próxima ação que caiba em menos de dois minutos, quando houver uma.
4. Conclua o problema atual antes de levantar outro.
5. Reafirme o progresso a cada turno em **uma linha** ("etapa 3 de 5 concluída"). Uma linha de progresso não é recapitulação; repetir o que já foi dito, é.
6. Estime **esforço** em unidades concretas, nunca "um pouco". Estimar **fato normativo** — ano de edição, data de etapa, nome de árbitro, colocação de clube — é proibido: esses vêm do documento (Markdown primeiro; ver *Fonte de Consulta dos Documentos*) ou do PDF original, nunca de suposição.
7. Após uma alteração, mostre o que passou a funcionar.
8. Erros: informe local, causa e correção, sem drama.
9. Limite a 5 itens cada lista dentro de uma resposta.
10. Sem preâmbulo, recapitulação ou despedida.

**Exceções:** explicar por completo quando o usuário pedir; confirmar antes de ação destrutiva ou irreversível; após três tentativas de correção sem sucesso, parar e identificar a suposição duvidosa; diante de pedido ambíguo, fazer uma pergunta curta.

**Não contam como recapitulação e continuam obrigatórios:** apresentar a lista de arquivos e a mensagem de commit antes de pedir autorização (ver *Convenções de Git*) e relatar o resultado da verificação documental.

## Organização dos Documentos

- **Raiz = edição em trabalho.** Os arquivos `.md` na raiz do repositório são sempre a edição **vigente ou em elaboração**. É neles que toda alteração acontece.
- **`Documentos/<ano>/` = acervo.** Contém os documentos já superados, mais os PDFs originais de cada ano.
- **Arquivamento na virada.** A cópia de um documento em `Documentos/<ano>/` é criada **no momento em que a edição é superada pela seguinte**, e não antes. Enquanto uma edição for a vigente, ela existe em um único lugar: a raiz. Isso evita duas cópias divergentes do mesmo texto e elimina a dúvida sobre qual vale.
  - Exemplo: quando a CBO publicar a ROP 2027, copie o `regrasOrientacaoPedestre.md` da raiz para `Documentos/2026/` e só então substitua o da raiz pelo texto de 2027.
- **Nome do arquivo-fonte igual ao do documento publicado.** O `.md`, o `.docx` e o `.pdf` de um mesmo documento compartilham o nome-base (ex.: `regulamentoDasCompeticoesCearenses`), variando apenas a extensão.
- **Tags de edição.** Toda edição publicada recebe uma tag anotada `v<ano>` no commit em que se tornou definitiva, dando um endereço permanente ao texto que valeu naquele ano. Edições em aberto não recebem tag.
- **Ordem cronológica inversa.** Em tabelas, relações, listas e notas de arquivos de controle e documentação (`README.md`, specs, tarefas), os anos e edições são sempre apresentados do mais novo para o mais velho (ex.: 2027, 2026, 2025...), facilitando a consulta e as buscas históricas.

## Fonte de Consulta dos Documentos

**Escopo:** vale para qualquer agente que **leia** o conteúdo de um regulamento do repositório para consultar, responder, comparar ou resumir. A [ADR-001](../wiki/decisions/ADR-001-markdown-como-fonte-da-verdade.md) fixa o Markdown como fonte da verdade; esta seção fixa o que ler.

- **Markdown primeiro.** Leia sempre o `.md` do documento. Na edição vigente ou em elaboração, ele está na raiz; em edição superada, em `Documentos/<ano>/`.
- **Documento longo, leitura por trecho.** Em documento com mais de 500 linhas (a ROP tem cerca de 2.600), localize o dispositivo por busca — número da regra ou do artigo, ou cabeçalho — e leia só as linhas dele; a ROP traz índice no início do arquivo. Para comparar anos, busque o mesmo dispositivo em cada arquivo. Não leia o documento inteiro para responder a uma pergunta pontual.
- **PDF só na falta do `.md`.** Abra o `.pdf` apenas quando o `.md` daquele documento, naquele ano, não existir (conversão pendente; a situação de cada ano está no [`README.md`](../../README.md)). Havendo `.md`, não abra o `.pdf` "para conferir" nem o use como segunda fonte.
- **`.docx` e `.pdf` gerados não são fonte.** Em `Documentos/2027/` o `.docx` e o `.pdf` são saída gerada do `.md` da raiz; consulte a raiz.
- **Declare o PDF.** Ao responder com base em um PDF, diga na resposta que o texto veio do PDF por falta do `.md`. Nunca misture as duas fontes sem avisar.
- **Exceções:** tarefa cujo objetivo é conferir ou converter o `.md` contra o PDF original (conferência de texto normativo, conversão do acervo); pedido expresso do usuário; `.md` ilegível ou truncado, caso em que o agente avisa o usuário antes de recorrer ao PDF.

## Controle de Pendências e Sugestões de Regra

O passo a passo — formulários, ciclo da sugestão, troca de situação, vínculo de dependência, modelo do comentário de fechamento e comandos — está no workflow [`gestao-issues.md`](../workflows/gestao-issues.md). Leia-o antes de abrir, alterar ou fechar uma *issue*. A decisão está na [ADR-005](../wiki/decisions/ADR-005-controle-de-pendencias-por-issues.md).

- **Controle único.** Tudo o que está pendente vive como *issue* do GitHub, nunca em dois lugares. Não existe `todo.md`: o histórico anterior a 2026-10-17 está congelado em [`todo-done.md`](../todo-done.md). Quem não tiver acesso ao GitHub pede ao usuário o texto da *issue* e não presume o conteúdo.
- **Um rótulo de tipo e um de equipe.** Tipos: `sugestão de regra` (inclusão, alteração ou revogação de dispositivo do regulamento), `tarefa` (trabalho que a própria equipe executa e fecha) e `acompanhamento` (item que depende de terceiro e só se fecha quando ele decidir). Equipes: `equipe: regras` (conteúdo normativo, calendário, interpretação de regra, conferência de texto normativo e acompanhamento da CBO) e `equipe: repositório` (scripts, CI, estrutura de pastas, documentação do repositório e conversão técnica do acervo). Na dúvida, a equipe é a que **executa**.
- **ROP é da CBO.** A ROP só pode ser alterada pela CBO: sugestão à CBO e espera por nova edição são sempre `acompanhamento`, nunca `tarefa`. Quando a CBO decidir, abre-se uma `tarefa` para o que couber ao repositório.
- **Revisão entre equipes.** Texto normativo (regulamento, ROP, `Documentos/**/*.md`, `clubesCampeoes.md`) só é alterado com revisão da equipe de regras, seja qual for a equipe da *issue*.
- **Sugestão fecha na deliberação.** A `sugestão de regra` aberta significa decisão pendente e tem no máximo um rótulo `situação`. Aprovada, gera uma `tarefa` com a redação final, que fecha quando o texto entra no regulamento.
- **Identificação do proponente.** A sugestão só é aberta com nome completo, número CBO e clube de quem sugere; faltando algum, o agente pede ao usuário antes de abrir. *Issues* são públicas: esses dados só aparecem na sugestão de regra, com a ciência do proponente, e `tarefa` e `acompanhamento` não levam dado pessoal.
- **Só com autorização do usuário.** O agente apresenta a redação antes de abrir *issue* com texto que ele redigiu, porque ela fica pública (na sugestão, em nome do proponente). Também depende de autorização trocar a situação de uma sugestão, fechar *issue* e fechar *milestone*.
- **Atribuição.** Cada pessoa se atribui à *issue* antes de começar, e ninguém pega *issue* que já tem responsável. O agente não escolhe tarefa nem se atribui sozinho: quem o dirige indica a *issue*. Indicada a *issue*, o agente a assume (`gh issue edit <N> --add-assignee "@me"`) e publica um comentário com as considerações iniciais antes de iniciar as modificações.
- **Fechamento com resumo.** Toda *issue* fecha com um comentário de resumo no formato do workflow, inclusive quando o fechamento vem de `Closes #N`. O agente apresenta o resumo ao usuário antes de comentar.

## Convenções de Git

- **Mensagens de commit** seguem [Conventional Commits](https://www.conventionalcommits.org/):
  `type(scope): descrição`
- **Escopo é obrigatório.** Não usar commits sem escopo.
- **Referência a *issue*.** Quando o commit trata de uma *issue*, o rodapé traz `Refs #N` (ou `Closes #N`, se a conclui). É referência, não autoria: não conflita com a regra de autoria abaixo.
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
- **Autoria humana exclusiva.** Nenhum commit pode carregar rodapé de coautoria ou de geração por agente de IA (`Co-Authored-By:`, `Generated with`, ou equivalente). O trabalho do repositório é assinado apenas pelo mantenedor humano, e um rodapé desses faz o agente constar como *Contributor* no GitHub. Antes de propor um commit, confira o rodapé da mensagem.
- **Autorização para Push:** É **obrigatório** solicitar a autorização expressa do usuário antes de realizar qualquer envio para o repositório remoto (`git push`).
- **Verificação Documental:** Antes de qualquer commit, execute `python .agents/scripts/verificar-documentos.py`. O commit só pode ser proposto se a verificação passar sem problemas — é a mesma checagem que o CI executa e que barra um *Pull Request*.
- **Regeneração de Documentos Finais:** Sempre que o arquivo `regulamentoDasCompeticoesCearenses.md` tiver sido modificado, é **obrigatório** regenerar os documentos finais (`.docx` e `.pdf`) **antes** do commit/push. Siga o workflow `.agents/workflows/atualizar-repositorio.md` para o procedimento completo.
- **Pré-requisito do Commit/Push:** Antes de solicitar a autorização para atualizar o repositório, você deve apresentar claramente ao usuário:
  1. A lista exata dos arquivos que foram modificados e estão sendo incluídos na atualização.
  2. A exata mensagem de *commit* que será utilizada.
