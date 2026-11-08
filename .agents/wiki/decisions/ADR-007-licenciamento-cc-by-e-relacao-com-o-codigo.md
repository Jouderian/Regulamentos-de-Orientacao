---
description: Decisão de licenciar a organização e a formatação do acervo em CC BY 4.0, com o texto oficial da licença no LICENSE, e de mantê-la independente da licença do código que aplica as regras.
---

# ADR 007: Licenciamento CC BY 4.0 e Relação com o Código de Apuração

> Registrada em 2026-11-08. Complementa a [ADR 001](ADR-001-markdown-como-fonte-da-verdade.md) e corresponde à [ADR 002](https://github.com/Jouderian/Apuracao-Campeonato/blob/main/.agents/wiki/decisions/ADR-002-licenciamento-polyform-noncommercial-e-relacao-com-o-regulamento.md) do repositório Apuracao-Campeonato.

## Contexto
O acervo reúne regulamentos que pertencem a outras entidades (FECORI e CBO). O que este repositório produz é a **organização e a formatação**: estrutura em Markdown, hierarquia de artigos, padronização e índices. O repositório [Apuracao-Campeonato](https://github.com/Jouderian/Apuracao-Campeonato) aplica essas regras em código e usa a licença PolyForm Noncommercial. Dois pontos pediam decisão:

- **Texto e código têm necessidades diferentes.** O texto precisa circular, ser citado e adaptado por atletas, clubes, organizadores e ferramentas de IA. O código precisa de controle sobre o uso comercial.
- **O `LICENSE` não era o texto oficial.** Tinha 24 linhas de resumo em português antes do texto da licença e caracteres corrompidos (`â€œLicensor.â€`). Por isso o GitHub o classificava como "Other" e não reconhecia a CC BY 4.0.

## Decisão
1. A organização e a formatação dos arquivos ficam sob a [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/legalcode), a variante que exige só atribuição.
2. O `LICENSE` contém **somente** o texto oficial da licença, sem alterações. O resumo em português e o modelo de crédito ficam na seção *Licença* do `README.md`.
3. O conteúdo das regras esportivas **não** é licenciado aqui: pertence à FECORI e à CBO. A licença não cobre nomes, siglas nem logotipos.
4. A licença é **independente** da do código de apuração. Trechos deste acervo citados no outro repositório continuam atribuídos à entidade de origem.

## Consequências
- **Positivas:**
  * O GitHub passa a reconhecer a licença como CC BY 4.0, e a conferência contra o texto oficial é direta.
  * Terceiros reutilizam o texto organizado, inclusive comercialmente, bastando dar o crédito.
  * Quem usa um repositório não herda as restrições do outro.
- **Negativas/Atenção:**
  * A CC BY 4.0 é irrevogável para o que já foi publicado: não dá para restringir depois ao uso não comercial.
  * Com atribuição apenas, alguém pode adaptar a organização do acervo e publicar a versão derivada em termos fechados.
  * A licença não protege o conteúdo das entidades. Quem reutiliza o texto das regras deve consultar a FECORI e a CBO quando o uso ultrapassar a consulta.
  * Qualquer troca de licença futura exige nova ADR e não alcança as versões já distribuídas.
