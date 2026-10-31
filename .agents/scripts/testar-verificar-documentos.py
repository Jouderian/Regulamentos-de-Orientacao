#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Testes das checagens de verificar-documentos.py.

Cada checagem tem um caso construído para falhar e um caso que passa. O último
teste confirma que o acervo atual passa na verificação de estrutura.

    python .agents/scripts/testar-verificar-documentos.py
"""
import importlib.util
import os
import tempfile
import unittest

AQUI = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    'verificar', os.path.join(AQUI, 'verificar-documentos.py'))
verificar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(verificar)

REL = 'regulamentoCCO.md'
BASE = '# Regulamento do I Campeonato Cearense de Orientação\n\n'


def artigos(*numeros):
    ordinais = {n: f'{n}º' if n < 10 else str(n) for n in numeros}
    return ''.join(f'**Art. {ordinais[n]}** – Texto do artigo.\n\n' for n in numeros)


def problemas_de(texto):
    verificar.problemas.clear()
    verificar.checar_estrutura(REL, texto)
    return list(verificar.problemas)


class ChecagensDeEstrutura(unittest.TestCase):
    def assertFalha(self, texto, trecho):
        achados = problemas_de(texto)
        self.assertTrue(any(trecho in p for p in achados),
                        f'esperava "{trecho}" em {achados}')

    def test_documento_correto_passa(self):
        texto = (BASE + artigos(*range(1, 12))
                 + '> **Parágrafo Único:** Texto.\n\n>> **a.** Item.\n\n'
                 + 'Veja o Art. 10 deste regulamento e o Art. 2º deste regulamento.\n')
        self.assertEqual(problemas_de(texto), [])

    def test_documento_sem_artigos_passa(self):
        self.assertEqual(problemas_de(BASE + '## REGRAS\n\nTexto.\n'), [])

    def test_salto_na_sequencia(self):
        self.assertFalha(BASE + artigos(1, 2, 4), 'salto na sequência de artigos: Art. 2 seguido de Art. 4')

    def test_artigo_duplicado(self):
        self.assertFalha(BASE + artigos(1, 2, 2), 'artigo duplicado: Art. 2')

    def test_artigo_fora_de_ordem(self):
        self.assertFalha(BASE + artigos(1, 3, 2), 'salto na sequência')

    def test_referencia_a_artigo_inexistente(self):
        texto = BASE + artigos(1, 2) + 'Conforme o Art. 37 deste regulamento.\n'
        self.assertFalha(texto, 'referência a artigo inexistente')

    def test_referencia_a_artigo_existente_passa(self):
        texto = BASE + artigos(1, 2) + 'Conforme o Art. 2º deste regulamento.\n'
        self.assertEqual(problemas_de(texto), [])

    def test_ordinal_ausente_antes_do_decimo(self):
        self.assertFalha(BASE + '**Art. 1** – Texto.\n', 'deveria ser "Art. 1º"')

    def test_ordinal_indevido_a_partir_do_decimo(self):
        texto = BASE + artigos(*range(1, 10)) + '**Art. 10º** – Texto.\n'
        self.assertFalha(texto, 'deveria ser "Art. 10"')

    def test_ordinal_indevido_em_referencia(self):
        texto = BASE + artigos(*range(1, 11)) + 'Conforme o Art. 10º deste regulamento.\n'
        self.assertFalha(texto, 'ordinal da referência fora da convenção')

    def test_paragrafo_unico_em_minuscula(self):
        self.assertFalha(BASE + '> **Parágrafo único:** Texto.\n', 'parágrafo único fora do padrão')

    def test_paragrafo_unico_sem_citacao(self):
        self.assertFalha(BASE + '**Parágrafo Único:** Texto.\n', 'parágrafo único fora do padrão')

    def test_alinea_com_parenteses(self):
        self.assertFalha(BASE + '>> **a)** Texto.\n', 'alínea fora do padrão')

    def test_alinea_sem_ponto(self):
        self.assertFalha(BASE + '>> **b** Texto.\n', 'alínea fora do padrão')

    def test_titulo_em_caixa_alta(self):
        texto = '# REGULAMENTO DO CAMPEONATO CEARENSE DE ORIENTAÇÃO\n\n' + artigos(1)
        self.assertFalha(texto, 'título em caixa alta')

    def test_titulo_ausente(self):
        self.assertFalha('## REGRAS\n\n' + artigos(1), 'sem título de nível 1')

    def test_arquivo_que_nao_e_regulamento_e_ignorado(self):
        verificar.problemas.clear()
        verificar.checar_estrutura('README.md', '# TÍTULO\n\n**Art. 3** – Texto.\n')
        self.assertEqual(verificar.problemas, [])


class Edicoes(unittest.TestCase):
    def problemas(self, edicoes):
        verificar.problemas.clear()
        verificar.checar_edicoes(edicoes)
        return list(verificar.problemas)

    def test_vigente_e_em_elaboracao_posterior_passam(self):
        self.assertEqual(self.problemas({'vigente': {'2026'}, 'em-elaboracao': {'2027'}}), [])

    def test_sem_vigente(self):
        self.assertTrue(self.problemas({'em-elaboracao': {'2027'}}))

    def test_duas_vigentes(self):
        self.assertTrue(self.problemas({'vigente': {'2025', '2026'}}))

    def test_duas_em_elaboracao(self):
        self.assertTrue(self.problemas({'vigente': {'2026'}, 'em-elaboracao': {'2027', '2028'}}))

    def test_em_elaboracao_anterior_a_vigente(self):
        self.assertTrue(self.problemas({'vigente': {'2026'}, 'em-elaboracao': {'2025'}}))


class Congelamento(unittest.TestCase):
    """Documentos/2026 fechado (vigente) e Documentos/2027 em elaboração."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        for ano, status in (('2026', 'vigente'), ('2027', 'em-elaboracao')):
            self.gravar(f'{ano}/regulamento.md', f'---\nano: {ano}\nstatus: {status}\n---\n'.encode())
            self.gravar(f'{ano}/regulamento.pdf', f'pdf {ano}'.encode())
        self.gravar('2026/regras.pdf', b'rop 2026')

    def tearDown(self):
        self.tmp.cleanup()

    def gravar(self, rel, conteudo):
        caminho = os.path.join(self.raiz, 'Documentos', rel)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, 'wb') as fh:
            fh.write(conteudo)

    def manifesto(self, *rels):
        return ''.join(f'{verificar._sha256(os.path.join(self.raiz, "Documentos", r))}  {r}\n' for r in rels)

    def problemas(self, atual, base=None):
        verificar.problemas.clear()
        verificar.checar_congelados(self.raiz, atual, base)
        return list(verificar.problemas)

    def assertFalha(self, achados, trecho):
        self.assertTrue(any(trecho in p for p in achados), f'esperava "{trecho}" em {achados}')

    def test_manifesto_completo_passa(self):
        self.assertEqual(self.problemas(self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')), [])

    def test_rascunho_em_elaboracao_pode_mudar(self):
        atual = self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')
        self.gravar('2027/regulamento.pdf', b'pdf 2027 regenerado')
        self.assertEqual(self.problemas(atual), [])

    def test_arquivo_congelado_alterado(self):
        atual = self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')
        self.gravar('2026/regulamento.pdf', b'pdf 2026 regenerado')
        self.assertFalha(self.problemas(atual), 'foi alterado')

    def test_arquivo_congelado_removido(self):
        atual = self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')
        os.remove(os.path.join(self.raiz, 'Documentos', '2026', 'regras.pdf'))
        self.assertFalha(self.problemas(atual), 'removido')

    def test_arquivo_sem_registro(self):
        self.assertFalha(self.problemas(self.manifesto('2026/regras.pdf')), 'sem registro')

    def test_linha_removida_do_manifesto(self):
        base = self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')
        atual = self.manifesto('2026/regulamento.pdf')
        self.assertFalha(self.problemas(atual, base), 'alterada ou removida')

    def test_docx_de_edicao_fechada_nao_e_congelado(self):
        self.gravar('2026/regulamento.docx', b'docx intermediario')
        self.assertEqual(self.problemas(self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')), [])

    def test_linha_nova_no_manifesto_passa(self):
        base = self.manifesto('2026/regras.pdf')
        atual = self.manifesto('2026/regras.pdf', '2026/regulamento.pdf')
        self.assertEqual(self.problemas(atual, base), [])


class Acervo(unittest.TestCase):
    def test_acervo_passa_na_verificacao_inteira(self):
        verificar.problemas.clear()
        for rel, caminho in verificar.arquivos_md():
            verificar.checar_estrutura(rel, verificar.ler(caminho))
        self.assertEqual(verificar.problemas, [])


if __name__ == '__main__':
    unittest.main()
