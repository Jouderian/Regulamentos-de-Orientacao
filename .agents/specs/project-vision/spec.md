---
description: Visão fundacional, atores e restrições dos regulamentos de orientação
---

# Visão do Projeto: Regulamentos de Orientação

## Objetivo Principal
Atuar como a fonte da verdade, padronizada e controlada por versão para as regras das competições de orientação do estado do Ceará. Este repositório simplifica a manutenção, garante o histórico de mudanças (auditabilidade) e atua como base para gerar os documentos finais (Word/PDF) para atletas, clubes e sistemas de Inteligência Artificial.

## Atores (Público-Alvo)
- **Atletas:** Consultam as regras para garantir conformidade e entender a estrutura e a logística das etapas.
- **Clubes de Orientação:** Utilizam o regulamento para balizar suas filiações e compreender seus direitos e deveres.
- **Organizadores de Eventos:** Guiam-se pelas obrigações técnicas e logísticas exigidas para o planejamento e a execução de uma competição.
- **Federações de Orientação:** São responsáveis por manter, deliberar atualizações, julgar casos omissos e publicar as versões finais.
- **Inteligências Artificiais (IAs):** Consomem a base textual estruturada em `.md` para interagir com o público e responder perguntas sobre as normativas.

## Restrições e Premissas Inegociáveis
1. **Conformidade com a CBO:** Nenhuma regra estadual pode entrar em conflito direto com as *Regras de Orientação Pedestre* (ROP) da *Confederação Brasileira de Orientação* (CBO), salvo adaptações explicitamente previstas na própria ROP.
2. **Fonte da Verdade Exclusiva (Markdown):** Toda adição, edição ou revogação de regras deve ocorrer obrigatoriamente nos arquivos `.md` na raiz do repositório. **Edições diretas em documentos Word ou PDF não são consideradas** oficiais.
3. **Rastreabilidade (Git):** Toda modificação precisa estar amparada por um histórico rastreável via controle de versão (Git).
4. **Organização Documental/Jurídica:** O regulamento consolidado deve manter e respeitar a hierarquia clássica de documentação legal (Capítulos, Artigos, Parágrafos, Incisos e Alíneas).

## Critérios de Sucesso
- Consolidação clara das regras comuns das competições de Orientação no Ceará em um arquivo único (`regulamentoCompeticoesCearenses.md`), mitigando ambiguidades ou duplicidade de informação.
- Manutenção simples para os responsáveis por meio da simplificação de formatos textuais.
- Centralização do histórico normativo.

## Fluxo de Atualização das Regras
1. Diretor(es) da Federação delibera(m) sobre alteração(ões) nas regras.
2. Diretor(es) da Federação edita(m) os arquivos `.md`.
3. Diretor(es) da Federação cria(m) um *branch* ou *commit* com a alteração.
4. Diretor(es) da Federação envia(m) a alteração para a *branch* principal (`main` ou `master`).
5. A alteração é publicada e distribuída automaticamente aos atletas, clubes e interessados.
