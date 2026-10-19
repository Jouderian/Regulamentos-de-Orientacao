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
- **PDF só na falta do `.md`.** Abra o `.pdf` apenas quando o `.md` daquele documento, naquele ano, não existir (conversão pendente; a situação de cada ano está no [`README.md`](../../README.md)). Havendo `.md`, não abra o `.pdf` "para conferir" nem o use como segunda fonte.
- **`.docx` e `.pdf` gerados não são fonte.** Em `Documentos/2027/` o `.docx` e o `.pdf` são saída gerada do `.md` da raiz; consulte a raiz.
- **Declare o PDF.** Ao responder com base em um PDF, diga na resposta que o texto veio do PDF por falta do `.md`. Nunca misture as duas fontes sem avisar.
- **Exceções:** tarefa cujo objetivo é conferir ou converter o `.md` contra o PDF original (conferência de texto normativo, conversão do acervo); pedido expresso do usuário; `.md` ilegível ou truncado, caso em que o agente avisa o usuário antes de recorrer ao PDF.

- **Controle único.** Tudo o que está pendente vive como *issue* do GitHub. Não existe `todo.md`: o histórico anterior a 2026-10-17 está congelado em [`todo-done.md`](../todo-done.md). Uma pendência nunca é registrada em dois lugares. A decisão está na [ADR-005](../wiki/decisions/ADR-005-controle-de-pendencias-por-issues.md).
- **Três tipos, um rótulo cada.** O formulário já aplica o rótulo.
  - `sugestão de regra`: proposta de inclusão, alteração ou revogação de dispositivo do regulamento. Formulário [`sugestao-regra.yml`](../../.github/ISSUE_TEMPLATE/sugestao-regra.yml).
  - `tarefa`: trabalho que a própria equipe executa e fecha. Formulários [`tarefa-regras.yml`](../../.github/ISSUE_TEMPLATE/tarefa-regras.yml) e [`tarefa-repositorio.yml`](../../.github/ISSUE_TEMPLATE/tarefa-repositorio.yml).
  - `acompanhamento`: item que depende de terceiro e só se fecha quando ele decidir. Formulário [`acompanhamento.yml`](../../.github/ISSUE_TEMPLATE/acompanhamento.yml). A ROP só pode ser alterada pela CBO: sugestão à CBO e espera por nova edição são sempre `acompanhamento`, nunca `tarefa`. Quando a CBO decidir, abre-se uma `tarefa` para o que couber ao repositório.
- **Duas equipes, um rótulo cada.** Toda *issue* tem exatamente um rótulo de tipo e um de equipe.
  - `equipe: regras`: conteúdo normativo — regulamento, calendário, interpretação de regra, conferência de texto normativo contra o original e acompanhamento da CBO.
  - `equipe: repositório`: scripts, CI, estrutura de pastas, documentação do repositório e conversão técnica do acervo.
  - Na dúvida, a equipe é a que **executa**.
- **Revisão entre equipes.** Texto normativo (regulamento, ROP, `Documentos/**/*.md`, `clubesCampeoes.md`) só é alterado com revisão da equipe de regras, seja qual for a equipe da *issue*.
- **Dependências.** A *issue* que aguarda outra é ligada a ela pelo vínculo nativo "Bloqueada por" do GitHub, criado pela interface da *issue* ou pela API (`dependencies/blocked_by`), e explica o motivo no corpo, em "Bloqueada porque". Não há rótulo de bloqueio: o vínculo é a única fonte.
- **Sugestão de regra vira *issue*.** Toda proposta de inclusão, alteração ou revogação de dispositivo do `regulamentoDasCompeticoesCearenses.md` é registrada como *issue* no GitHub, com o formulário [`sugestao-regra.yml`](../../.github/ISSUE_TEMPLATE/sugestao-regra.yml) e o rótulo `sugestão de regra`. É um tipo próprio, nunca `tarefa`.
- **Identificação do proponente.** A *issue* só é aberta com nome completo, número CBO e clube de quem sugere. Faltando algum desses dados, o agente pede ao usuário antes de abrir.
- **Redação elaborada pelo agente.** Quando o proponente só descreve a intenção e o agente redige o texto proposto, o agente apresenta a redação ao usuário antes de abrir a *issue*, porque ela fica pública em nome do proponente. O mesmo vale para o texto de qualquer `tarefa` ou `acompanhamento` que o agente redija. O agente não fecha *issue* sem autorização do usuário.
- **Várias pessoas e vários agentes.** Cada pessoa se atribui à *issue* antes de começar, e o agente que ela dirige trabalha sob essa atribuição. Ninguém pega *issue* que já tem responsável. O agente não escolhe tarefa nem se atribui sozinho: quem o dirige indica a *issue*. Ao ser direcionado para atuar em uma *issue*, o agente deve imediatamente assumi-la no GitHub (`gh issue edit <N> --add-assignee "@me"`) e publicar um comentário com as considerações iniciais sobre o trabalho antes de iniciar as modificações, garantindo visibilidade a toda a equipe.
- **Fechamento com resumo.** Ao fechar uma *issue*, quem fecha deixa nela um comentário com o resumo do que foi feito, para que ler o histórico não exija abrir o PR ou o commit. O comentário traz **Resumo** (o que foi feito, em até 3 linhas), **Mudanças** (arquivos alterados ou decisão tomada), **Referência** (hash do commit ou número do PR) e **Fica de fora** (o que não foi feito e em qual *issue* está registrado, ou "nada"). Se o fechamento vem de `Closes #N` em PR ou commit, o comentário é postado no mesmo momento, porque o fechamento automático não registra o que foi feito. Na `sugestão de regra`, o resumo traz o resultado da deliberação e a redação final aprovada, ou a justificativa da rejeição. No `acompanhamento`, traz a decisão do terceiro e o que ela gerou (por exemplo, a `tarefa` aberta). O agente apresenta o resumo ao usuário antes de comentar.
- **Sem dados pessoais.** *Issues* são públicas. `tarefa` e `acompanhamento` não levam dado pessoal; nome, número CBO e clube só aparecem nas sugestões de regra, com a ciência do proponente.
- **Consulta independente de ferramenta.** Nenhuma regra pressupõe um cliente específico. O backlog se consulta pela web, nas *issues* abertas da [equipe de regras](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues?q=is%3Aissue+is%3Aopen+label%3A%22equipe%3A+regras%22) e da [equipe do repositório](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues?q=is%3Aissue+is%3Aopen+label%3A%22equipe%3A+reposit%C3%B3rio%22), ou por qualquer cliente do GitHub (por exemplo, `gh issue list --label "equipe: regras"`). Quem não tiver acesso pede ao usuário o texto da *issue* e não presume o conteúdo.

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
