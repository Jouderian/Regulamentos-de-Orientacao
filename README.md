# Regulamentos das Competições Cearenses de Orientação

Este repositório tem como objetivo atualizar e padronizar a documentação dos regulamentos das competições de orientação do Ceará, visando a gestão dos regulamentos do **Campeonato Cearense de Orientação (CCO)** e do **Campeonato Cearense de Orientação Sprint (CCOS)**, além de auxiliar na padronização e gestão das **Regras de Orientação Pedestre (ROP)** nacionais.

A conversão destes documentos para o formato **Markdown (.md)** visa facilitar o controle de versão, garantir uma estrutura de documento consistente (com hierarquia clara de artigos, parágrafos e itens) e simplificar a manutenção e a consulta por parte de atletas, clubes, organizadores e interessados. Além de facilitar o uso dos regulamentos por **IA's**, para responder perguntas sobre os regulamentos.

## Objetivos

- **Unificação:** Consolidar as regras comuns das competições em um documento coeso, mantendo claras as distinções de logística, calendário e requisitos de organização específicos de cada competição.  
- **Padronização:** Aplicar um formato *Markdown* de alta qualidade e com estilo de documento legal para melhorar a legibilidade.  
- **Manutenibilidade:** Facilitar futuras revisões, edições e acompanhamento do histórico de alterações através do controle de versão (Git).

## Documentos Principais

- **Regulamento das Competições Cearenses de Orientação**: documento unificado do **Campeonato Cearense de Orientação** (CCO) e do **Campeonato Cearense de Orientação Sprint** (CCOS).
  - **Edição 2027, em elaboração:** [`Documentos/2027/regulamentoDasCompeticoesCearenses.md`](Documentos/2027/regulamentoDasCompeticoesCearenses.md). O `.docx` e o `.pdf` da mesma pasta são gerados dele e mudam até a publicação.
  - **Edição 2026, vigente:** [`Documentos/2026/regulamentoDasCompeticoesCearenses.md`](Documentos/2026/regulamentoDasCompeticoesCearenses.md), com o PDF publicado.
- **[Regras de Orientação Pedestre](Documentos/2026/regrasOrientacaoPedestre.md)**: versão padronizada das **Regras de Orientação Pedestre** (nacional), Edição 2026, referência das duas edições acima.

## Acervo Histórico (2012-2027)

Cada edição fica em `Documentos/<ano>/`, da elaboração ao arquivamento, o que permite comparar a evolução das regras ano a ano. Todos os anos têm o PDF original e o texto em Markdown (`.md`); a conversão do acervo está concluída.

> [!IMPORTANT]
> PDF publicado não muda. Todo `.pdf` de edição publicada tem o hash SHA-256 registrado em [`Documentos/arquivosCongelados.sha256`](Documentos/arquivosCongelados.sha256), e a verificação automática recusa qualquer alteração. Para conferir: `cd Documentos && sha256sum -c arquivosCongelados.sha256`.

| Ano | CCO | CCOS | ROP (nacional) | Resultados de clubes |
| :---: | :---: | :---: | :---: | :---: |
| 2027 | **MD** + PDF + DOCX (unificado, em elaboração) | **MD** + PDF + DOCX (unificado, em elaboração) | *aguardando CBO* | *não publicado* |
| 2026 | **MD** + PDF (unificado, vigente) | **MD** + PDF (unificado, vigente) | **MD** + PDF | *em andamento* (CCO) |
| 2025 | **MD** + PDF | *não realizado* | **MD** + PDF | ✔ |
| 2024 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2023 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2022 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2020-2021 | *não realizado* | *não realizado* | **MD** + PDF | — |
| 2019 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2018 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2017 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2016 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2015 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2014 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2013 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |
| 2012 | **MD** + PDF | **MD** + PDF | **MD** + PDF | ✔ |

O padrão e o procedimento da conversão estão em [`.agents/specs/regulation-standardization/spec.md`](.agents/specs/regulation-standardization/spec.md).

> [!NOTE]
> - Em **2026**, o *Campeonato Cearense de Orientação Sprint* (CCOS) foi cancelado pela **FECORI** após a publicação do regulamento unificado, não havendo apuração de resultados de clubes para esta modalidade.
> - Em **2025** o *Campeonato Cearense de Orientação Sprint* (CCOS) não foi realizado, devido a **FECORI** ter organizado o *Campeonato Brasileiro de Orientação Sprint* (CamBOS).
> - Nos anos de **2020 e 2021**, não foram realizados campeonatos oficiais devido às restrições impostas pela pandemia de **COVID-19**. Por este motivo, não existem regulamentos correspondentes a este período.

## Histórico de Clubes Campeões

O repositório também consolida o histórico de conquistas das entidades esportivas do Ceará:
- **[clubesCampeoes.md](clubesCampeoes.md)**: Catálogo com a classificação final acumulada de clubes (campeões, vice-campeões e terceiros colocados) e a pontuação detalhada de cada clube por ano.

## Como Sugerir uma Alteração

Atletas podem propor a inclusão, a alteração ou a revogação de uma regra do regulamento por um de dois caminhos:

- **Pelo clube:** leve a sugestão ao diretor técnico do seu clube, que a encaminha à **FECORI**.
- **Pelo GitHub:** abra uma *issue* com o formulário **[Sugestão de regra](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/new?template=sugestao-regra.yml)**. O formulário pede nome completo, número CBO e clube do proponente, além do artigo afetado, da redação atual, da redação proposta e da justificativa.

> [!IMPORTANT]
> As *issues* são públicas: nome, número CBO e clube informados no formulário ficam visíveis para qualquer pessoa.

As sugestões dos dois caminhos são avaliadas juntas pelo diretor técnico da **FECORI** e pelos diretores técnicos dos clubes, na deliberação do regulamento. O resultado de cada sugestão feita por *issue* é registrado nela.

## Licença

A organização, padronização e estruturação destes arquivos estão licenciadas sob a **[Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](LICENSE)**.

Você é livre para compartilhar e adaptar o material, desde que dê o crédito apropriado às modificações e formatações originais realizadas neste repositório. O conteúdo subjacente referente às regras esportivas pertence às entidades organizadoras responsáveis.
