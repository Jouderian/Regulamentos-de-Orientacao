---
description: Histórico de tarefas concluídas do projeto
---

# Tarefas Concluídas (Histórico)

- [X] **Revisão de Redação (Regulamento Geral):** No Art. 2º, Parágrafo 1º, alínea 'a', analisar a condição *"ou participar de pelo menos um evento oficial da FECORI"*. A redação atual pode gerar problemas jurídicos/esportivos na definição exata de quem constitui um atleta filiado.
- [X] **Revisão de Redação (Regulamento Geral) comparado com CCO:** As lacunas identificadas na análise comparativa estão sanadas. O regulamento unificado agora contempla integralmente todas as regras do CCO original.
- [X] **Revisão de Redação (Regulamento Geral) comparado com CCOS:** As lacunas identificadas na análise comparativa estão sanadas. O regulamento unificado agora contempla integralmente todas as regras do CCOS original.
- [X] **Atualiza arquivo final** do arquivo Word (.docx) com o conteudo do regulamento geral atualizado.
- [X] **Revisão da Redação (Regulamento Geral) comparando com a ROP** As lacunas identificadas na análise comparativa estão sanadas. O regulamento unificado agora contempla integralmente todas as regras da ROP.
- [X] **Automação da Geração de Documentos:** Implementado workflow local (`/atualizar-repositorio`) que regenera automaticamente os documentos finais (`.docx` e `.pdf`) via Pandoc e Word COM sempre que o `regulamentoCompeticoesCearenses.md` for alterado, antes do push ao repositório remoto.
- [X] **Padronização dos Regulamentos Históricos (2018-2025):** Arquivos PDF antigos convertidos para Markdown usando as ferramentas `Pandoc` (via conversão prévia Word) e `pdftotext` (via extração e Regex PowerShell). Todo o acervo foi padronizado (Capítulos, Artigos, Parágrafos) seguindo a estrutura de 2026.
- [X] **Bloco de metadados nos regulamentos:** Adicionado frontmatter YAML no topo de todos os 12 regulamentos declarando `ano`, `edicao`, `status` (`vigente`/`arquivado`) e `rop_referencia`. Criado o script `python .agents/scripts/gerar-documentos.py` que remove o frontmatter antes do Pandoc (impedindo vazamentos no `.docx`/`.pdf`) e compila ambos os formatos de forma integrada. O script `verificar-documentos.py` foi estendido para validar a obrigatoriedade dos campos e exigir exatamente 1 regulamento com `status: vigente`.
- [X] **Atualização das ações do CI (Node.js 20 descontinuado):** Em `.github/workflows/verificacao-documental.yml`, `actions/checkout`, `actions/setup-python` e `actions/upload-artifact` passaram para `@v7`, versões que rodam nativamente em Node.js 24, eliminando o aviso de descontinuação do Node.js 20. O `pandoc/actions/setup@v1` foi mantido por ser ação *composite*, sem dependência de Node.js.
