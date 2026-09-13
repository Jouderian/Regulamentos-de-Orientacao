#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificações automáticas de integridade documental do repositório.

Executado pelo CI (.github/workflows/verificacao-documental.yml) e localmente:

    python .agents/scripts/verificar-documentos.py

Sai com código 1 se encontrar qualquer problema.
"""
import os
import re
import sys
from collections import Counter
from urllib.parse import unquote

RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
problemas = []


def falha(arquivo, linha, msg):
    local = f"{arquivo}:{linha}" if linha else arquivo
    problemas.append(f"{local}: {msg}")


def arquivos_md():
    for raiz, dirs, nomes in os.walk(RAIZ):
        dirs[:] = [d for d in dirs if d not in ('.git', '.github', '__pycache__')]
        for n in sorted(nomes):
            if n.endswith('.md'):
                caminho = os.path.join(raiz, n)
                yield os.path.relpath(caminho, RAIZ).replace('\\', '/'), caminho


def ler(caminho):
    with open(caminho, encoding='utf-8') as fh:
        return fh.read()


def linha_de(texto, pos):
    return texto.count('\n', 0, pos) + 1


# --------------------------------------------------------------------------
# 1. Links relativos precisam existir; caminhos absolutos são proibidos.
# --------------------------------------------------------------------------
def checar_links(rel, texto):
    base = os.path.dirname(os.path.join(RAIZ, rel))
    for m in re.finditer(r'\[[^\]]*\]\(([^)\s]+)', texto):
        link = m.group(1)
        if link.startswith(('http://', 'https://', 'mailto:', '#')):
            continue
        if link.startswith('file:') or re.match(r'^[a-zA-Z]:[\\/]', link):
            falha(rel, linha_de(texto, m.start()),
                  f'caminho absoluto/local em link: {link}')
            continue
        alvo = unquote(link.split('#')[0])
        if alvo and not os.path.exists(os.path.normpath(os.path.join(base, alvo))):
            falha(rel, linha_de(texto, m.start()), f'link relativo inexistente: {link}')


# --------------------------------------------------------------------------
# 2. Artefatos de conversão de PDF/DOCX.
# --------------------------------------------------------------------------
def checar_artefatos(rel, texto):
    for m in re.finditer('­', texto):
        falha(rel, linha_de(texto, m.start()), 'hífen condicional invisível (U+00AD)')
    if texto.startswith('﻿'):
        falha(rel, 1, 'arquivo inicia com BOM (U+FEFF)')
    for m in re.finditer(' ', texto):
        falha(rel, linha_de(texto, m.start()), 'espaço não separável (U+00A0)')
    # Palavra partida por hifenização de fim de linha ("orien-\ntação").
    for m in re.finditer(r'(?<![-\s])-\r?\n(?=[a-zà-ÿ])', texto):
        falha(rel, linha_de(texto, m.start()),
              'palavra partida por hifenização de fim de linha')
    for m in re.finditer(r'Paragrafo', texto):
        falha(rel, linha_de(texto, m.start()), '"Paragrafo" sem acento')
    for m in re.finditer(r'(?:Parágrafo |Art\. )\d+o\b', texto):
        falha(rel, linha_de(texto, m.start()), f'ordinal sem indicador: {m.group(0)!r}')


# --------------------------------------------------------------------------
# 3. Tipografia jurídica dos regulamentos (ADR-003).
# --------------------------------------------------------------------------
def checar_tipografia(rel, texto):
    nome = os.path.basename(rel)
    if not nome.startswith(('regulamentoCCO', 'regulamentoCompeticoes')):
        return
    for m in re.finditer(r'(?m)^\*\*Art\.? ?\d+.{0,3}?\*\*(?! – \S)(.{0,20})', texto):
        falha(rel, linha_de(texto, m.start()),
              f'artigo fora do padrão "**Art. Nº** – Texto": {m.group(0)[:40]!r}')


# --------------------------------------------------------------------------
# 4. Frontmatter obrigatório em .agents/ (regra de .agents/rules/rules.md).
# --------------------------------------------------------------------------
def checar_frontmatter(rel, texto):
    if not rel.startswith('.agents/'):
        return
    if not texto.startswith('---'):
        falha(rel, 1, 'arquivo em .agents/ sem YAML frontmatter')
        return
    cabecalho = texto.split('---', 2)[1] if texto.count('---') >= 2 else ''
    if not re.search(r'(?m)^description:\s*\S', cabecalho):
        falha(rel, 1, 'frontmatter sem campo "description" preenchido')


# --------------------------------------------------------------------------
# 5. Coerência do quadro de medalhas de clubesCampeoes.md.
# --------------------------------------------------------------------------
SEM_PODIO = ('-', 'Não publicado', 'Em andamento', 'Não realizado', 'Sem premiação')
ROTULO = {0: 'Campeão', 1: 'Vice-Campeão', 2: '3º Lugar'}


def _tabela_apos(texto, titulo):
    """Devolve as linhas de dados da primeira tabela após o título dado.

    O título é casado como linha inteira: sem isso, "### Campeonato ..." casaria
    dentro de "#### Campeonato ...", lendo a tabela errada.
    """
    m = re.search(r'(?m)^' + re.escape(titulo) + r'\s*$', texto)
    if not m:
        return []
    linhas = []
    for linha in texto[m.start():].split('\n')[1:]:
        if linha.startswith('|'):
            if re.match(r'^\|[\s:|-]+\|?$', linha):
                continue
            linhas.append([c.strip() for c in linha.strip().strip('|').split('|')])
        elif linhas:
            break
    return linhas


def _limpar(celula):
    return celula.replace('*', '').strip()


def _apurar_por_ano(texto, titulo, modalidade):
    """Conta títulos por clube a partir da tabela geral de campeões (uma linha por ano)."""
    contagem = Counter()
    linhas = _tabela_apos(texto, titulo)
    if not linhas:
        falha('clubesCampeoes.md', None,
              f'tabela geral de campeões do {modalidade} não encontrada')
        return contagem
    for celulas in linhas:
        if len(celulas) < 5 or celulas[0].lower() == 'ano':
            continue
        for pos, coluna in enumerate(celulas[2:5]):
            clube = _limpar(coluna)
            if clube and clube not in SEM_PODIO:
                contagem[(clube, pos)] += 1
    return contagem


def _ler_quadro(texto, titulo, escopo):
    """Lê um quadro de medalhas (clube x colocação) e valida a coluna Pódios."""
    quadro = Counter()
    for celulas in _tabela_apos(texto, titulo):
        if len(celulas) < 5 or celulas[0].lower() == 'clube':
            continue
        clube = _limpar(celulas[0])
        try:
            valores = [int(celulas[1 + p]) for p in range(3)]
            podios = int(celulas[4])
        except ValueError:
            falha('clubesCampeoes.md', None, f'{escopo}/{clube}: célula não numérica no quadro')
            continue
        for pos, v in enumerate(valores):
            quadro[(clube, pos)] = v
        if podios != sum(valores):
            falha('clubesCampeoes.md', None,
                  f'{escopo}/{clube}: coluna "Pódios" diz {podios}, '
                  f'mas a soma das colocações é {sum(valores)}')
    return quadro


def _comparar(esperado, declarado, escopo):
    for clube, pos in sorted(set(esperado) | set(declarado)):
        if esperado[(clube, pos)] != declarado[(clube, pos)]:
            falha('clubesCampeoes.md', None,
                  f'{escopo}/{clube}/{ROTULO[pos]}: quadro declara {declarado[(clube, pos)]}, '
                  f'tabelas por ano somam {esperado[(clube, pos)]}')


def checar_medalhas(rel, texto):
    if rel != 'clubesCampeoes.md':
        return

    apurado = {
        'CCO': _apurar_por_ano(
            texto, '### Campeonato Cearense de Orientação - CCO (Floresta)', 'CCO'),
        'CCOS': _apurar_por_ano(
            texto, '### Campeonato Cearense de Orientação Sprint - CCOS (Urbano)', 'CCOS'),
    }

    _comparar(apurado['CCO'], _ler_quadro(
        texto, '#### Campeonato Cearense de Orientação - CCO (Floresta)', 'CCO'), 'CCO')
    _comparar(apurado['CCOS'], _ler_quadro(
        texto, '#### Campeonato Cearense de Orientação Sprint - CCOS (Urbano)', 'CCOS'), 'CCOS')

    total = Counter()
    total.update(apurado['CCO'])
    total.update(apurado['CCOS'])
    _comparar(total, _ler_quadro(
        texto, '## Quadro Geral de Medalhas (Consolidado)', 'consolidado'), 'consolidado')


# --------------------------------------------------------------------------
def main():
    total = 0
    for rel, caminho in arquivos_md():
        total += 1
        texto = ler(caminho)
        checar_links(rel, texto)
        checar_artefatos(rel, texto)
        checar_tipografia(rel, texto)
        checar_frontmatter(rel, texto)
        checar_medalhas(rel, texto)

    print(f'Arquivos Markdown verificados: {total}')
    if problemas:
        print(f'\n{len(problemas)} problema(s) encontrado(s):\n')
        for p in problemas:
            print(f'  - {p}')
        return 1
    print('Nenhum problema encontrado.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
