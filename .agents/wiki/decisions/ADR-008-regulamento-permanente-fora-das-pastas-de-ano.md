---
description: Decisão de manter regulamento da FECORI sem edição anual, como o de uso do kit SPORTident, em Documentos/ fora das pastas de ano, alterado no mesmo arquivo e com status próprio.
---

# ADR 008: Regulamento Permanente Fora das Pastas de Ano

> Registrada em 2026-11-15. Complementa a [ADR 006](ADR-006-edicoes-por-ano-e-arquivos-congelados.md). Decidida na [*issue* #51](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/51).

## Contexto
A FECORI adquiriu um kit de cronometragem SPORTident e precisa regular o uso dele pelos clubes filiados e o empréstimo a outras federações. O regulamento do kit difere do restante do acervo em três pontos:

- **Não tem edição anual.** Vale até ser alterado e não acompanha a temporada do CCO e do CCOS. A [ADR 006](ADR-006-edicoes-por-ano-e-arquivos-congelados.md) pressupõe que todo documento pertença a uma edição em `Documentos/<ano>/`.
- **É aprovado de outro modo.** A Diretoria da FECORI aprova e altera; a Assembleia Geral referenda na reunião seguinte.
- **Não é regra de competição.** O acervo reunia só os regulamentos das competições estaduais e a ROP.

## Decisão
1. Regulamento da FECORI sem edição anual é **permanente** e vive em `Documentos/`, fora das pastas de ano. O primeiro é o [`regulamentoDeUsoDoKitSportident.md`](../../../Documentos/regulamentoDeUsoDoKitSportident.md).
2. O `status` diz a fase: `em-elaboracao` até a aprovação da Diretoria e `vigente` depois. Não há `arquivado`: a alteração aprovada entra no mesmo arquivo, e o histórico fica no Git.
3. O frontmatter registra a data da última aprovação da Diretoria em `aprovacao: AAAA-MM-DD` e a do referendo da Assembleia Geral em `referendo: AAAA-MM-DD`.
4. O PR que altera texto `vigente` só é mesclado depois da aprovação da Diretoria, porque a mesclagem muda de imediato a versão em vigor.
5. O texto segue a tipografia jurídica da [ADR 003](ADR-003-historical-regulation-standardization.md) e passa pela revisão da equipe de regras, como todo `.md` de `Documentos/` ([`CODEOWNERS`](../../../.github/CODEOWNERS)).
6. Não se gera nem se congela `.docx` ou `.pdf` do regulamento permanente. Se a FECORI passar a publicar PDF assinado, a decisão será revista.
7. Os commits do regulamento do kit usam o escopo `kit`.

## Consequências
- **Positivas:**
  * O regulamento tem endereço estável, e a versão em vigor é sempre a do arquivo.
  * As pastas de ano continuam guardando só o que pertence a uma edição.
  * Clubes, federações e ferramentas de IA consultam o regulamento do kit no mesmo acervo dos regulamentos de competição.
- **Negativas/Atenção:**
  * A versão aprovada em certa data só se recupera pelo histórico do Git: não há cópia por versão nem PDF assinado e congelado.
  * O `verificar-documentos.py` reconhece os regulamentos pelo prefixo do nome e não aplica ao regulamento permanente as checagens de estrutura e de tipografia. Até a verificação ser estendida, a sequência de artigos, o ordinal, o parágrafo único e a alínea são conferidos na revisão.
  * O acervo deixa de ser só de regras de competição, e o `README.md` ganha uma seção própria para o regulamento do kit.
