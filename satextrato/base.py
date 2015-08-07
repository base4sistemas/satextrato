# -*- coding: utf-8 -*-
#
# satextrato/base.py
#
# Copyright 2015 Base4 Sistemas Ltda ME
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import textwrap
import warnings
import xml.etree.ElementTree as ET

from unidecode import unidecode

import escpos.barcode
import escpos.feature

from satcomum import br
from satcomum import constantes
from satcomum import util

from .config import conf


def _bordas(esquerda, direita, largura=48, espacamento_minimo=4):
        espacamento = largura - (len(esquerda) + len(direita))
        if espacamento < espacamento_minimo:
            espacamento = espacamento_minimo
            comprimento_maximo = int(largura / 2) - espacamento_minimo
            esquerda = esquerda[:comprimento_maximo]
            direita = direita[:comprimento_maximo]
        return '%s%s%s' % (esquerda, ' ' * espacamento, direita)


class ExtratoCFe(object):
    """Classe base para os extratos do CF-e de venda e cancelamento, fornecendo
    uma implementação comum para o cabeçalho dos CF-e de venda e cancelamento,
    além da infraestrutura que simplifica a interface para impressoras ESC/POS.

    As implementações que realmente emitem os extratos estão nas classes
    :class:`~satextrato.venda.ExtratoCFeVenda` e
    :class:`~satextrato.cancelamento.ExtratoCFeCancelamento`.
    """

    def __init__(self, fp, impressora):
        """Inicia uma instância de :class:`ExtratoCFe`.

        :param fp: Um objeto *file-like* para o documento XML que contém o CF-e.
        :param impressora: Um objeto :class:`escpos.impl.epson.GenericESCPOS`
            ou especialização.

        """
        super(ExtratoCFe, self).__init__()
        self._tree = ET.parse(fp)
        self.root = self._tree.getroot() # referência para o elemento `CFe`
        self.impressora = impressora

        self._flag_negrito = False
        self._flag_italico = False
        self._flag_expandido = False
        self._flag_condensado= False


    @property
    def _colunas(self):
        if self._flag_condensado and not self._flag_expandido:
            return conf.colunas.condensado
        elif self._flag_expandido and not self._flag_condensado:
            return conf.colunas.expandido
        return conf.colunas.normal


    @property
    def is_ambiente_testes(self):
        """Indica se o CF-e-SAT foi emitido em "ambiente de testes".

        Embora o Manual de Orientação para emissão dos extratos do CF-e-SAT não
        seja claro quanto ao que significa "estar em condição de teste", esta
        implementação irá assumir "condição de testes" quando:

        * elemento B10 ``tpAmb`` for ``2`` (ambiente de testes) **OU**
        * elemento B12 ``signAC`` possuir a assinatura de teste, indicada pela
          constante :attr:`satcomum.constantes.ASSINATURA_AC_TESTE`.

        .. note::

            O CF-e de cancelamento não possui o elemento ``tpAmb``, conforme
            descrito na ER SAT, item 4.2.3 **Layout do CF-e de cancelamento**.

        :raises ValueError: Se o documento XML não identificar um CF-e-SAT de
            venda ou cancelamento.

        """
        signAC = self.root.findtext('./infCFe/ide/signAC')

        if self.root.tag == constantes.ROOT_TAG_VENDA:
            tpAmb = self.root.findtext('./infCFe/ide/tpAmb')
            return tpAmb == constantes.B10_TESTES or \
                    signAC == constantes.ASSINATURA_AC_TESTE

        elif self.root.tag == constantes.ROOT_TAG_CANCELAMENTO:
            # CF-e-SAT de cancelamento não possui `tpAmb`
            return signAC == constantes.ASSINATURA_AC_TESTE

        raise ValueError('Documento nao parece ser um CF-e-SAT, '
                'root tag {!r}'.format(self.root.tag))


    def imprimir(self):
        self.cabecalho()
        self.corpo()
        self.rodape()
        self.fim_documento()


    def centro(self):
        self.impressora.justify_center()
        return self


    def esquerda(self):
        self.impressora.justify_left()
        return self


    def normal(self):
        if self._flag_negrito:
            self.negrito()
        if self._flag_italico:
            self.italico()
        if self._flag_expandido:
            self.expandido()
        if self._flag_condensado:
            self.condensado()


    def negrito(self):
        self._flag_negrito = not self._flag_negrito
        self.impressora.set_emphasized(self._flag_negrito)
        return self


    def italico(self):
        warnings.warn('Estilo "italico" ainda nao disponivel via PyESCPOS',
                stacklevel=2)
        self._flag_italico = not self._flag_italico
        return self


    def expandido(self):
        self._flag_expandido = not self._flag_expandido
        self.impressora.set_expanded(self._flag_expandido)
        return self


    def condensado(self):
        self._flag_condensado = not self._flag_condensado
        self.impressora.set_condensed(self._flag_condensado)
        return self


    def bordas(self, texto_esquerda, texto_direita,
            colunas=None,
            espacamento_minimo=4):
        largura = colunas or self._colunas
        texto = _bordas(texto_esquerda, texto_direita,
                largura=largura,
                espacamento_minimo=espacamento_minimo)
        self.texto(texto)
        return self


    def quebrar(self, texto, colunas=None):
        largura = colunas or self._colunas
        # considera hard-breaks
        linhas_fixas = texto.replace('\r', '').split('\n')
        for linha_fixa in linhas_fixas:
            linhas = textwrap.wrap(linha_fixa, largura)
            for linha in linhas:
                self.texto(linha)
        return self


    def avanco(self, linhas=1):
        self.impressora.lf(lines=linhas)
        return self


    def texto(self, texto):
        self.impressora.text(unidecode(util.forcar_unicode(texto)))
        return self


    def separador(self, caracter='-', colunas=None):
        largura = colunas or self._colunas
        self.texto('-' * largura)
        return self


    def indicacao_de_teste(self):
        """Imprime indicação de teste se o CF-e estiver em "condição de teste".
        Caso contrário, não faz nada. A indicação de teste, conforme o Manual de
        Orientação deverá ser impressa em itálico (note a linha em branco acima
        e abaixo da inscrição "TESTE"):

        .. sourcecode:: text

                    10        20        30        40      48 :
            ....:....|....:....|....:....|....:....|....:..! :
                                                             :
                             = T E S T E =                   :
                                                             :
            <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< :
            <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< :
            <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< :

        .. note::

            O correto são linhas com sinais de ``>``, mas isso faz com que o
            framework de teste interprete como um bloco de teste (doctest). Os
            sinais de ``<`` dão uma boa ideia do resultado final.

        """
        if self.is_ambiente_testes:
            self.italico()
            self.avanco()
            self.texto('= T E S T E =')
            self.avanco()
            for i in xrange(3):
                self.texto('>' * conf.colunas.normal)
            self.italico()


    def numero_extrato(self):
        """
        Obtém o número do extrato, elemento ``nCFe`` (B06). Se o CF-e estiver
        em condição de teste retornará ``000000``.

        Veja :meth:`is_ambiente_testes` para outros detalhes.
        """
        if self.is_ambiente_testes:
            return '0' * 6
        return self.root.findtext('./infCFe/ide/nCFe')


    def chave_cfe_code128(self, chave):
        """
        Imprime o código de barras Code128 da chave do CF-e informada.
        """
        code128_params = dict(
                barcode_height=conf.code128_altura,
                barcode_width=escpos.barcode.BARCODE_NORMAL_WIDTH,
                barcode_hri=escpos.barcode.BARCODE_HRI_NONE)

        if conf.code128_quebrar:
            # imprime o Code128 da chave do CF-e em duas partes de 22 digitos
            chave_quebrada = util.partes_chave_cfe(chave, partes=2)
            self.impressora.code128(chave_quebrada[0], **code128_params)
            self.avanco()
            self.impressora.code128(chave_quebrada[1], **code128_params)
        else:
            self.impressora.code128(chave, **code128_params)


    def fim_documento(self):
        """
        Encerra o documento, imprimindo o rodapé (se houver) e avançando ou
        guilhotinando o documento, conforme as configurações.
        """
        self.normal()
        self.avanco()
        self.separador()

        if conf.nota_rodape.esquerda or conf.nota_rodape.direita:
            self.condensado()
            self.bordas(conf.nota_rodape.esquerda, conf.nota_rodape.direita)
            self.condensado()

        if conf.cortar_documento and \
                self.impressora.hardware_features.get(
                        escpos.feature.CUTTER, False):
            self.impressora.cut(partial=conf.cortar_parcialmente)

        elif conf.avancar_linhas > 0:
            self.avanco(conf.avancar_linhas)


    def cabecalho(self):

        self.normal()

        emit = self.root.find('./infCFe/emit')
        enderEmit = emit.find('enderEmit')

        nome_fantasia = emit.findtext('xFant')
        razao_social = emit.findtext('xNome')

        logradouro = enderEmit.findtext('xLgr')
        numero = enderEmit.findtext('nro')
        complemento = enderEmit.findtext('xCpl')
        bairro = enderEmit.findtext('xBairro')

        if numero: # número não é obrigatório
            logradouro = u'{}, {}'.format(logradouro, numero)

        if complemento: # complemento não é obrigatório
            # faz um esforço para manter o complemento na mesma linha que o
            # logradouro/número se couber, senão o complemento irá usar uma
            # linha exclusiva...
            if len(logradouro) + len(complemento) < self._colunas:
                # ok, mantém o complemento na mesma linha que o logradouro
                logradouro = u'{}, {}'.format(logradouro, complemento)
                complemento = '' # ignora a linha que deveria conter o xCpl

        cidade = u'{}/{} CEP: {}'.format(
                enderEmit.findtext('xMun'),
                br.uf_pelo_codigo(int(self.root.findtext('./infCFe/ide/cUF'))),
                br.as_cep(enderEmit.findtext('CEP')))

        partes_endereco = [logradouro, complemento, bairro, cidade,]
        endereco = u'\r\n'.join([e for e in partes_endereco if e])

        cnpj = 'CNPJ: {}'.format(br.as_cnpj(emit.findtext('CNPJ')))
        im = 'IM: {}'.format(emit.findtext('IM') or '')
        ie = 'IE: {}'.format(emit.findtext('IE'))

        self.centro()
        self.negrito()

        if nome_fantasia:
            self.quebrar(nome_fantasia)

        self.quebrar(razao_social)
        self.negrito()

        self.quebrar(endereco)

        self.avanco()
        self.esquerda()
        self.texto(cnpj)
        self.texto(ie)

        if im:
            self.texto(im)

        self.separador()


    def rodape(self):
        raise NotImplementedError()


    def corpo(self):
        raise NotImplementedError()
