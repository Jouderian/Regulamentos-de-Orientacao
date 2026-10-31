#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Verificações automáticas de integridade documental do repositório.

Executado pelo CI (.github/workflows/verificacao-documental.yml) e localmente:

    python .agents/scripts/verificar-documentos.py [--congelar]

--congelar registra no manifesto os PDF de edição fechada que ainda não estão
nele; nunca altera uma linha existente. Sai com código 1 se encontrar
qualquer problema.
"""
import hashlib
import os
import re
import subprocess
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


def sem_codigo(texto):
    """Substitui trechos de código por espaços, preservando posições e linhas.

    Evita acusar como defeito as menções que *documentam* o defeito, como
    `Paragrafo` citado entre crases nesta própria documentação.
    """
    def mascarar(m):
        return re.sub(r'[^\n]', ' ', m.group(0))

    texto = re.sub(r'(?ms)^```.*?^```', mascarar, texto)
    return re.sub(r'`[^`\n]+`', mascarar, texto)


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
    prosa = sem_codigo(texto)
    for m in re.finditer(r'Paragrafo', prosa):
        falha(rel, linha_de(prosa, m.start()), '"Paragrafo" sem acento')
    for m in re.finditer(r'(?:Parágrafo |Art\. )\d+o\b', prosa):
        falha(rel, linha_de(prosa, m.start()), f'ordinal sem indicador: {m.group(0)!r}')


# --------------------------------------------------------------------------
# 3. Tipografia jurídica dos regulamentos (ADR-003).
# --------------------------------------------------------------------------
def checar_tipografia(rel, texto):
    nome = os.path.basename(rel)
    if not nome.startswith(('regulamentoCCO', 'regulamentoDasCompeticoes')):
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
# 6. Bloco de metadados obrigatório nos regulamentos de competição.
# --------------------------------------------------------------------------
CAMPOS_REGULAMENTO = ('ano', 'edicao', 'status', 'rop_referencia')
STATUS = ('em-elaboracao', 'vigente', 'arquivado')


def checar_metadados_regulamento(rel, texto, edicoes):
    nome = os.path.basename(rel)
    if not (nome.startswith('regulamentoCCO') or nome.startswith('regulamentoDasCompeticoes')):
        return

    if not texto.startswith('---'):
        falha(rel, 1, 'regulamento sem cabeçalho frontmatter YAML')
        return

    cabecalho = texto.split('---', 2)[1] if texto.count('---') >= 2 else ''

    for campo in CAMPOS_REGULAMENTO:
        if not re.search(r'(?m)^' + campo + r':\s*\S', cabecalho):
            falha(rel, 1, f'frontmatter sem campo obrigatório "{campo}"')

    m_ano = re.search(r'(?m)^ano:\s*(\d{4})\b', cabecalho)
    if not m_ano:
        falha(rel, 1, 'campo "ano" deve ser um ano válido de 4 dígitos')
    else:
        ano_declarado = m_ano.group(1)
        partes = rel.replace('\\', '/').split('/')
        if partes[0] != 'Documentos' or len(partes) != 3:
            falha(rel, 1, 'regulamento fora de Documentos/<ano>/ (ADR-006)')
        elif ano_declarado != partes[1]:
            falha(rel, 1, f'campo "ano" ({ano_declarado}) diverge da pasta ({partes[1]})')

    m_status = re.search(r'(?m)^status:\s*(\S+)', cabecalho)
    if m_status:
        status = m_status.group(1).strip()
        if status not in STATUS:
            falha(rel, 1, f'status inválido "{status}" (esperado: "em-elaboracao", "vigente" ou "arquivado")')
        elif m_ano:
            edicoes.setdefault(status, set()).add(m_ano.group(1))


def checar_edicoes(edicoes):
    """Uma edição vigente e, no máximo, uma em elaboração, posterior à vigente."""
    vigentes = sorted(edicoes.get('vigente', ()))
    em_elaboracao = sorted(edicoes.get('em-elaboracao', ()))
    if len(vigentes) != 1:
        falha('Documentos', 0, f'deve haver exatamente 1 edição com regulamento "vigente", mas há {len(vigentes)}: {vigentes}')
    if len(em_elaboracao) > 1:
        falha('Documentos', 0, f'deve haver no máximo 1 edição "em-elaboracao", mas há {len(em_elaboracao)}: {em_elaboracao}')
    if len(vigentes) == 1 and em_elaboracao and em_elaboracao[0] <= vigentes[0]:
        falha('Documentos', 0, f'a edição em elaboração ({em_elaboracao[0]}) deve ser posterior à vigente ({vigentes[0]})')


# --------------------------------------------------------------------------
# 8. PDFs publicados congelados (ADR-006): todo PDF de Documentos/<ano>/,
#    exceto o gerado do regulamento em elaboração, tem o hash no manifesto,
#    que só recebe linhas novas. O .docx é intermediário e não é congelado.
# --------------------------------------------------------------------------
MANIFESTO = 'Documentos/arquivosCongelados.sha256'
PASTA_ANO = re.compile(r'^\d{4}(-\d{4})?$')
LINHA_MANIFESTO = re.compile(r'([0-9a-f]{64}) [ *](.+)')


def _sha256(caminho):
    h = hashlib.sha256()
    with open(caminho, 'rb') as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


def _status(caminho):
    with open(caminho, encoding='utf-8') as fh:
        inicio = fh.read(2048)
    m = re.match(r'---\n(.*?)\n---', inicio, re.S)
    s = re.search(r'(?m)^status:\s*(\S+)', m.group(1)) if m else None
    return s.group(1) if s else None


def arquivos_congelaveis(raiz):
    """PDFs de Documentos/<ano>/, como '<ano>/<arquivo>', exceto o do .md em elaboração."""
    documentos = os.path.join(raiz, 'Documentos')
    congelaveis = []
    for ano in sorted(os.listdir(documentos)):
        pasta = os.path.join(documentos, ano)
        if not (PASTA_ANO.match(ano) and os.path.isdir(pasta)):
            continue
        nomes = sorted(os.listdir(pasta))
        em_elaboracao = {n[:-3] for n in nomes
                         if n.endswith('.md') and _status(os.path.join(pasta, n)) == 'em-elaboracao'}
        for nome in nomes:
            base, ext = os.path.splitext(nome)
            if ext.lower() == '.pdf' and not nome.startswith('~$') and base not in em_elaboracao:
                congelaveis.append(f'{ano}/{nome}')
    return congelaveis


def ler_manifesto(texto):
    entradas = {}
    for n, linha in enumerate(texto.splitlines(), 1):
        if not linha.strip():
            continue
        m = LINHA_MANIFESTO.fullmatch(linha)
        if not m:
            falha(MANIFESTO, n, f'linha fora do formato "<sha256>  <ano>/<arquivo>": {linha[:60]!r}')
        elif m.group(2) in entradas:
            falha(MANIFESTO, n, f'arquivo registrado mais de uma vez: {m.group(2)}')
        else:
            entradas[m.group(2)] = m.group(1)
    return entradas


def manifesto_base():
    """Manifesto no commit de referência: VERIFICAR_BASE (CI) ou HEAD (local).

    Devolve None quando não há com o que comparar: push que cria o branch ou
    commit anterior à existência do manifesto.
    """
    base = os.environ.get('VERIFICAR_BASE', '').strip()
    explicita = bool(base)
    base = base or 'HEAD'
    if re.fullmatch(r'0+', base):
        return None

    def git(*args):
        try:
            return subprocess.run(['git', *args], cwd=RAIZ, capture_output=True)
        except OSError:
            return None

    existe = git('cat-file', '-e', f'{base}^{{commit}}')
    if existe is None or existe.returncode != 0:
        if explicita:
            falha(MANIFESTO, 0, f'commit de referência {base[:12]} indisponível: o CI precisa do histórico completo')
        return None
    res = git('show', f'{base}:{MANIFESTO}')
    return res.stdout.decode('utf-8') if res.returncode == 0 else None


def checar_congelados(raiz, texto_atual, texto_base=None):
    registrados = ler_manifesto(texto_atual)
    for rel, esperado in registrados.items():
        caminho = os.path.join(raiz, 'Documentos', rel)
        if not os.path.isfile(caminho):
            falha(MANIFESTO, 0, f'arquivo congelado removido: Documentos/{rel}')
        elif _sha256(caminho) != esperado:
            falha(f'Documentos/{rel}', 0, 'arquivo congelado foi alterado: o hash não confere com o manifesto')
    for rel in arquivos_congelaveis(raiz):
        if rel not in registrados:
            falha(f'Documentos/{rel}', 0, 'PDF de edição fechada sem registro no manifesto; '
                                         'registre com "python .agents/scripts/verificar-documentos.py --congelar"')
    if texto_base is not None:
        atuais = set(texto_atual.splitlines())
        for linha in texto_base.splitlines():
            if linha.strip() and linha not in atuais:
                falha(MANIFESTO, 0, f'linha do manifesto alterada ou removida: {linha[:80]!r}')


def congelar(raiz):
    caminho = os.path.join(raiz, MANIFESTO)
    texto = ler(caminho) if os.path.exists(caminho) else ''
    registrados = ler_manifesto(texto)
    novos = [f'{_sha256(os.path.join(raiz, "Documentos", rel))}  {rel}\n'
             for rel in arquivos_congelaveis(raiz) if rel not in registrados]
    if novos:
        if texto and not texto.endswith('\n'):
            texto += '\n'
        with open(caminho, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write(texto + ''.join(novos))
    print(f'Arquivos congelados agora: {len(novos)}')
    for linha in novos:
        print(f'  + Documentos/{linha.split("  ", 1)[1].strip()}')


# --------------------------------------------------------------------------
# 7. Estrutura dos regulamentos: artigos, ordinal, parágrafo único, alínea, título.
# --------------------------------------------------------------------------
ARTIGO = re.compile(r'(?m)^\*\*Art\.? ?(\d+)([^*]{0,3}?)\*\*')
REFERENCIA = re.compile(r'(?i)\bArt(?:igo|\.)? ?(\d+)(º|°|o)?\s+deste\s+regulamento')
PARAGRAFO_UNICO = re.compile(r'(?mi)^[> ]*\**\s*Parágrafo\s+[uú]nico.*$')
ALINEA = re.compile(r'(?m)^>+ ?\*\*(\(?[a-z][).]?)\*\*')


def _ordinal_correto(numero, sufixo):
    """Art. 1º a 9º levam ordinal; do 10 em diante, cardinal (ADR-003, revisão de 2026-10-17)."""
    return sufixo == ('º' if numero < 10 else '')


def checar_estrutura(rel, texto):
    nome = os.path.basename(rel)
    if not nome.startswith(('regulamentoCCO', 'regulamentoDasCompeticoes')):
        return
    prosa = sem_codigo(texto)

    anterior = None
    existentes = set()
    for m in ARTIGO.finditer(prosa):
        numero, sufixo = int(m.group(1)), m.group(2)
        linha = linha_de(prosa, m.start())
        if not _ordinal_correto(numero, sufixo):
            esperado = f'{numero}º' if numero < 10 else str(numero)
            falha(rel, linha, f'ordinal do artigo fora da convenção: '
                              f'"Art. {numero}{sufixo}" deveria ser "Art. {esperado}"')
        if numero in existentes:
            falha(rel, linha, f'artigo duplicado: Art. {numero}')
        elif anterior is not None and numero != anterior + 1:
            falha(rel, linha, f'salto na sequência de artigos: Art. {anterior} seguido de Art. {numero}')
        existentes.add(numero)
        anterior = numero

    for m in REFERENCIA.finditer(prosa):
        numero, sufixo = int(m.group(1)), m.group(2) or ''
        linha = linha_de(prosa, m.start())
        if numero not in existentes:
            falha(rel, linha, f'referência a artigo inexistente neste documento: {m.group(0)!r}')
        if not _ordinal_correto(numero, sufixo):
            falha(rel, linha, f'ordinal da referência fora da convenção: {m.group(0)!r}')

    for m in PARAGRAFO_UNICO.finditer(prosa):
        if not m.group(0).startswith('> **Parágrafo Único:**'):
            falha(rel, linha_de(prosa, m.start()),
                  f'parágrafo único fora do padrão "> **Parágrafo Único:**": {m.group(0)[:40]!r}')

    for m in ALINEA.finditer(prosa):
        if not re.fullmatch(r'[a-z]\.', m.group(1)):
            falha(rel, linha_de(prosa, m.start()),
                  f'alínea fora do padrão "**a.**": {m.group(0)!r}')

    titulo = re.search(r'(?m)^# (.+)$', prosa)
    if not titulo:
        falha(rel, 1, 'regulamento sem título de nível 1 ("# ...")')
    elif not re.search(r'[a-zà-ÿ]', titulo.group(1)):
        falha(rel, linha_de(prosa, titulo.start()),
              f'título em caixa alta: {titulo.group(1)[:50]!r}')


# --------------------------------------------------------------------------
def main():
    if '--congelar' in sys.argv[1:]:
        congelar(RAIZ)

    total = 0
    edicoes = {}
    for rel, caminho in arquivos_md():
        total += 1
        texto = ler(caminho)
        checar_links(rel, texto)
        checar_artefatos(rel, texto)
        checar_tipografia(rel, texto)
        checar_estrutura(rel, texto)
        checar_frontmatter(rel, texto)
        checar_medalhas(rel, texto)
        checar_metadados_regulamento(rel, texto, edicoes)
    checar_edicoes(edicoes)

    manifesto = os.path.join(RAIZ, MANIFESTO)
    checar_congelados(RAIZ, ler(manifesto) if os.path.exists(manifesto) else '', manifesto_base())

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

