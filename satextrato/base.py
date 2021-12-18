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
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import textwrap
import xml.etree.ElementTree as ET

from six.moves import range

from unidecode import unidecode

import escpos.barcode
import escpos.feature

from satcomum import br
from satcomum import constantes

from .config import padrao as config_padrao


class ExtratoCFe(object):
    """Classe base para os extratos do CF-e de venda e cancelamento, fornecendo
    uma implementação comum para o cabeçalho dos CF-e de venda e cancelamento,
    além da infraestrutura que simplifica a interface para impressoras ESC/POS.

    As implementações que realmente emitem os extratos estão nas classes
    :class:`~satextrato.venda.ExtratoCFeVenda` e
    :class:`~satextrato.cancelamento.ExtratoCFeCancelamento`.
    """

    def __init__(self, fp, impressora, config=None):
        """Inicia uma instância de :class:`ExtratoCFe`.

        :param fp: Um *file object* para o documento XML que contém o CF-e.

        :param impressora: Um instância (ou subclasse, especialização) de
            :class:`escpos.impl.epson.GenericESCPOS` usado para efetivamente
            imprimir o extrato.

        :param config: Opcional.
            Uma instância de :class:`satextrato.config.Configuracoes`.
            Se não informado, serão usados valores padrão.

        """
        super(ExtratoCFe, self).__init__()
        self._config = config or config_padrao()
        self._tree = ET.parse(fp)
        self.root = self._tree.getroot()
        self.impressora = impressora

        self._flag_negrito = False
        self._flag_italico = False
        self._flag_expandido = False
        self._flag_condensado = False

    @property
    def _colunas(self):
        if self._flag_condensado:
            num_colunas = self.impressora.feature.columns.condensed
        elif self._flag_expandido:
            num_colunas = self.impressora.feature.columns.expanded
        else:
            num_colunas = self.impressora.feature.columns.normal
        return num_colunas

    @property
    def is_ambiente_testes(self):
        """Indica se o CF-e-SAT foi emitido em "ambiente de testes".
        Considera como emitido em ambiente de testes quando:

        * Elemento B10 ``tpAmb`` for ``2`` (ambiente de testes) ou
        * Elemento B12 ``signAC`` possuir a assinatura de teste, indicada pela
          constante :attr:`satcomum.constantes.ASSINATURA_AC_TESTE`.

        .. note::

            O CF-e de cancelamento não possui o elemento ``tpAmb``, conforme
            descrito na ER SAT, item 4.2.3 **Layout do CF-e de cancelamento**.

        :raises ValueError: Se o documento XML não for identificado como um
            CF-e-SAT de venda ou cancelamento.

        """
        signAC = self.root.findtext('./infCFe/ide/signAC')

        if self.root.tag == constantes.ROOT_TAG_VENDA:
            tpAmb = self.root.findtext('./infCFe/ide/tpAmb')
            return (tpAmb == constantes.B10_TESTES
                    or signAC == constantes.ASSINATURA_AC_TESTE)

        elif self.root.tag == constantes.ROOT_TAG_CANCELAMENTO:
            # CF-e-SAT de cancelamento não possui `tpAmb`
            return signAC == constantes.ASSINATURA_AC_TESTE

        raise ValueError(
                (
                    'Documento nao parece ser um CF-e-SAT; root tag: {!r}'
                ).format(self.root.tag)
            )

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

    def bordas(
            self,
            texto_esquerda,
            texto_direita,
            colunas=None,
            espacamento_minimo=4
            ):
        largura = colunas or self._colunas
        texto = _bordas(
                texto_esquerda,
                texto_direita,
                largura=largura,
                espacamento_minimo=espacamento_minimo
            )
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
        self.impressora.text(unidecode(texto))
        return self

    def separador(self, caracter='-', colunas=None):
        largura = colunas or self._colunas
        self.texto('-' * largura)
        return self

    def indicacao_de_teste(self):
        """Imprime indicação de teste se o CF-e estiver em "condição de
        teste". Caso contrário, não faz nada. A indicação de teste,
        conforme o Manual de Orientação deverá ser impressa em itálico
        (note a linha em branco acima e abaixo da inscrição "TESTE"):

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
            for i in range(3):
                self.texto('>' * self._colunas)
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
        """Imprime o código de barras padrão Code128 para a chave do CF-e.

        :param chave: Instância de :class:`satcomum.ersat.ChaveCFeSAT`.
        """
        self.centro()
        self.condensado()
        self.texto(' '.join(chave.partes()))
        self.condensado()

        if self._config.code128.ignorar:
            return

        code128_params = dict(
                barcode_height=self._config.code128.altura,
                barcode_width=escpos.barcode.BARCODE_NORMAL_WIDTH,
                barcode_hri=escpos.barcode.BARCODE_HRI_NONE
            )

        if self._config.code128.truncar:
            tamanho = self._config.code128.truncar_tamanho
            digitos = ''.join(chave.partes())[:tamanho]
            self.centro()
            self.impressora.code128(digitos, **code128_params)

        elif self._config.code128.quebrar:
            partes = _quebrar_chave(chave, self._config.code128.quebrar_partes)
            for n_parte, parte in enumerate(partes, 1):
                self.centro()
                self.impressora.code128(parte, **code128_params)
                if self._config.code128.pular_linha_entre_partes:
                    if n_parte < len(partes):
                        self.avanco()
        else:
            partes = chave.partes(1)
            self.centro()
            self.impressora.code128(partes[0], **code128_params)

    def qrcode_mensagem(self):
        mensagem = self._config.qrcode.mensagem.strip()
        if not mensagem:
            return

        if self._config.qrcode.mensagem_modo_condensado:
            self.condensado()
        self.centro()
        for linha in textwrap.wrap(mensagem, self._colunas):
            self.texto(linha)
        self.esquerda()
        if self._config.qrcode.mensagem_modo_condensado:
            self.condensado()

    def fim_documento(self):
        """Encerra o documento, imprimindo o rodapé (se houver) e avançando ou
        guilhotinando o documento, conforme as configurações.
        """
        self.normal()
        self.avanco()
        self.separador()

        conf_cupom = self._config.cupom
        conf_rodape = self._config.rodape

        if conf_rodape.esquerda or conf_rodape.direita:
            self.condensado()
            self.bordas(conf_rodape.esquerda, conf_rodape.direita)
            self.condensado()

        if self.impressora.feature.cutter and conf_cupom.cortar_documento:
            if conf_cupom.avancar_linhas > 0:
                self.avanco(conf_cupom.avancar_linhas)
            self.impressora.cut(
                    partial=conf_cupom.cortar_parcialmente,
                    feed=conf_cupom.cortar_avanco
                )
        else:
            # impressora não possui guilhotina ou não é para cortar o documento
            if conf_cupom.avancar_linhas > 0:
                self.avanco(conf_cupom.avancar_linhas)

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

        if numero:  # número não é obrigatório
            logradouro = u'{}, {}'.format(logradouro, numero)

        if complemento:  # complemento não é obrigatório
            # faz um esforço para manter o complemento na mesma linha que o
            # logradouro/número se couber, senão o complemento irá usar uma
            # linha exclusiva...
            if len(logradouro) + len(complemento) < self._colunas:
                # ok, mantém o complemento na mesma linha que o logradouro
                logradouro = u'{}, {}'.format(logradouro, complemento)
                complemento = ''  # ignora a linha que deveria conter o xCpl

        cidade = u'{}/{} CEP: {}'.format(
                enderEmit.findtext('xMun'),
                br.uf_pelo_codigo(int(self.root.findtext('./infCFe/ide/cUF'))),
                br.as_cep(enderEmit.findtext('CEP')))

        partes_endereco = [logradouro, complemento, bairro, cidade]
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


def _bordas(
        esquerda,
        direita,
        largura=48,
        espacamento_minimo=4,
        favorecer_direita=True
        ):
    """Prepara duas strings para serem impressas alinhadas às bordas opostas da
    mídia, os textos da esquerda (borda esquerda) e da direita (borda direita),
    respeitando uma largura e espaçamento mínimo determinados.

    .. sourcecode:: python

        >>> _bordas('a', 'b')
        'a                                              b'

        >>> esquerda = 'a' * 30
        >>> direita = 'b' * 30
        >>> _bordas(esquerda, direita)
        'aaaaaaaaaaaaaaaaaaaaaa    bbbbbbbbbbbbbbbbbbbbbb'

        >>> esquerda = 'Gazeta publica hoje breve nota de faxina na quermesse'
        >>> direita = 'Um pequeno jabuti xereta viu dez cegonhas felizes'
        >>> _bordas(esquerda, direita, espacamento_minimo=1)
        'Gazeta publica hoje bre viu dez cegonhas felizes'


    :param str esquerda: O texto a ser exibido à esquerda. Se o texto não
        couber (em relação à largura e ao espaçamento mínimo) será exibida
        apenas a porção mais à esquerda desse texto, sendo cortados (não
        impressos) os caracteres do final do texto.

    :param str direita: O texto à ser exibido à direita. Se o texto da direita
        não couber (em relação à largura e ao espaçamento mínimo) será exibida
        apenas porção mais à direita desse texto, sendo cortados (não
        impressos) os caracteres do início do texto.

    :param int largura: Largura em caracteres a considerar ao calcular o vão
        entre os textos da esquerda e direita. O padrão é 48, já que é a
        largura mais comum entre as impressoras térmicas de bobina quando
        imprimindo com a fonte normal.

    :param int espacamento_minimo: Opcional. Determina o número de espaços
        mínimo a ser deixado entre os textos da esquerda e direita. O padrão
        são quatro espaços.

    :param bool favorecer_direita: Opcional. Determina se o texto da direita
        deverá ser favorecido com um espaço maior quando houver diferença
        (sobra) entre os textos da esquerda e direita em relação ao espaçamento
        mínimo determinado. O padrão é favorecer o texto da direita, já que é
        normalmente o dado relevante, como um valor ou percentual.

    :returns: Uma string contendo os textos da esquerda e direita encaixados na
        largura determinada, respeitando um espaçamento mínimo entre eles. Se
        necessário os textos serão truncados para respeitar a largura (o texto
        da esquerda será truncado no final e o texto da direita será truncado
        no início).

    :rtype: str

    """
    espacamento = largura - (len(esquerda) + len(direita))
    if espacamento < espacamento_minimo:
        espacamento = espacamento_minimo
        cpmax = int((largura - espacamento) // 2)
        cpmax_esq, cpmax_dir = cpmax, cpmax
        diferenca = largura - (espacamento + cpmax * 2)
        if diferenca > 0:
            if favorecer_direita:
                cpmax_dir += diferenca
            else:
                cpmax_esq += diferenca
        esquerda = esquerda[:cpmax_esq]
        direita = direita[-cpmax_dir:]
    return '%s%s%s' % (esquerda, ' ' * espacamento, direita)


def _quebrar_chave(chave, quebrar_partes):
    # chave: satcomum.ersat.ChaveCFeSAT
    # quebrar_partes: list[int]
    # Lista <quebrar_partes> deve possuir apenas números pares
    digitos = ''.join(chave.partes())
    partes = []
    a = 0
    for n in quebrar_partes:
        partes.append(digitos[a:a+n])
        a += n
    return partes
