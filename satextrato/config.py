# -*- coding: utf-8 -*-
#
# satextrato/config.py
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

from decimal import Decimal

import escpos.barcode

ZERO = Decimal(0)


class LarguraBobina(object):
    # FIXME: A implementação de ESC/POS deverá saber quais os valores para os
    #        modos normal, condensado e expandido;
    #
    normal = 48
    """
    Número de caracteres por linha no modo de impressão normal.
    """

    condensado = 57
    """
    Número de caracteres por linha no modo de impressão condensado.
    """

    expandido = 24
    """
    Número de caracteres por linha no modo impressão expandido.
    """


class ParametrosQRCode(object):
    tamanho_modulo = escpos.barcode.QRCODE_MODULE_SIZE_4
    """
    Determina o tamanho do módulo QRCode.
    Valor padrão é :attr:`escpos.barcode.QRCODE_MODULE_SIZE_4`
    """

    nivel_correcao = escpos.barcode.QRCODE_ERROR_CORRECTION_L
    """
    Determina o nível de correção (ECC) do QRCode.
    Valor padrão é :attr:`escpos.barcode.QRCODE_ERROR_CORRECTION_L`
    """


class NotaRodape(object):

    esquerda = 'Extrato SAT-CF-e'
    """
    Texto alinha à borda esquerda da bobina.
    """

    direita = 'http://git.io/vJRRk'
    """
    Texto alinhado à borda direita da bobina.

    .. todo::

        Usar https://github.com/blog/985-git-io-github-url-shortener
    """


class ConfiguracoesExtrato(object):

    colunas = LarguraBobina()
    """
    Referência aos atributos que determinam a largura da bobina,
    classe :class:`LarguraBobina` ou implementação especializada.
    """

    qrcode = ParametrosQRCode()
    """
    Referência aos atributos que determinam os parâmetros do QRCode,
    classe :class:`ParametrosQRCode` ou implementação especializada.
    """

    nota_rodape = NotaRodape()
    """
    Referência aos atributos que serão usados na impressão da nota de rodapé,
    classe :class:`NotaRodape` ou implementação especializada.
    """

    itens_modo_condensado = True
    """
    Indica se os dados dos itens, no corpo do Extrato do CF-e-SAT deverão ser
    impressos em modo condensado. Se não, serão impressos em modo normal.
    """

    avancar_linhas = 10
    """Número de linhas em branco a avançar ao final do Extrato do CF-e-SAT.

    .. note::

        Esta configuração será considerada mesmo se :attr:`cortar_documento`
        estiver configurado como ``True``, avançando um número ``n`` de linhas
        em branco antes de realizar o corte.

    """

    cortar_documento = True
    """Se o documento deve ser cortado ao ser concluído. Esta configuração não
    terá efeito se o equipamento não possuir uma guilhotina.

    .. note::

        Algumas impressoras possuem a guilhotina muito próxima do cabeçote de
        impressão, fazendo com que o corte elimine dados que ainda estão
        abaixo da linha de corte. Use :attr:`avancar_linhas` para determinar o
        número de linhas em branco a avançar antes de acionar a guilhotina.

    """

    cortar_parcialmente = True
    """Ao cortar o documento (:attr:`cortar_documento`), esta propriedade
    indicará se o corte deverá ser parcial ou total.
    """

    exibir_nome_consumidor = False
    """
    Indica se o nome do consumidor deve ou não ser exibido no Grupo II
    "Dados do Consumidor" do corpo do Extrato do CF-e-SAT. Esta configuração
    será considerada apenas se o elemento ``xNome`` (E04) existir no CF-e.

    .. warning::

        A documentação para impressão do extrato não diz que o nome do
        consumidor deverá ser exibido, mas que apenas o documento (CNPJ/CPF)
        deverão ser exibidos.

    """

    code128_quebrar = False
    """
    Indica se o código de barras Code128 que representa a chave do CF-e deverá
    ser quebrado em 2 partes de 22 dígitos cada ou não. Essa decisão depende
    do equipamento utilizado para impressão.
    """

    code128_altura = 96
    """
    Indica a altura preferencial em milímetros para código de barras que
    representa a chave do CF-e. A altura poderá ser ignorada se o equipamento
    utilizado para impressão não suportar esta configuração.

    A altura padrão é ``96``, que é calculado com base na média de 0,125mm por
    ponto. Assim, ``96`` significa uma altura de aproximadamente 12mm.
    """

    cliche = None
    """
    .. warning::

        Rascunho. Não implementado.

    Dados para o clichê de quaisquer Extratos CF-e-SAT, sejam eles de venda
    ou de cancelamento. Os dados do clichê serão usados como uma forma de
    melhorar a formatação das informações. Essas informações, pelo menos em
    tese, são as mesmas informações que se obteria para produzir o clichê a
    partir do CF-e.

    Trata-se de uma lista de strings. Cada string será uma linha do clichê que
    poderá indicar certos aspectos da formatação através de *hashtags*, como
    por exemplo, ``#negrito``, ``#condensado`` e ``#expandido``.

    Hashtags conflitantes serão ignoradas e vencerá a última hashtag carregada.
    Por exemplo, se houver a especificação ``#condensado`` e, sem seguida,
    a hashtag ``#expandido``, será considerado expandido se esta for a última
    hashtag lida.

    Um exemplo de especificação do clichê::

        conf.cliche = [
                u'#expandido #negrito BASE4 SISTEMAS',
                u'#negrito Base4 Sistemas Ltda ME',
                u'#condensado Rua Armando Gulim, 65',
                u'#condensado Parque Glória III',
                u'#condensado Catanduva/SP - CEP 15807-250',]

    """


conf = ConfiguracoesExtrato()
"""
Variável de módulo utilizada como base para as configurações de impressão.
"""
