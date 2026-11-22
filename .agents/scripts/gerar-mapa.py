#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gera o mapa de leitura de um documento longo (protótipo, ROP).

O mapa lista cada seção com id estável, título, intervalo de linhas e tamanho
estimado, para o agente ler só o trecho de que precisa. É derivado do `.md`:
nunca se edita à mão.

    python .agents/scripts/gerar-mapa.py Documentos/2026/regrasOrientacaoPedestre.md
    python .agents/scripts/gerar-mapa.py --verificar Documentos/2026/regrasOrientacaoPedestre.md

Saída: .agents/mapas/<pasta-do-ano>/<nomeBase>.md. --verificar não escreve:
sai com código 1 se o mapa estiver ausente ou defasado (hash do fonte diverge).
"""
import hashlib
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

TITULO = re.compile(r'^(#{2,6})\s+(.*?)\s*$')
CAPITULO = re.compile(r'^CAP[IÍ]TULO\s+([IVX]+)\b', re.IGNORECASE)
APENDICE = re.compile(r'^Ap[eê]ndice\s+(\d+)\b', re.IGNORECASE)
ANEXOS = re.compile(r'^ANEXOS?\b', re.IGNORECASE)
ARTIGO = re.compile(r'^Artigo\s+(\d+)\b', re.IGNORECASE)
NUMERADO = re.compile(r'^(\d+(?:\.\d+)*)\.?\s+(.*)$')
REGRA = re.compile(r'^\*\*(\d+(?:\.\d+)+)\*\*')
ROMANOS = {'I': 1, 'II': 2, 'III': 3, 'IV': 4}


def ler_texto(caminho):
    with open(caminho, 'rb') as f:
        bruto = f.read()
    return bruto.decode('utf-8').replace('\r\n', '\n')


def limpar_titulo(texto):
    texto = re.sub(r'\s*\{#[^}]*\}\s*$', '', texto)
    return re.sub(r'\s+', ' ', texto).strip()


def secoes(linhas):
    """Devolve [(nivel, id, titulo, inicio, fim, grupo)] do corpo do documento."""
    # O corpo começa no primeiro "## CAPITULO I" que não esteja no Índice.
    achados = []
    for n, texto in enumerate(linhas, 1):
        m = TITULO.match(texto)
        if m:
            achados.append((n, len(m.group(1)), limpar_titulo(m.group(2))))

    inicio_corpo = None
    for n, nivel, titulo in achados:
        if nivel == 2 and re.match(r'^CAP[IÍ]TULO I\b', titulo, re.IGNORECASE):
            inicio_corpo = n
            break
    plano = False
    if inicio_corpo is None:
        # Modo plano (ROP 2022): sem capítulos, seções "## 1. TÍTULO" direto após o Índice.
        for n, nivel, titulo in achados:
            if nivel == 2 and re.match(r'^1\.?\s+\S', titulo):
                inicio_corpo = n
                plano = True
                break
    if inicio_corpo is None:
        sys.exit('erro: não achei o início do corpo ("## CAPITULO I" ou "## 1. TÍTULO")')

    corpo = []
    for n, nivel, titulo in achados:
        if n < inicio_corpo:
            continue
        eh_grupo = bool(CAPITULO.match(titulo) or APENDICE.match(titulo) or ANEXOS.match(titulo))
        if plano:
            nivel += 1   # "## N. TÍTULO" vira seção (nível 3); "###" vira subseção
        elif nivel == 2 and not eh_grupo:
            nivel = 3   # "## 8. DISPOSIÇÕES FINAIS", "## Artigo 11": filho do apêndice
        corpo.append((n, nivel, titulo))
    resultado = []
    contexto = None   # prefixo do apêndice atual (apN) ou None nos capítulos
    grupo = None
    usados = {}

    for pos, (n, nivel, titulo) in enumerate(corpo):
        fim = len(linhas)
        for n2, nivel2, _ in corpo[pos + 1:]:
            if nivel2 <= nivel:
                fim = n2 - 1
                break

        ident = None
        if nivel == 2:
            mc = CAPITULO.match(titulo)
            ma = APENDICE.match(titulo)
            if ANEXOS.match(titulo):
                contexto = None
                grupo = ident = 'anexos'
            elif mc:
                contexto = None
                grupo = f'cap{ROMANOS.get(mc.group(1).upper(), mc.group(1))}'
                ident = grupo
            elif ma:
                contexto = f'ap{ma.group(1)}'
                grupo = contexto
                ident = contexto
        else:
            ident = filho(titulo, contexto)

        if ident is None:
            ident = f'L{n}'
        if ident in usados:
            usados[ident] += 1
            ident = f'{ident}-{usados[ident]}'
        else:
            usados[ident] = 1
        resultado.append((nivel, ident, titulo, n, fim, grupo))
    return resultado


def filho(titulo, contexto):
    ma = ARTIGO.match(titulo)
    mn = NUMERADO.match(titulo)
    if ma:
        chave = f'art{ma.group(1)}'
    elif mn:
        chave = mn.group(1)
    else:
        return None
    return f'{contexto}/{chave}' if contexto else chave


def faixa_regras(linhas, inicio, fim):
    regras = []
    for texto in linhas[inicio - 1:fim]:
        m = REGRA.match(texto)
        if m:
            regras.append(m.group(1))
    if not regras:
        return ''
    if len(regras) == 1:
        return regras[0]
    return f'{regras[0]}–{regras[-1]}'


def tokens_estimados(linhas, inicio, fim):
    chars = sum(len(t) + 1 for t in linhas[inicio - 1:fim])
    return round(chars / 3.5 / 50) * 50


def avisos_numeracao(linhas, lista):
    """Seção numerada no cabeçalho cujas regras `**N.x**` começam por outro número."""
    avisos = []
    for nivel, ident, titulo, ini, fim, grupo in lista:
        if nivel != 3 or not re.fullmatch(r'\d+', ident):
            continue
        for texto in linhas[ini - 1:fim]:
            m = REGRA.match(texto)
            if m and m.group(1).split('.')[0] != ident:
                avisos.append(f'{ini}: seção {ident} contém a regra {m.group(1)} (cabeçalho ausente?)')
                break
    for nivel, ident, titulo, ini, fim, grupo in lista:
        if nivel >= 3 and fim - ini + 1 > 600:
            avisos.append(f'{ini}: seção {ident} com {fim - ini + 1} linhas (cabeçalhos seguintes sem "###"?)')
    # Regras `**N.x**` de capítulo sem nenhuma seção N no mapa: título sem cabeçalho `###`.
    secoes_topo = {i for nv, i, *_ in lista if nv == 3 and re.fullmatch(r'\d+', i)}
    ate = max((int(i) for i in secoes_topo), default=0)
    com_regra = set()
    for numero, texto in enumerate(linhas, 1):
        m = REGRA.match(texto)
        if m and not m.group(1).startswith('0') and numero >= (lista[0][3] if lista else 0):
            com_regra.add(m.group(1).split('.')[0])
    faltam = sorted((int(n) for n in com_regra if n not in secoes_topo and int(n) < 100))
    if faltam:
        avisos.append(f'0: regras sem seção no mapa (título sem cabeçalho "###"?): {faltam}')
    return avisos


def montar_mapa(caminho, raiz=RAIZ):
    texto = ler_texto(caminho)
    linhas = texto.split('\n')
    if linhas and linhas[-1] == '':
        linhas.pop()
    sha = hashlib.sha256(texto.encode('utf-8')).hexdigest()
    rel = os.path.relpath(caminho, raiz).replace('\\', '/')

    cab = [
        '---',
        f'description: Mapa de leitura de {rel}: id, título e linhas de cada seção (gerado; não editar)',
        f'fonte: {rel}',
        f'sha256: {sha}',
        f'linhas: {len(linhas)}',
        '---',
        '',
        f'# Mapa de {os.path.basename(rel)}',
        '',
        'Gerado por `python .agents/scripts/gerar-mapa.py`. Colunas: `id | título | linhas | regras | ~tokens`.',
        'Leia só o intervalo de linhas do id escolhido (Read com offset e limit).',
        '',
    ]
    corpo = []
    lista = secoes(linhas)
    for aviso in avisos_numeracao(linhas, lista):
        print(f'aviso: {aviso}', file=sys.stderr)
    for nivel, ident, titulo, ini, fim, grupo in lista:
        if nivel == 2:
            corpo.append('')
            corpo.append(f'## {ident} — {titulo} | {ini}-{fim} | ~{tokens_estimados(linhas, ini, fim)}')
            continue
        recuo = '' if nivel <= 3 else '  '
        corpo.append(f'{recuo}{ident} | {titulo} | {ini}-{fim} | '
                     f'{faixa_regras(linhas, ini, fim)} | {tokens_estimados(linhas, ini, fim)}')
    return '\n'.join(cab + corpo) + '\n', sha


def destino(caminho, raiz=RAIZ):
    ano = os.path.basename(os.path.dirname(os.path.abspath(caminho)))
    nome = os.path.basename(caminho)
    return os.path.join(raiz, '.agents', 'mapas', ano, nome)


def main(argv):
    verificar = '--verificar' in argv
    alvos = [a for a in argv if not a.startswith('--')]
    if len(alvos) != 1:
        sys.exit(__doc__)
    caminho = os.path.abspath(alvos[0])
    if not os.path.isfile(caminho):
        sys.exit(f'erro: arquivo não encontrado: {alvos[0]}')

    mapa, sha = montar_mapa(caminho)
    saida = destino(caminho)

    if verificar:
        if not os.path.isfile(saida):
            print(f'{saida}: mapa ausente')
            return 1
        atual = re.search(r'^sha256: (\w+)$', ler_texto(saida), re.MULTILINE)
        if atual and atual.group(1) == sha:
            print('mapa em dia')
            return 0
        print(f'{saida}: mapa defasado; rode gerar-mapa.py')
        return 1

    os.makedirs(os.path.dirname(saida), exist_ok=True)
    with open(saida, 'w', encoding='utf-8', newline='\n') as f:
        f.write(mapa)
    print(f'{os.path.relpath(saida, RAIZ)}: {mapa.count(chr(10))} linhas')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
