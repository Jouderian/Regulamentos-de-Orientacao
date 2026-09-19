#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automação da compilação de documentos finais (.docx e .pdf) a partir do Markdown.

Remove o bloco de metadados YAML antes de enviar ao Pandoc (garantindo que nada
do frontmatter apareça no documento final) e em seguida converte o .docx para
.pdf utilizando o Microsoft Word via COM/PowerShell.

Uso:
    python .agents/scripts/gerar-documentos.py
"""
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FONTE = os.path.join(RAIZ, 'regulamentoDasCompeticoesCearenses.md')
TEMPLATE = os.path.join(RAIZ, 'Documentos', 'template_estilos.docx')


def ler_fonte():
    if not os.path.exists(FONTE):
        print(f"Erro: Arquivo fonte não encontrado: {FONTE}", file=sys.stderr)
        sys.exit(1)
    with open(FONTE, 'r', encoding='utf-8') as fh:
        return fh.read()


def extrair_ano(texto):
    m = re.search(r'(?m)^ano:\s*(\d{4})', texto)
    if m:
        return m.group(1)
    print("Aviso: Campo 'ano' não encontrado no frontmatter. Usando 2027 como padrão.")
    return '2027'


def limpar_frontmatter(texto):
    """Remove o bloco YAML frontmatter no topo do documento."""
    return re.sub(r'(?s)^---\r?\n.*?\r?\n---\r?\n', '', texto)


def gerar_docx(conteudo_md, docx_path):
    print(f"Compilando DOCX via Pandoc -> {docx_path}")
    os.makedirs(os.path.dirname(docx_path), exist_ok=True)
    cmd = [
        'pandoc',
        '-f', 'markdown',
        '-t', 'docx',
        '-o', docx_path,
        f'--reference-doc={TEMPLATE}'
    ]
    res = subprocess.run(
        cmd,
        input=conteudo_md.encode('utf-8'),
        capture_output=True
    )
    if res.returncode != 0:
        erro = res.stderr.decode('utf-8', errors='replace')
        print(f"Erro ao executar Pandoc: {erro}", file=sys.stderr)
        sys.exit(res.returncode)
    print("DOCX gerado com sucesso.")


def gerar_pdf(docx_path, pdf_path):
    print(f"Convertendo DOCX para PDF via Word -> {pdf_path}")
    # Normaliza caminhos com barras invertidas para o PowerShell
    docx_win = os.path.abspath(docx_path).replace('/', '\\')
    pdf_win = os.path.abspath(pdf_path).replace('/', '\\')

    ps_script = f"""
$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {{
    $doc = $word.Documents.Open('{docx_win}')
    $doc.SaveAs([ref]'{pdf_win}', [ref]17)
    $doc.Close()
}} finally {{
    $word.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($word) | Out-Null
}}
"""
    res = subprocess.run(
        ['powershell', '-NoProfile', '-ExecutionPolicy', 'Bypass', '-Command', ps_script],
        capture_output=True,
        text=True
    )
    if res.returncode != 0:
        print(f"Erro ao converter para PDF: {res.stderr}", file=sys.stderr)
        sys.exit(res.returncode)
    print("PDF gerado com sucesso.")


def main():
    if not os.path.exists(TEMPLATE):
        print(f"Erro: Template de estilos não encontrado: {TEMPLATE}", file=sys.stderr)
        sys.exit(1)

    texto = ler_fonte()
    ano = extrair_ano(texto)
    conteudo_limpo = limpar_frontmatter(texto)

    pasta_destino = os.path.join(RAIZ, 'Documentos', ano)
    docx_destino = os.path.join(pasta_destino, 'regulamentoDasCompeticoesCearenses.docx')
    pdf_destino = os.path.join(pasta_destino, 'regulamentoDasCompeticoesCearenses.pdf')

    gerar_docx(conteudo_limpo, docx_destino)
    gerar_pdf(docx_destino, pdf_destino)

    print(f"\nDocumentos de {ano} gerados e atualizados com sucesso:")
    print(f"  - {os.path.relpath(docx_destino, RAIZ)} ({os.path.getsize(docx_destino)} bytes)")
    print(f"  - {os.path.relpath(pdf_destino, RAIZ)} ({os.path.getsize(pdf_destino)} bytes)")


if __name__ == '__main__':
    main()
