#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Converte um PDF de regulamento em Markdown com a tipografia do projeto.

Extrai o texto com MarkItDown e aplica as regras de padronização jurídica
definidas na ADR-003 (.agents/wiki/decisions/ADR-003-historical-regulation-standardization.md):

    python .agents/scripts/import-pdf.py <caminho_do_pdf> [caminho_do_markdown_saida]

A conversão é um ponto de partida, não um resultado final: o texto gerado
precisa de revisão contra o PDF original e de aprovação em
verificar-documentos.py antes do commit.

Sai com código 1 se a conversão falhar.
"""
import argparse
import os
import re
import sys

from markitdown import MarkItDown, MarkItDownException


def padronizar_texto(texto):
    # 1. Remover cabeçalhos da Federação
    texto = re.sub(
        r'\x0c?\s*FEDERAÇÃO CEARENSE DE ORIENTAÇÃO'
        r'(?:\s*\n\s*Fundada em [^\n]+)?'
        r'(?:\s*\n\s*(?:de Orientação,\s*)?sob o\s*CNPJ:[^\n]+)?',
        '',
        texto
    )

    # 2. Remover rodapés da Federação (FECORI e CBO) de forma independente por linha
    texto = re.sub(r'(?m)^\s*www\.fecori\.org\.br\s*$', '', texto)
    texto = re.sub(r'(?m)^\s*(?:~\s*)?\d+\s*/\s*\d+\s*(?:~\s*)?$', '', texto)
    texto = re.sub(r'(?m)^\s*\d{2}/\d{2}/\d{2,4}\s*\d{2}:\d{2}\s*$', '', texto)
    texto = re.sub(
        r'(?m)^\s*Confederação Brasileira de Orientação\s*[-–—]\s*CBO'
        r'\s*[-–—]\s*www\.cbo\.esp\.br\s*\d+\s*$',
        '',
        texto
    )

    # 3. Remover espaços duplos ou múltiplos entre palavras (preservando indentação de início de linha)
    texto = re.sub(r'(?<=\S)[ \t]{2,}', ' ', texto)

    # 4. Remover marcas de quebra de página (\x0c) residuais
    texto = texto.replace('\x0c', '')

    # 5. Capítulos: CAPÍTULO IV - DAS... -> ## CAPÍTULO IV - DAS...
    # Evita duplicar o ## se já tiver
    texto = re.sub(r'(?m)^(?!#+ )(CAPÍTULO\s+[IVXLCDM\d]+.*?)$', r'## \1', texto)

    # 6. Artigos: Art. 1º - O campeonato... -> **Art. 1º** – O campeonato...
    texto = re.sub(r'(?m)^Art\.\s*(\d+)([ºo°]?)\s*[-–—]\s*(.*)$', _artigo, texto)

    # 7. Parágrafo único: Parágrafo Único - ... -> > **Parágrafo único:** ...
    # Suporta variações de acentuação e maiúsculas/minúsculas
    texto = re.sub(
        r'(?m)^Parágrafo\s*[uUüúÚ]n[ií]co\s*[-–—:]\s*(.*)$',
        r'> **Parágrafo único:** \1',
        texto
    )

    # 8. Parágrafo 1º - ... -> > **Parágrafo 1º:** ...
    texto = re.sub(r'(?m)^Parágrafo\s*(\d+)([ºo°]?)\s*[-–—:]\s*(.*)$', _paragrafo, texto)

    # 9. Alíneas: a) Blabla -> >> **a)** Blabla
    # Exige o espaço depois do parêntese: sem ele, qualquer trecho de linha
    # iniciado por letra minúscula com parêntese de fechamento viraria alínea.
    texto = re.sub(r'(?m)^[ \t]*([a-z])\)[ \t]+(.*)$', r'>> **\1)** \2', texto)

    # 10. Colapsar múltiplas linhas em branco seguidas (mais de 2 newlines)
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    return texto.strip()


def _ordinal(num, sufixo, sempre=False):
    """Normaliza o indicador de ordinal: 1o e 1° viram 1º.

    Com `sempre`, acrescenta o indicador ausente nos ordinais de 1 a 9
    (a forma usada nos parágrafos: "Parágrafo 1º", nunca "Parágrafo 1").
    """
    if sufixo in ('o', '°'):
        return 'º'
    if not sufixo and sempre and int(num) < 10:
        return 'º'
    return sufixo


def _artigo(match):
    num, sufixo, conteudo = match.groups()
    return f'**Art. {num}{_ordinal(num, sufixo)}** – {conteudo}'


def _paragrafo(match):
    num, sufixo, conteudo = match.groups()
    return f'> **Parágrafo {num}{_ordinal(num, sufixo, sempre=True)}:** {conteudo}'


def analisar_argumentos(argv):
    parser = argparse.ArgumentParser(
        prog='import-pdf.py',
        description='Converte um PDF de regulamento em Markdown com a tipografia '
                    'jurídica do projeto (ADR-003).',
        epilog='O Markdown gerado é um rascunho: revise contra o PDF original e '
               'rode verificar-documentos.py antes do commit.',
    )
    parser.add_argument(
        'pdf',
        help='caminho do PDF de entrada',
    )
    parser.add_argument(
        'saida',
        nargs='?',
        help='caminho do Markdown de saída (padrão: mesmo nome do PDF, com .md)',
    )
    return parser.parse_args(argv)


def main(argv=None):
    args = analisar_argumentos(argv)

    if not os.path.isfile(args.pdf):
        print(f'Erro: arquivo {args.pdf} não encontrado.', file=sys.stderr)
        return 1

    saida = args.saida or os.path.splitext(args.pdf)[0] + '.md'

    print(f'Convertendo {args.pdf} usando MarkItDown...')
    try:
        resultado = MarkItDown().convert(args.pdf)
    except MarkItDownException as erro:
        print(f'Erro na extração do PDF: {erro!r}', file=sys.stderr)
        return 1

    print('Aplicando regras de padronização jurídica...')
    markdown = padronizar_texto(resultado.text_content)

    # PDF escaneado não tem camada de texto: a extração devolve vazio sem
    # levantar erro. Gravar esse nada como "sucesso" esconderia a falha.
    if not markdown:
        print(f'Erro: nenhum texto extraído de {args.pdf}. O PDF provavelmente é '
              'escaneado (sem camada de texto) — veja a nota sobre OCR em '
              '.agents/workflows/import-pdf.md.', file=sys.stderr)
        return 1

    try:
        with open(saida, 'w', encoding='utf-8') as fh:
            fh.write(markdown + '\n')
    except OSError as erro:
        print(f'Erro ao gravar {saida}: {erro}', file=sys.stderr)
        return 1

    print(f'Sucesso! Arquivo salvo em: {saida}')
    print('Revise o resultado contra o PDF original antes do commit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
