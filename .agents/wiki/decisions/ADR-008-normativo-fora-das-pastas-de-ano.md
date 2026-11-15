---
description: Decisão de manter o normativo da FECORI sem edição anual, como a norma de uso do kit SPORTident, em Documentos/normativos/ fora das pastas de ano, alterado no mesmo arquivo, com status próprio e verificação documental.
---

# ADR 008: Normativo Fora das Pastas de Ano

> Registrada em 2026-11-15; o tipo, antes chamado "regulamento permanente", passou a **normativo** no mesmo dia. Complementa a [ADR 006](ADR-006-edicoes-por-ano-e-arquivos-congelados.md). Decidida na [*issue* #51](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/51).

## Contexto
A FECORI adquiriu um kit de cronometragem SPORTident e precisa regular o uso dele pelos clubes filiados e o empréstimo a outras federações. A norma do kit difere do restante do acervo em três pontos:

- **Não tem edição anual.** Vale até ser alterado e não acompanha a temporada do CCO e do CCOS. A [ADR 006](ADR-006-edicoes-por-ano-e-arquivos-congelados.md) pressupõe que todo documento pertença a uma edição em `Documentos/<ano>/`.
- **É aprovado de outro modo.** A Diretoria da FECORI aprova e altera; a Assembleia Geral referenda na reunião seguinte.
- **Não é regra de competição.** O acervo reunia só os regulamentos das competições estaduais e a ROP.

## Decisão
1. **Normativo** é o documento normativo de âmbito técnico da FECORI sem edição anual. Vive em `Documentos/normativos/`, fora das pastas de ano. O primeiro é o [`normaDeUsoDoKitSportident.md`](../../../Documentos/normativos/normaDeUsoDoKitSportident.md).
2. **Exceção: o Regimento de Taxas.** Tem regramento próprio e cabe à Diretoria Financeira da FECORI, fora do âmbito técnico. Este repositório não o hospeda: apenas o cita nos normativos que dependem dele.
3. O `status` diz a fase: `em-elaboracao` até a aprovação da Diretoria e `vigente` depois. Não há `arquivado`: a alteração aprovada entra no mesmo arquivo, e o histórico fica no Git.
4. O frontmatter registra a data da última aprovação da Diretoria em `aprovacao: AAAA-MM-DD` e a do referendo da Assembleia Geral em `referendo: AAAA-MM-DD`. O normativo `vigente` exige `aprovacao`.
5. O PR que altera texto `vigente` só é mesclado depois da aprovação da Diretoria, porque a mesclagem muda de imediato a versão em vigor.
6. O texto segue a tipografia jurídica da [ADR 003](ADR-003-historical-regulation-standardization.md) e passa pela revisão da equipe de regras, como todo `.md` de `Documentos/` ([`CODEOWNERS`](../../../.github/CODEOWNERS)).
7. Não se gera nem se congela `.docx` ou `.pdf` do normativo. Se a FECORI passar a publicar PDF assinado, a decisão será revista.
8. O `verificar-documentos.py` reconhece o normativo pelo caminho (`.md` direto em `Documentos/normativos/`) e aplica a ele as checagens de estrutura e de tipografia, a de referências a artigos, a do frontmatter e a de ausência de `.docx` e `.pdf`. Normativo `vigente` não pode conter pendência `???`.
9. Os commits do normativo do kit usam o escopo `kit`.

## Consequências
- **Positivas:**
  * O normativo tem endereço estável, e a versão em vigor é sempre a do arquivo.
  * As pastas de ano continuam guardando só o que pertence a uma edição.
  * Clubes, federações e ferramentas de IA consultam o normativo no mesmo acervo dos regulamentos de competição.
  * Inserir ou remover artigo não deixa referência cruzada apontando para o artigo errado sem que o CI acuse.
- **Negativas/Atenção:**
  * A versão aprovada em certa data só se recupera pelo histórico do Git: não há cópia por versão nem PDF assinado e congelado.
  * A verificação de referências confere o número do artigo, não o parágrafo ("Art. 3º, Parágrafo 2º"): a existência do parágrafo é conferida na revisão.
  * Referência a artigo de outro documento ("Art. 55 do Estatuto") é ignorada pela verificação, que reconhece o padrão `d[oa] <documento>` logo depois do número.
  * O acervo deixa de ser só de regras de competição, e o `README.md` ganha uma seção própria para o normativo do kit.

## Revisão de 2026-11-15: pasta própria e nome do arquivo
Decidida na [*issue* #57](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/57). Com o normativo solto na raiz de `Documentos/`, ao lado do manifesto e do template, o verificador o reconhecia por exclusão ("qualquer `.md` direto em `Documentos/`"), e cada norma nova cairia no mesmo monte. Decidiu-se:

1. O normativo vive em **`Documentos/normativos/`**, uma norma por arquivo. As pastas de ano e os nomes do passado não mudam: o manifesto de arquivos congelados, as tags `v<ano>` e os links externos dependem deles.
2. O nome do arquivo começa por **`norma`** (`normaDeUsoDoKitSportident.md`), como `regulamento…` e `regras…` já indicam o tipo do ato; **normativo** é o nome da categoria e da pasta. O regulamento do kit, ainda `em-elaboracao`, passa a "Norma de Uso do Kit de Cronometragem SPORTident".
3. O verificador reconhece o normativo pelo caminho. Até o arquivo do kit mudar de pasta, aceita também `.md` direto em `Documentos/`; o segundo caso é removido depois da migração.
4. Renomear ou mover documento normativo vai no mesmo PR da correção dos links, exceção à regra de PR separado, porque a verificação documental acusa link quebrado.

**Consequências:**
- Cada norma futura entra em `Documentos/normativos/` sem alterar regra nem script, e o `CODEOWNERS` atual (`/Documentos/**/*.md`) já a cobre.
- A migração tem dois PRs: o de infraestrutura, que aceita os dois caminhos e mescla sem aprovação, e o do arquivo, que precisa da equipe de regras.
- Se uma norma passar a ter arquivos anexos (como formulários dos Anexos III e IV do kit), a estrutura de uma pasta por norma deve ser reavaliada.
