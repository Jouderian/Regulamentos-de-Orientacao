#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Converte um PDF de regulamento em Markdown com a tipografia do projeto.

Extrai o texto com MarkItDown e aplica as regras de padronização jurídica
definidas na ADR-003 (.agents/wiki/decisions/ADR-003-historical-regulation-standardization.md):

    python .agents/scripts/import-pdf.py <caminho_do_pdf> [caminho_do_markdown_saida]

A conversão é um ponto de partida, não um resultado final: o texto gerado
precisa de revisão contra o PDF original e de aprovação em
verificar-documentos.py antes do commit.

O Markdown sai com o frontmatter exigido pelo verificador (ano, edicao,
status, rop_referencia, description). O ano vem da pasta Documentos/<ano>/ do
PDF (ou de --ano) e a edição, do numeral romano do título (ou de --edicao).
Nada disso é estimado: se um valor não puder ser identificado, o script para
e pede a opção correspondente.

Se o calendário de etapas não virar tabela, o arquivo é gravado e o script avisa
na saída de erro: a tabela se monta à mão contra o PDF.

Sai com código 1 se a conversão falhar.
"""
import argparse
import os
import re
import sys
import unicodedata

from markitdown import MarkItDown, MarkItDownException

ROMANO = r'(?=[IVXLCDM])M{0,3}(?:CM|CD|D?C{0,3})(?:XC|XL|L?X{0,3})(?:IX|IV|V?I{0,3})'
PALAVRAS_MINUSCULAS = {'a', 'o', 'as', 'os', 'da', 'de', 'do', 'das', 'dos', 'e'}
SIGLAS = {'CCO', 'CCOS', 'CBO', 'FECORI', 'ROP', 'RGOP'}
LIMITE_LINHAS_TITULO = 8

# Linhas que abrem um bloco próprio ao juntar as linhas de um artigo (_unir_linhas).
INICIO_DE_BLOCO = re.compile(r'#|\*\*Art\.|> \*\*|>> \*\*|\|')
CORPO_DE_BLOCO = re.compile(r'\*\*Art\.|> \*\*|>> \*\*')
# Inciso numérico, marcador, data de assinatura e anexo não continuam o artigo anterior.
FORA_DO_ARTIGO = re.compile(r'\d+[.)][ \t]+\S|[-•][ \t]|Fortaleza\b.*\d{4}\.?$|ANEXO\b')
# Começo de um calendário de etapas que o script não converteu em tabela.
CALENDARIO_SOLTO = re.compile(r'^(?:Etapa|ETAPA|Percurso|PERCURSO)\b[^.;:|\n]*$', re.M)
# O PDF quebra o texto na largura da página: uma linha mais curta que isso, fechada com
# pontuação, é a última do parágrafo, e a linha seguinte (assinatura, por exemplo) não a continua.
LINHA_CURTA = 60


def padronizar_texto(texto):
    # 1. Remover o timbre da Federação: o nome sozinho na linha, ou seguido do
    # "Fundada em" do timbre. O nome dentro de uma frase ("filiado à FEDERAÇÃO
    # CEARENSE DE ORIENTAÇÃO (FECORI)") é texto do regulamento e fica. O timbre
    # ocupa até três linhas, e a última começa em "Brasileira de Orientação," ou
    # "de Orientação," conforme o PDF.
    texto = re.sub(
        r'(?m)(?:^[ \t]*\x0c?[ \t]*FEDERAÇÃO CEARENSE DE ORIENTAÇÃO[ \t]*$'
        r'|\x0c?[ \t]*FEDERAÇÃO CEARENSE DE ORIENTAÇÃO(?=[ \t]+Fundada em))'
        r'(?:\s*\n\s*Fundada em [^\n]+|[ \t]+Fundada em [^\n]{0,140}?CNPJ:?[ \t]*[\d./-]+)?'
        r'(?:\s*\n\s*(?:Brasileira\s+)?(?:de\s+Orientação,\s*)?sobe?\s+o\s*CNPJ:[^\n]+)?',
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

    # 4. Remover marcas de quebra de página (\x0c) residuais e o acento combinante
    # (U+0301) que o PDF deixa depois de vogal já acentuada ("será́"). A
    # normalização antes dele funde o acento solto à vogal sem acento ("e" + U+0301).
    texto = texto.replace('\x0c', '')
    texto = unicodedata.normalize('NFC', texto).replace('́', '')

    # 5. Desfazer as letras duplicadas do negrito simulado do PDF
    texto = re.sub(r'(?m)^.*$', _desduplicar_linha, texto)

    # 6. Título: as linhas em caixa-alta do topo viram "# Título"
    texto = _montar_titulo(texto.lstrip())

    # 7. Calendário de etapas: texto solto -> tabela Markdown
    texto = re.sub(
        r'(?m)^ETAPA[ \t]+DATA[ \t]+ORGANIZADOR[ \t]*\n'
        r'((?:\d+ª[ \t]+\d{1,2}/\S+[ \t]+\S.*(?:\n|$))+)',
        _calendario,
        texto
    )

    # 8. Capítulos: CAPÍTULO IV - DAS... -> ## CAPÍTULO IV - DAS...
    # Evita duplicar o ## se já tiver
    texto = re.sub(r'(?m)^(?!#+ )(CAPÍTULO\s+[IVXLCDM\d]+.*?)$', r'## \1', texto)

    # 9. Capítulos numerados: 1. DA REGULAMENTAÇÃO GERAL -> ## 1. DA REGULAMENTAÇÃO GERAL
    # Só linhas sem minúsculas: um inciso numerado ("1. Alunos matriculados...") não é capítulo.
    # Aceita "10.DA SEGURANÇA" (sem espaço depois do ponto), que alguns PDFs trazem.
    texto = re.sub(
        r'(?m)^(\d+)\.[ \t]*((?:D[AOE]S?|ANEXO)\b[^a-zà-ÿ\n]*)$',
        r'## \1. \2',
        texto
    )

    # 10. Artigos: Art. 1º - O campeonato... -> **Art. 1º** – O campeonato...
    # Aceita "Art 8º -" (sem ponto), que vários PDFs antigos trazem.
    texto = re.sub(r'(?m)^Art\.?[ \t]*(\d+)([ºo°]?)[ \t]*[-–—][ \t]*(.*)$', _artigo, texto)

    # 11. Parágrafo único: Parágrafo único - ... -> > **Parágrafo Único:** ...
    # Suporta variações de acentuação e maiúsculas/minúsculas
    texto = re.sub(
        r'(?m)^Parágrafo\s*[uUüúÚ]n[ií]co\s*[-–—:.]\s*(.*)$',
        r'> **Parágrafo Único:** \1',
        texto
    )

    # 12. Parágrafo 1º - ... -> > **Parágrafo 1º:** ...
    texto = re.sub(r'(?m)^Parágrafo\s*(\d+)([ºo°]?)\s*[-–—:.]\s*(.*)$', _paragrafo, texto)

    # 13. Alíneas: a) Blabla e a. Blabla -> >> **a.** Blabla
    # Exige o espaço depois do ponto ou parêntese: sem ele, qualquer trecho de
    # linha iniciado por letra minúscula com esse fechamento viraria alínea.
    texto = re.sub(r'(?m)^[ \t]*([a-z])[).][ \t]+(.*)$', r'>> **\1.** \2', texto)

    # 14. Referência cruzada com ordinal em "o" ou "°" no corpo: Art. 44o -> Art. 44º
    texto = re.sub(r'\b((?:Arts?|Parágrafo)\.?[ \t]*\d+)[o°](?![\wÀ-ÿ])', r'\1º', texto)

    # 15. Um parágrafo por linha, com linha em branco entre artigos, parágrafos e alíneas
    texto = _unir_linhas(texto)

    # 16. Colapsar múltiplas linhas em branco seguidas (mais de 2 newlines)
    texto = re.sub(r'\n{3,}', '\n\n', texto)

    return texto.strip()


def _unir_linhas(texto):
    """Junta as linhas de cada artigo, parágrafo e alínea em um parágrafo só.

    O PDF quebra o texto na largura da página e o MarkItDown ainda deixa linhas em
    branco no meio das frases; o acervo guarda cada dispositivo em uma linha. O que
    não é artigo, parágrafo ou alínea (tabelas, calendário solto, assinatura, anexo)
    não é tocado: juntar esses trechos misturaria conteúdo.
    """
    saida = []
    corpo = None  # linhas do artigo, parágrafo ou alínea aberto
    for linha in texto.split('\n'):
        limpa = linha.strip()
        if corpo is not None:
            if not limpa:
                continue
            fim_do_paragrafo = len(corpo[-1]) < LINHA_CURTA and corpo[-1][-1] in '.;:!?'
            if not (fim_do_paragrafo or INICIO_DE_BLOCO.match(limpa)
                    or FORA_DO_ARTIGO.match(limpa) or CALENDARIO_SOLTO.match(limpa)):
                corpo.append(limpa)
                continue
            saida += [_juntar(corpo), '']
            corpo = None
        if CORPO_DE_BLOCO.match(limpa):
            if saida and saida[-1]:
                saida.append('')
            corpo = [limpa]
        else:
            saida.append(linha)
    if corpo is not None:
        saida.append(_juntar(corpo))
    return '\n'.join(saida)


def _juntar(linhas):
    """Une as linhas de um bloco com espaço.

    Hífen no fim da linha: a sigla composta ("SI-" e "Card") fecha sem espaço. Nos
    demais casos a quebra fica, para o verificar-documentos.py apontar a palavra
    partida ("orien-" e "tação"): só quem lê o PDF sabe se o hífen é da palavra.
    """
    texto = linhas[0]
    for linha in linhas[1:]:
        if re.search(r'(?<![-\s])-$', texto):
            texto += linha if linha[0].isupper() else '\n' + linha
        else:
            texto += ' ' + linha
    return texto


def _desduplicar_linha(match):
    """Desfaz o negrito simulado do PDF: "RREEGGUULLAAMMEENNTTOO" vira "REGULAMENTO".

    Só age na linha em que todas as letras vêm em pares (e há ao menos dois
    pares): uma palavra com letra dobrada legítima ("CLASSIFICAÇÃO") não é tocada.
    """
    linha = match.group(0)
    miolo = linha.strip()
    em_pares = re.fullmatch(r'(?:([^\W\d_])\1|[ \t])+', miolo)
    if em_pares and len(re.findall(r'([^\W\d_])\1', miolo)) >= 2:
        return re.sub(r'([^\W\d_])\1', r'\1', linha)
    return linha


def _linha_de_titulo(linha):
    """Linha em caixa-alta que não é capítulo nem anexo."""
    return (bool(linha.strip())
            and not re.search(r'[a-zà-ÿ]', linha)
            and not re.match(r'\s*(?:\d+\.|CAPÍTULO\b|ANEXO\b)', linha))


def _montar_titulo(texto):
    """Junta as linhas de título do topo ("REGULAMENTO", "DO", "X CAMPEONATO...") em `# Título`.

    Algumas linhas do título vêm separadas por linha em branco: ela não encerra o título.
    """
    linhas = texto.split('\n')
    fim = 0  # logo depois da última linha do título
    i = 0
    while i < len(linhas) and (not linhas[i].strip() or _linha_de_titulo(linhas[i])):
        if linhas[i].strip():
            fim = i + 1
        i += 1
    partes = [linha.strip() for linha in linhas[:fim] if linha.strip()]
    bloco = ' '.join(partes)
    # Exigir as duas palavras evita transformar em título uma linha qualquer em
    # caixa-alta do topo ("CNPJ – 07.360.881/0001-09") ou só metade dele.
    if len(partes) > LIMITE_LINHAS_TITULO or 'REGULAMENTO' not in bloco or 'CAMPEONATO' not in bloco:
        return texto
    return '\n'.join(['# ' + _caixa_de_titulo(bloco), ''] + linhas[fim:])


def _caixa_de_titulo(texto):
    """REGULAMENTO DO X CAMPEONATO -> Regulamento do X Campeonato (numerais romanos e siglas ficam)."""
    palavras = []
    for i, palavra in enumerate(texto.split()):
        if re.fullmatch(ROMANO, palavra) or palavra in SIGLAS:
            palavras.append(palavra)
        elif i > 0 and palavra.lower() in PALAVRAS_MINUSCULAS:
            palavras.append(palavra.lower())
        else:
            palavras.append(palavra.capitalize())
    return ' '.join(palavras)


def _calendario(match):
    linhas = ['| Etapa | Data | Organizador |', '| :--- | :--- | :--- |']
    for linha in match.group(1).strip().split('\n'):
        etapa, data, organizador = linha.split(None, 2)
        linhas.append(f'| {etapa} | {data} | {organizador.strip()} |')
    return '\n' + '\n'.join(linhas) + '\n\n'


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
    # Técnica legislativa (LC 95/1998, art. 10, I; ADR-003): ordinal até o 9º, cardinal do 10 em diante.
    sufixo = '' if int(num) >= 10 else _ordinal(num, sufixo, sempre=True)
    return f'**Art. {num}{sufixo}** – {conteudo}'


def _paragrafo(match):
    num, sufixo, conteudo = match.groups()
    return f'> **Parágrafo {num}{_ordinal(num, sufixo, sempre=True)}:** {conteudo}'


def extrair_titulo(markdown):
    """Devolve o texto do `# Título` do topo, ou None se o PDF não trouxe título identificável."""
    m = re.match(r'# (.+)', markdown)
    return m.group(1).strip() if m else None


def identificar_edicao(titulo, pdf):
    """"Regulamento do X Campeonato..." em regulamentoCCO.pdf -> "X CCO"; None se não houver numeral."""
    if not titulo:
        return None
    m = re.search(r'\b(' + ROMANO + r')\s+Campeonato\b', titulo)
    if not m:
        return None
    sprint = 'Sprint' in titulo or 'CCOS' in os.path.basename(pdf)
    return f'{m.group(1)} {"CCOS" if sprint else "CCO"}'


def identificar_ano(pdf):
    """Ano da pasta Documentos/<ano>/ que contém o PDF; None se o PDF estiver fora do acervo."""
    pasta = os.path.basename(os.path.dirname(os.path.abspath(pdf)))
    return pasta if re.fullmatch(r'\d{4}', pasta) else None


def montar_frontmatter(titulo, ano, edicao, rop_referencia):
    descricao = f'{titulo} ({ano})' if titulo else f'Regulamento {edicao} ({ano})'
    return (
        '---\n'
        f'ano: {ano}\n'
        f'edicao: {edicao}\n'
        'status: arquivado\n'
        f'rop_referencia: {rop_referencia}\n'
        f'description: {descricao}\n'
        '---\n\n'
    )


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
    parser.add_argument(
        '--ano',
        help='ano da edição (padrão: pasta Documentos/<ano>/ do PDF)',
    )
    parser.add_argument(
        '--edicao',
        help='edição, como "X CCO" (padrão: numeral romano do título do PDF)',
    )
    parser.add_argument(
        '--rop-referencia',
        help='ano da ROP citada pelo regulamento (padrão: o próprio ano da edição)',
    )
    parser.add_argument(
        '--sem-frontmatter',
        action='store_true',
        help='não gera o frontmatter (para documentos que não são regulamento de competição)',
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

    if not args.sem_frontmatter:
        titulo = extrair_titulo(markdown)
        ano = args.ano or identificar_ano(args.pdf)
        edicao = args.edicao or identificar_edicao(titulo, args.pdf)
        # Ano e edição são fatos normativos: nunca se estimam.
        for valor, opcao, origem in (
                (ano, '--ano', 'da pasta Documentos/<ano>/ do PDF'),
                (edicao, '--edicao', 'do numeral romano do título')):
            if not valor:
                print(f'Erro: não foi possível obter o valor de {opcao[2:]} {origem}. '
                      f'Informe {opcao} (ou use --sem-frontmatter).', file=sys.stderr)
                return 1
        markdown = montar_frontmatter(
            titulo, ano, edicao, args.rop_referencia or ano) + markdown

    # Calendário que o script não reconheceu (colunas em linhas separadas, célula
    # mesclada): sem aviso, o trecho sairia como texto solto e passaria despercebido.
    if CALENDARIO_SOLTO.search(markdown):
        print('Aviso: o calendário de etapas não virou tabela; monte-o à mão contra o PDF.',
              file=sys.stderr)

    try:
        # newline='\n': no Windows o padrão gravaria CRLF; o repositório usa LF.
        with open(saida, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(markdown + '\n')
    except OSError as erro:
        print(f'Erro ao gravar {saida}: {erro}', file=sys.stderr)
        return 1

    print(f'Sucesso! Arquivo salvo em: {saida}')
    print('Revise o resultado contra o PDF original antes do commit.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
