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

from unidecode import unidecode

import escpos.barcode
import escpos.feature

from satcomum import br
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
    """
    Classe base para os extratos CF-e, fornecendo uma implementação padrão
    para o cabeçalho dos CF-e de venda e para os CF-e de cancelamento. Também
    fornece uma infraestrutura que simplifica a interface com impressoras
    ESC/POS, acrescentando fluidez à API de impressão.
    """

    def __init__(self, xmlstr, impressora):
        """

        :param xmlstr: String (unicode) contendo o XML do CF-e-SAT.
        :param impressora: Um objeto :class:`escpos.impl.epson.GenericESCPOS`
            ou especialização.
        """
        super(ExtratoCFe, self).__init__()
        self._xmlstr = xmlstr
        self.xml = util.XMLFacadeFromString(self._xmlstr)
        self.impressora = impressora

        self._flag_negrito = False
        self._flag_expandido = False
        self._flag_condensado= False


    @property
    def _colunas(self):
        if self._flag_condensado and not self._flag_expandido:
            return conf.colunas.condensado
        elif self._flag_expandido and not self._flag_condensado:
            return conf.colunas.expandido
        return conf.colunas.normal


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
        if self._flag_expandido:
            self.expandido()
        if self._flag_condensado:
            self.condensado()

    def negrito(self):
        self._flag_negrito = not self._flag_negrito
        self.impressora.set_emphasized(self._flag_negrito)
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

        nome_fantasia = self.xml.text('infCFe/emit/xFant', default='')
        razao_social = self.xml.text('infCFe/emit/xNome')

        logradouro = self.xml.text('infCFe/emit/enderEmit/xLgr')
        numero = self.xml.text('infCFe/emit/enderEmit/nro', default='')
        complemento = self.xml.text('infCFe/emit/enderEmit/xCpl', default='')
        bairro = self.xml.text('infCFe/emit/enderEmit/xBairro')

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
                self.xml.text('infCFe/emit/enderEmit/xMun'),
                br.uf_pelo_codigo(int(self.xml.text('infCFe/ide/cUF'))),
                br.as_cep(self.xml.text('infCFe/emit/enderEmit/CEP')))

        partes_endereco = [
                logradouro,
                complemento,
                bairro,
                cidade,]

        endereco = u'\r\n'.join([e for e in partes_endereco if e])

        im = 'IM: {}'.format(self.xml.text('infCFe/emit/IM', default=''))
        ie = 'IE: {}'.format(self.xml.text('infCFe/emit/IE'))
        cnpj = 'CNPJ: {}'.format(
                br.as_cnpj(self.xml.text('infCFe/emit/CNPJ')))

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
