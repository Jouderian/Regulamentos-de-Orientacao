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

## 3. Passo a Passo da Geração do Arquivo Final

Sempre que o documento `regulamentoCompeticoesCearenses.md` for alterado e o conteúdo final estiver aprovado, execute o comando abaixo na raiz do repositório para sobrescrever/atualizar a versão do ano correspondente (ex: 2026):

```powershell
pandoc regulamentoCompeticoesCearenses.md -o Documentos/2026/regulamentoDasCompeticoesCearenses.docx --reference-doc=Documentos/template_estilos.docx
```

## 4. Geração do PDF a partir do DOCX

O Pandoc não aplica o template `.docx` diretamente ao gerar um `.pdf`. Por isso, a forma correta e automatizada de gerar um PDF idêntico ao molde original é: primeiro gerar o `.docx` (passo 3), e em seguida convertê-lo em PDF utilizando o próprio Microsoft Word de forma invisível via PowerShell.

Execute o script PowerShell abaixo para converter o arquivo final `.docx` em `.pdf`:

```powershell
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$docPath = Resolve-Path "Documentos\2026\regulamentoDasCompeticoesCearenses.docx"
$pdfPath = [System.IO.Path]::ChangeExtension($docPath.Path, ".pdf")
$doc = $word.Documents.Open($docPath.Path)
$doc.SaveAs([ref]$pdfPath, [ref]17) # 17 = wdFormatPDF
$doc.Close()
$word.Quit()
[System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
Write-Output "PDF Gerado com sucesso!"
```

## 5. Integração CI/CD (Melhoria Futura)
Atualmente a geração é um processo manual documentado (Local CLI). O objetivo para o projeto é que esse script seja futuramente integrado em um workflow do **GitHub Actions**. Assim, ao aprovar um *Pull Request* na branch `main`, a compilação do `.docx` ocorrerá nos servidores do GitHub e será anexada automaticamente como um "Release".