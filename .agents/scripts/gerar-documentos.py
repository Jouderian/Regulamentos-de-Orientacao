#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automação da compilação de documentos finais (.docx e .pdf) a partir do Markdown.

Gera só a edição em elaboração (`status: em-elaboracao` no frontmatter), na pasta
do próprio .md. O .pdf de edição vigente ou arquivada está congelado (ADR-006),
e o script recusa regenerá-lo.

Remove o bloco de metadados YAML antes de enviar ao Pandoc (garantindo que nada
do frontmatter apareça no documento final) e em seguida converte o .docx para
.pdf utilizando o Microsoft Word via COM/PowerShell.

Uso:
    python .agents/scripts/gerar-documentos.py [Documentos/<ano>/regulamentoDasCompeticoesCearenses.md]

Sem argumento, usa o regulamento em elaboração de Documentos/<ano>/.
"""
import glob
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOME = 'regulamentoDasCompeticoesCearenses'
TEMPLATE = os.path.join(RAIZ, 'Documentos', 'template_estilos.docx')


def erro(msg):
    print(f"Erro: {msg}", file=sys.stderr)
    sys.exit(1)


def ler(caminho):
    if not os.path.exists(caminho):
        erro(f"Arquivo fonte não encontrado: {caminho}")
    with open(caminho, 'r', encoding='utf-8') as fh:
        return fh.read()


def extrair_status(texto):
    m = re.search(r'(?m)^status:\s*(\S+)', texto.split('---', 2)[1] if texto.startswith('---') else '')
    return m.group(1) if m else None


def localizar_fonte(argumento):
    if argumento:
        return os.path.abspath(argumento)
    candidatos = [c for c in sorted(glob.glob(os.path.join(RAIZ, 'Documentos', '*', NOME + '.md')))
                  if extrair_status(ler(c)) == 'em-elaboracao']
    if len(candidatos) != 1:
        erro(f"esperava 1 regulamento em elaboração em Documentos/<ano>/, mas há {len(candidatos)}.")
    return candidatos[0]


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
        erro_pandoc = res.stderr.decode('utf-8', errors='replace')
        print(f"Erro ao executar Pandoc: {erro_pandoc}", file=sys.stderr)
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
        erro(f"Template de estilos não encontrado: {TEMPLATE}")

    fonte = localizar_fonte(sys.argv[1] if len(sys.argv) > 1 else None)
    rel = os.path.relpath(fonte, RAIZ)
    texto = ler(fonte)
    status = extrair_status(texto)
    if status != 'em-elaboracao':
        erro(f'{rel} está com status "{status}". O .pdf de edição vigente ou arquivada '
             f'está congelado (ADR-006) e não é regenerado.')

    pasta_destino = os.path.dirname(fonte)
    base = os.path.splitext(fonte)[0]
    docx_destino = base + '.docx'
    pdf_destino = base + '.pdf'

    gerar_docx(limpar_frontmatter(texto), docx_destino)
    gerar_pdf(docx_destino, pdf_destino)

    print(f"\nDocumentos de {os.path.basename(pasta_destino)} gerados e atualizados com sucesso:")
    print(f"  - {os.path.relpath(docx_destino, RAIZ)} ({os.path.getsize(docx_destino)} bytes)")
    print(f"  - {os.path.relpath(pdf_destino, RAIZ)} ({os.path.getsize(pdf_destino)} bytes)")


if __name__ == '__main__':
    main()
