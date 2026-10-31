---
description: Procedimento operacional para a geração automatizada de documentos finais (.docx e .pdf) a partir da fonte em Markdown (.md).
---

# Workflow: Geração de Documentos Finais

Este guia descreve os passos exatos e dependências necessárias para converter o arquivo base de regulamentos em Markdown para o formato Word (.docx), preservando o layout e a identidade visual da Federação. Este documento serve como manual para futuros contribuidores e agentes de Inteligência Artificial.

## 1. Dependências Necessárias

A automação da conversão depende do **Pandoc**, um conversor universal de documentos.

**Para instalar no Windows (PowerShell/CMD):**
```powershell
winget install JohnMacFarlane.Pandoc
```
> [!NOTE]
> Se a ferramenta não for reconhecida imediatamente após a instalação, reinicie o terminal ou recarregue as variáveis de ambiente (`$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")`).

## 2. O Molde (Template)
Para evitar a perda da formatação oficial da Federação, o projeto utiliza um documento Word base chamado de molde ou template. 
- O arquivo deve estar localizado em: `Documentos/template_estilos.docx`.
- **Como funciona:** O *Pandoc* extrairá as configurações desse arquivo (como tamanho da página, margens, fontes e estilos de cabeçalhos) e aplicará o texto atualizado do arquivo Markdown sobre elas.
- **Manutenção do Molde:** Caso seja necessário alterar a fonte oficial ou as margens dos futuros regulamentos, basta abrir o `Documentos/template_estilos.docx` no *Microsoft Word*, editar os estilos nativos e salvar.

## 3. Geração Automatizada (.docx e .pdf)

Sempre que o regulamento em elaboração for alterado, execute o script de automação na raiz do repositório:

```bash
python .agents/scripts/gerar-documentos.py
```

O script realiza o processo completo de forma integrada:
1. Localiza o regulamento com `status: em-elaboracao` em `Documentos/<ano>/` e grava o `.docx` e o `.pdf` na mesma pasta. Edição vigente ou arquivada é recusada: o `.pdf` dela está congelado ([ADR-006](../wiki/decisions/ADR-006-edicoes-por-ano-e-arquivos-congelados.md)).
2. Remove o bloco de metadados frontmatter (`--- ... ---`) antes de repassar o texto puro ao Pandoc via `stdin`, garantindo que nenhum metadado vaze para o documento final.
3. Compila o `.docx` aplicando o template oficial `Documentos/template_estilos.docx`.
4. Converte o `.docx` em `.pdf` de forma transparente via Microsoft Word (COM).

## 4. Execução Manual (Referência)

Caso seja necessário executar as etapas manualmente sem o script, sempre na edição em elaboração:

1. **Compilar DOCX via Pandoc:**
   ```powershell
   pandoc Documentos/<ano>/regulamentoDasCompeticoesCearenses.md -o Documentos/<ano>/regulamentoDasCompeticoesCearenses.docx --reference-doc=Documentos/template_estilos.docx
   ```
2. **Converter DOCX em PDF via Word:**
   ```powershell
   $word = New-Object -ComObject Word.Application
   $word.Visible = $false
   $docPath = Resolve-Path "Documentos\<ano>\regulamentoDasCompeticoesCearenses.docx"
   $pdfPath = [System.IO.Path]::ChangeExtension($docPath.Path, ".pdf")
   $doc = $word.Documents.Open($docPath.Path)
   $doc.SaveAs([ref]$pdfPath, [ref]17) # 17 = wdFormatPDF
   $doc.Close()
   $word.Quit()
   [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
   Write-Output "PDF Gerado com sucesso!"
   ```

## 5. Integração CI/CD
O job `gerar-docx` de `.github/workflows/verificacao-documental.yml` já converte o `.md` da edição em elaboração em `.docx` a cada execução do CI e publica o resultado como artefato da execução. O `.pdf` fica fora do CI porque depende do Microsoft Word. A comparação do `.docx` versionado em `Documentos/<ano>/` com o recém-gerado ainda não existe: está registrada na [*issue* #18](https://github.com/Jouderian/Regulamentos-de-Orientacao/issues/18).