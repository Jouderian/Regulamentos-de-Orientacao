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