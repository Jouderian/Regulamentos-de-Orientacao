#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Automação da compilação de documentos finais (.docx e .pdf) a partir do Markdown.

Gera só a edição em elaboração (`status: em-elaboracao` no frontmatter), na pasta
do próprio .md. O .pdf de edição vigente ou arquivada está congelado (ADR-006),
e o script recusa regenerá-lo. Roda só na publicação da edição
(.agents/workflows/publicar-edicao.md): durante a elaboração, o regulamento
existe só como .md.

Remove o bloco de metadados YAML antes de enviar ao Pandoc (garantindo que nada
do frontmatter apareça no documento final) e em seguida converte o .docx para
.pdf utilizando o Microsoft Word via COM/PowerShell.

Normativo (`.md` em Documentos/normativos/, ADR-008): aceita `em-elaboracao` ou
`vigente`, regenera o .pdf a cada execução (não é congelado) e não mantém o
.docx, que fica só como intermediário temporário.

Uso:
    python .agents/scripts/gerar-documentos.py [Documentos/<ano>/regulamentoDasCompeticoesCearenses.md]
    python .agents/scripts/gerar-documentos.py Documentos/normativos/<norma>.md

Sem argumento, usa o regulamento em elaboração de Documentos/<ano>/.
"""
import glob
import os
import re
import subprocess
import sys
import tempfile

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NOME = 'regulamentoDasCompeticoesCearenses'
TEMPLATE = os.path.join(RAIZ, 'Documentos', 'template_estilos.docx')
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def erro(msg):
    print(f"Erro: {msg}", file=sys.stderr)
    sys.exit(1)


def ler(caminho):
    if not os.path.exists(caminho):
        erro(f"Arquivo fonte não encontrado: {caminho}")
    with open(caminho, 'r', encoding='utf-8') as fh:
        return fh.read()


def eh_normativo(fonte):
    """Normativo (ADR-008): `.md` direto em Documentos/normativos/."""
    pasta = os.path.dirname(os.path.abspath(fonte))
    return (fonte.lower().endswith('.md')
            and os.path.basename(pasta) == 'normativos'
            and os.path.dirname(pasta) == os.path.join(RAIZ, 'Documentos'))


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


# --------------------------------------------------------------------------
# Formatação do normativo (ADR-008). O Pandoc entrega o texto com o molde
# `template_estilos.docx`, mas a diagramação para leitura humana (texto
# justificado, título centralizado em versalete, alíneas e parágrafos com recuo,
# tabelas em azul com listras, Anexos em páginas próprias) era feita à mão no
# Word. `formatar_normativo` aplica esse acabamento ao .docx antes da conversão
# para .pdf, sem alterar o texto.
# --------------------------------------------------------------------------
ESTILO_TABELA = 'TabeladeLista4-nfase1'
ESTILO_TABELA_XML = (
    '<w:style xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'w:type="table" w:styleId="TabeladeLista4-nfase1"><w:name w:val="List Table 4 Accent 1"/>'
    '<w:basedOn w:val="Tabelanormal"/><w:uiPriority w:val="49"/><w:pPr><w:spacing w:after="0"/></w:pPr>'
    '<w:tblPr><w:tblStyleRowBandSize w:val="1"/><w:tblStyleColBandSize w:val="1"/><w:tblBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="45B0E1" w:themeColor="accent1" w:themeTint="99"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="45B0E1" w:themeColor="accent1" w:themeTint="99"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="45B0E1" w:themeColor="accent1" w:themeTint="99"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="45B0E1" w:themeColor="accent1" w:themeTint="99"/>'
    '<w:insideH w:val="single" w:sz="4" w:space="0" w:color="45B0E1" w:themeColor="accent1" w:themeTint="99"/>'
    '</w:tblBorders></w:tblPr>'
    '<w:tblStylePr w:type="firstRow"><w:rPr><w:b/><w:bCs/><w:color w:val="FFFFFF" w:themeColor="background1"/></w:rPr>'
    '<w:tblPr/><w:tcPr><w:tcBorders>'
    '<w:top w:val="single" w:sz="4" w:space="0" w:color="156082" w:themeColor="accent1"/>'
    '<w:left w:val="single" w:sz="4" w:space="0" w:color="156082" w:themeColor="accent1"/>'
    '<w:bottom w:val="single" w:sz="4" w:space="0" w:color="156082" w:themeColor="accent1"/>'
    '<w:right w:val="single" w:sz="4" w:space="0" w:color="156082" w:themeColor="accent1"/>'
    '<w:insideH w:val="nil"/></w:tcBorders>'
    '<w:shd w:val="clear" w:color="auto" w:fill="156082" w:themeFill="accent1"/></w:tcPr></w:tblStylePr>'
    '<w:tblStylePr w:type="band1Horz"><w:tblPr/><w:tcPr>'
    '<w:shd w:val="clear" w:color="auto" w:fill="C1E4F5" w:themeFill="accent1" w:themeFillTint="33"/>'
    '</w:tcPr></w:tblStylePr></w:style>'
)
RECUO_PARAGRAFO = 284   # twips: "Parágrafo 1º: ..."
RECUO_ALINEA = 567      # twips: "a. ...", com 283 de deslocamento (hanging)
DESLOC_ALINEA = 283


def _largura_util_twips(doc):
    sec = doc.sections[0]
    return int((sec.page_width - sec.left_margin - sec.right_margin) / 635)


def _pesos_colunas(tabela):
    """Peso de cada coluna: o maior entre a palavra mais longa e o conteúdo mais longo (até 38 caracteres)."""
    pesos = []
    for c in range(len(tabela.columns)):
        textos = [row.cells[c].text.strip() for row in tabela.rows]
        palavra = max((len(w) for t in textos for w in t.split()), default=1)
        longo = max((len(t) for t in textos), default=1)
        pesos.append(max(palavra + 3, min(longo, 38)))
    return pesos


def _formatar_tabela(tabela, largura):
    from docx.oxml import parse_xml
    from docx.oxml.ns import qn
    tbl = tabela._tbl
    tbl_pr = tbl.tblPr
    for tag in ('w:tblStyle', 'w:tblW', 'w:tblLayout', 'w:tblLook'):
        for el in tbl_pr.findall(qn(tag)):
            tbl_pr.remove(el)
    novos = [
        parse_xml(f'<w:tblStyle xmlns:w="{W_NS}" w:val="{ESTILO_TABELA}"/>'),
        parse_xml(f'<w:tblW xmlns:w="{W_NS}" w:w="5000" w:type="pct"/>'),
        parse_xml(f'<w:tblLayout xmlns:w="{W_NS}" w:type="fixed"/>'),
        parse_xml(f'<w:tblLook xmlns:w="{W_NS}" w:val="0420" w:firstRow="1" w:lastRow="0" '
                  'w:firstColumn="0" w:lastColumn="0" w:noHBand="0" w:noVBand="1"/>'),
    ]
    for el in reversed(novos):
        tbl_pr.insert(0, el)
    pesos = _pesos_colunas(tabela)
    larguras = [int(largura * p / sum(pesos)) for p in pesos]
    grade = tbl.find(qn('w:tblGrid'))
    for gc, w in zip(grade.findall(qn('w:gridCol')), larguras):
        gc.set(qn('w:w'), str(w))
    for row in tabela.rows:
        for cell, w in zip(row.cells, larguras):
            tc_pr = cell._tc.get_or_add_tcPr()
            for el in tc_pr.findall(qn('w:tcW')):
                tc_pr.remove(el)
            tc_pr.insert(0, parse_xml(f'<w:tcW xmlns:w="{W_NS}" w:w="{w}" w:type="dxa"/>'))


def _garantir_estilo_tabela(doc):
    from docx.oxml import parse_xml
    from docx.oxml.ns import qn
    estilos = doc.styles.element
    existe = any(s.get(qn('w:styleId')) == ESTILO_TABELA for s in estilos.findall(qn('w:style')))
    if not existe:
        estilos.append(parse_xml(ESTILO_TABELA_XML))


def formatar_normativo(docx_path):
    """Aplica ao .docx do normativo a diagramação de leitura humana (ver comentário da seção)."""
    try:
        import docx
        from docx.enum.text import WD_ALIGN_PARAGRAPH
        from docx.shared import Pt, Twips
    except ImportError:
        erro("formatar o normativo exige a biblioteca python-docx: pip install python-docx")

    doc = docx.Document(docx_path)
    largura = _largura_util_twips(doc)
    estilos_texto = {'first paragraph', 'body text', 'compact', 'block text'}
    primeiro_anexo = True
    titulo_feito = False

    for p in doc.paragraphs:
        estilo = (p.style.name or '').lower()
        texto = p.text.strip()
        tem_marcador = p._p.pPr is not None and p._p.pPr.numPr is not None

        if estilo == 'heading 1' and not titulo_feito:
            titulo_feito = True
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.paragraph_format.space_after = Twips(360)
            for r in p.runs:
                r.font.bold = True
                r.font.small_caps = True
            continue

        if estilo == 'heading 2':
            if texto.startswith('Anexo'):
                for r in p.runs:
                    r.font.small_caps = True
                if primeiro_anexo or 'Termo' in texto:
                    p.paragraph_format.page_break_before = True
                primeiro_anexo = False
            continue

        if estilo not in estilos_texto:
            continue

        if texto.startswith('Termo ') and p.runs and all(r.bold for r in p.runs if r.text.strip()):
            for r in p.runs:
                r.font.small_caps = True
                r.font.size = Pt(14)

        # Quebra de linha manual dentro de parágrafo justificado estica a linha anterior: fica à esquerda.
        # O mesmo vale para linha de preenchimento (sublinhados seguidos), que não quebra e deixa a anterior esticada.
        com_quebra = bool(p._p.xpath('.//w:br[not(@w:type="page")]')) or re.search(r'_{8,}', texto)
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT if com_quebra else WD_ALIGN_PARAGRAPH.JUSTIFY
        # Linha de assinatura escrita como "> ___" dentro de item de lista sai com o ">" literal: o sinal é descartado.
        for anterior, r in zip(p.runs, p.runs[1:]):
            if r.text.startswith('> ') and anterior._r.xpath('.//w:br'):
                r.text = r.text[2:]
        pf = p.paragraph_format
        if estilo == 'block text':
            pf.right_indent = Twips(0)
            if re.match(r'^[a-z]\.\s', texto) and len(p.runs) > 1 and p.runs[1].text.strip() == '':
                pf.left_indent = Twips(RECUO_ALINEA)
                pf.first_line_indent = Twips(-DESLOC_ALINEA)
                p.runs[1].text = '\t'
            elif texto.startswith('Nota:'):
                pf.left_indent = Twips(0)
            elif texto.startswith('Parágrafo'):
                pf.left_indent = Twips(RECUO_PARAGRAFO)
            else:
                pf.left_indent = Twips(RECUO_ALINEA)
        elif tem_marcador:
            pf.left_indent = Twips(RECUO_ALINEA)
            pf.first_line_indent = Twips(-DESLOC_ALINEA)

    _garantir_estilo_tabela(doc)
    for tabela in doc.tables:
        if len(tabela.columns) >= 3:
            _formatar_tabela(tabela, largura)

    doc.save(docx_path)
    print("Diagramação do normativo aplicada ao DOCX.")


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
    if eh_normativo(fonte):
        if status not in ('em-elaboracao', 'vigente'):
            erro(f'{rel} está com status "{status}" (esperado: "em-elaboracao" ou "vigente").')
    elif status != 'em-elaboracao':
        erro(f'{rel} está com status "{status}". O .pdf de edição vigente ou arquivada '
             f'está congelado (ADR-006) e não é regenerado.')

    pasta_destino = os.path.dirname(fonte)
    base = os.path.splitext(fonte)[0]
    docx_destino = base + '.docx'
    pdf_destino = base + '.pdf'

    if eh_normativo(fonte):
        # Normativo (ADR-008): só o .pdf fica no acervo; o .docx é intermediário descartável.
        with tempfile.TemporaryDirectory() as tmp:
            docx_tmp = os.path.join(tmp, os.path.basename(docx_destino))
            gerar_docx(limpar_frontmatter(texto), docx_tmp)
            formatar_normativo(docx_tmp)
            gerar_pdf(docx_tmp, pdf_destino)
        print(f"\nPDF do normativo gerado e atualizado com sucesso (status: {status}):")
        print(f"  - {os.path.relpath(pdf_destino, RAIZ)} ({os.path.getsize(pdf_destino)} bytes)")
        return

    gerar_docx(limpar_frontmatter(texto), docx_destino)
    gerar_pdf(docx_destino, pdf_destino)

    print(f"\nDocumentos de {os.path.basename(pasta_destino)} gerados e atualizados com sucesso:")
    print(f"  - {os.path.relpath(docx_destino, RAIZ)} ({os.path.getsize(docx_destino)} bytes)")
    print(f"  - {os.path.relpath(pdf_destino, RAIZ)} ({os.path.getsize(pdf_destino)} bytes)")


if __name__ == '__main__':
    main()
