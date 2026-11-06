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


class RopEmElaboracao(unittest.TestCase):
    def problemas(self, *arquivos):
        verificar.problemas.clear()
        rops = []
        for rel, status in arquivos:
            verificar.checar_status_rop(rel, f'---\nano: 2027\nstatus: {status}\n---\n', rops)
        verificar.checar_rops(rops)
        return list(verificar.problemas)

    def test_uma_rop_em_elaboracao_passa(self):
        self.assertEqual(self.problemas(('Documentos/2027/regrasOrientacaoPedestre.md', 'em-elaboracao')), [])

    def test_duas_rops_em_elaboracao(self):
        self.assertTrue(self.problemas(('Documentos/2027/regrasOrientacaoPedestre.md', 'em-elaboracao'),
                                       ('Documentos/2028/regrasOrientacaoPedestre.md', 'em-elaboracao')))

    def test_status_invalido(self):
        self.assertTrue(self.problemas(('Documentos/2027/regrasOrientacaoPedestre.md', 'rascunho')))

    def test_rop_nao_conta_como_edicao_do_regulamento(self):
        verificar.problemas.clear()
        edicoes = {}
        verificar.checar_metadados_regulamento('Documentos/2027/regrasOrientacaoPedestre.md',
                                               '---\nano: 2027\nstatus: em-elaboracao\n---\n', edicoes)
        self.assertEqual(edicoes, {})


class Congelamento(unittest.TestCase):
    """CCOS 2025 arquivado, regulamento e ROP de 2026 publicados; regulamento e minuta da ROP de 2027 em elaboração."""

    REG = 'regulamentoDasCompeticoesCearenses'
    ROP = 'regrasOrientacaoPedestre'

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        self.gravar('2025/regulamentoCCOS.md', b'---\nano: 2025\nstatus: arquivado\n---\n')
        self.gravar('2025/regulamentoCCOS.pdf', b'ccos 2025')
        for ano, status in (('2026', 'vigente'), ('2027', 'em-elaboracao')):
            self.gravar(f'{ano}/{self.REG}.md', f'---\nano: {ano}\nstatus: {status}\n---\n'.encode())
            self.gravar(f'{ano}/{self.REG}.pdf', f'pdf {ano}'.encode())
        self.gravar(f'2026/{self.ROP}.md', b'---\ndescription: ROP 2026\n---\n')
        self.gravar(f'2026/{self.ROP}.pdf', b'rop 2026')
        self.gravar(f'2027/{self.ROP}.md', b'---\nano: 2027\nstatus: em-elaboracao\n---\n')
        self.gravar(f'2027/{self.ROP}.pdf', b'minuta rop 2027')
        self.gravar('2026/resultadoClubesCCO.pdf', b'resultado 2026')
        self.fechado = f'2026/{self.REG}.pdf'
        self.congelados = ['2025/regulamentoCCOS.pdf', f'2026/{self.ROP}.pdf', self.fechado]

    def tearDown(self):
        self.tmp.cleanup()

    def gravar(self, rel, conteudo):
        caminho = os.path.join(self.raiz, 'Documentos', rel)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, 'wb') as fh:
            fh.write(conteudo)

    def manifesto(self, *rels):
        return ''.join(f'{verificar._sha256(os.path.join(self.raiz, "Documentos", r))}  {r}\n' for r in rels)

    def completo(self):
        return self.manifesto(*self.congelados)

    def problemas(self, atual, base=None):
        verificar.problemas.clear()
        verificar.checar_congelados(self.raiz, atual, base)
        return list(verificar.problemas)

    def assertFalha(self, achados, trecho):
        self.assertTrue(any(trecho in p for p in achados), f'esperava "{trecho}" em {achados}')

    def test_congelaveis_sao_regulamentos_fechados_e_rop_publicada(self):
        self.assertEqual(verificar.arquivos_congelaveis(self.raiz), self.congelados)

    def test_manifesto_completo_passa(self):
        self.assertEqual(self.problemas(self.completo()), [])

    def test_rascunhos_em_elaboracao_podem_mudar(self):
        self.gravar(f'2027/{self.REG}.pdf', b'pdf 2027 regenerado')
        self.gravar(f'2027/{self.ROP}.pdf', b'nova minuta 2027')
        self.assertEqual(self.problemas(self.completo()), [])

    def test_resultado_pode_mudar(self):
        self.gravar('2026/resultadoClubesCCO.pdf', b'resultado corrigido')
        self.assertEqual(self.problemas(self.completo()), [])

    def test_rop_publicada_alterada(self):
        atual = self.completo()
        self.gravar(f'2026/{self.ROP}.pdf', b'rop 2026 substituida')
        self.assertFalha(self.problemas(atual), 'foi alterado')

    def test_ccos_alterado(self):
        atual = self.completo()
        self.gravar('2025/regulamentoCCOS.pdf', b'ccos 2025 regenerado')
        self.assertFalha(self.problemas(atual), 'foi alterado')

    def test_arquivo_congelado_removido(self):
        atual = self.completo()
        os.remove(os.path.join(self.raiz, 'Documentos', self.fechado))
        self.assertFalha(self.problemas(atual), 'removido')

    def test_arquivo_sem_registro(self):
        self.assertFalha(self.problemas(self.manifesto(self.fechado)), 'sem registro')

    def test_pdf_nao_congelavel_no_manifesto(self):
        atual = self.manifesto(*self.congelados, '2026/resultadoClubesCCO.pdf')
        self.assertFalha(self.problemas(atual), 'não se congela')

    def test_minuta_no_manifesto(self):
        atual = self.manifesto(*self.congelados, f'2027/{self.ROP}.pdf')
        self.assertFalha(self.problemas(atual), 'não se congela')

    def test_linha_removida_do_manifesto(self):
        atual = self.manifesto(*self.congelados[:-1])
        self.assertFalha(self.problemas(atual, self.completo()), 'alterada ou removida')

    def test_remover_linha_de_pdf_nao_congelavel_passa(self):
        base = self.manifesto(*self.congelados, '2026/resultadoClubesCCO.pdf')
        self.assertEqual(self.problemas(self.completo(), base), [])

    def test_docx_de_edicao_fechada_nao_e_congelado(self):
        self.gravar(f'2026/{self.REG}.docx', b'docx intermediario')
        self.assertEqual(self.problemas(self.completo()), [])

    def test_linha_nova_no_manifesto_passa(self):
        self.assertEqual(self.problemas(self.completo(), self.manifesto(self.fechado)), [])


class IndiceSpecs(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.raiz = self.tmp.name
        self.spec('alfa', 'ativa')

    def tearDown(self):
        self.tmp.cleanup()

    def spec(self, nome, status):
        pasta = os.path.join(self.raiz, '.agents', 'specs', nome)
        os.makedirs(pasta, exist_ok=True)
        with open(os.path.join(pasta, 'spec.md'), 'w', encoding='utf-8') as fh:
            fh.write(f'---\ndescription: x\nstatus: {status}\n---\n')

    def indice(self, *linhas):
        with open(os.path.join(self.raiz, '.agents', 'specs', 'index.md'), 'w', encoding='utf-8') as fh:
            fh.write('\n'.join(linhas) + '\n')

    def problemas(self):
        verificar.problemas.clear()
        verificar.checar_indice_specs(self.raiz)
        return list(verificar.problemas)

    def test_indice_coerente_passa(self):
        self.indice('| [alfa](alfa/spec.md) | ativa | Resumo |')
        self.assertEqual(self.problemas(), [])

    def test_indice_ausente(self):
        self.assertTrue(self.problemas())

    def test_spec_fora_do_indice(self):
        self.spec('beta', 'ativa')
        self.indice('| [alfa](alfa/spec.md) | ativa | Resumo |')
        self.assertTrue(self.problemas())

    def test_situacao_divergente(self):
        self.indice('| [alfa](alfa/spec.md) | concluída | Resumo |')
        self.assertTrue(self.problemas())

    def test_spec_sem_status(self):
        self.spec('alfa', 'pendente')
        self.indice('| [alfa](alfa/spec.md) | pendente | Resumo |')
        self.assertTrue(self.problemas())


class Acervo(unittest.TestCase):
    def test_acervo_passa_na_verificacao_inteira(self):
        verificar.problemas.clear()
        for rel, caminho in verificar.arquivos_md():
            verificar.checar_estrutura(rel, verificar.ler(caminho))
        self.assertEqual(verificar.problemas, [])


if __name__ == '__main__':
    unittest.main()
