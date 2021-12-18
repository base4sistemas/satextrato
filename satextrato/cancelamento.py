# -*- coding: utf-8 -*-
#
# satextrato/cancelamento.py
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
from __future__ import unicode_literals

import xml.etree.ElementTree as ET

from datetime import datetime
from decimal import Decimal

import six

from satcomum import br
from satcomum import ersat

from .base import ExtratoCFe


class ExtratoCFeCancelamento(ExtratoCFe):
    """Implementa impressão do extrato do CF-e de cancelamento."""

    def __init__(self, fp_venda, fp_canc, impressora, config=None):
        """Inicia uma instância de :class:`ExtratoCFeCancelamento`.

        :param fp_venda: Um *file object* para o XML do CF-e de venda.
            Neste caso, o documento XML da venda que foi cancelada.

        :param fp_canc: Um *file object* para o XML do CF-e de cancelamento.

        :param impressora: Um instância (ou subclasse, especialização) de
            :class:`escpos.impl.epson.GenericESCPOS` usado para efetivamente
            imprimir o extrato.

        :param config: Opcional.
            Uma instância de :class:`satextrato.config.Configuracoes`.
            Se não informado, serão usados valores padrão.

        """
        super(ExtratoCFeCancelamento, self).__init__(
                fp_canc,
                impressora,
                config=config
            )
        # (!) `self.root` mantém uma referência para o elemento `CFeCanc`
        self._tree_venda = ET.parse(fp_venda)
        self.root_venda = self._tree_venda.getroot()  # ref. elemento `CFe`

    def corpo(self):
        self.corpo_titulo()
        self.corpo_dados_consumidor()
        self.corpo_total_cupom()
        self.corpo_dados_cfe_cancelado()

    def corpo_titulo(self):
        self.normal()
        self.centro()
        self.negrito()
        self.texto('Extrato No. {}'.format(self.numero_extrato()))
        self.texto('CUPOM FISCAL ELETRÔNICO - SAT')
        self.texto('CANCELAMENTO')
        self.indicacao_de_teste()
        self.negrito()
        self.esquerda()
        self.separador()
        self.negrito()
        self.condensado()
        self.texto('DADOS DO CUPOM FISCAL ELETRÔNICO CANCELADO')
        self.condensado()
        self.negrito()

    def corpo_dados_consumidor(self):
        documento = (
                self.root.findtext('./infCFe/dest/CNPJ')
                or self.root.findtext('./infCFe/dest/CPF')
                or ''
            )

        if br.is_cnpjcpf(documento):
            self.normal()
            self.esquerda()
            self.avanco()
            self.texto('CPF/CNPJ do Consumidor: {}'.format(
                    br.as_cnpjcpf(documento)))
        else:
            # não há um consumidor identificado; apenas normaliza e avança
            self.normal()
            self.avanco()

    def corpo_total_cupom(self):
        self.normal()
        self.esquerda()
        self.negrito()
        self.texto('TOTAL R$ {:n}'.format(
                Decimal(self.root.findtext('./infCFe/total/vCFe'))))
        self.negrito()

    def corpo_dados_cfe_cancelado(self):

        infCFe = self.root_venda.find('./infCFe')  # (!) infCFe da venda
        sat_numero_serie = 'SAT no. {}'.format(
                infCFe.findtext('ide/nserieSAT')
            )

        datahora = datetime.strptime('{}{}'.format(
                infCFe.findtext('ide/dEmi'),
                infCFe.findtext('ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')
        if six.PY2:
            # Python 2: strftime() resulta em str, que precisará ser passado
            # como um objeto unicode para unidecode (em self.texto())
            datahora_emissao = datahora_emissao.decode('utf-8')

        self.normal()
        self.separador()
        self.centro()
        self.negrito()
        self.texto(sat_numero_serie)
        self.negrito()
        self.texto(datahora_emissao)
        self.avanco()

        self.chave_cfe_code128(ersat.ChaveCFeSAT(infCFe.attrib['Id']))
        self.avanco()

        self.centro()
        self.impressora.qrcode(
                ersat.dados_qrcode(self._tree_venda),
                qrcode_module_size=self._config.qrcode.tamanho_modulo,
                qrcode_ecc_level=self._config.qrcode.nivel_correcao
            )

    def rodape(self):
        infCFe = self.root.find('./infCFe')  # (!) infCFe do cancelamento
        sat_numero_serie = 'SAT no. {}'.format(
                infCFe.findtext('ide/nserieSAT')
            )

        datahora = datetime.strptime('{}{}'.format(
                infCFe.findtext('ide/dEmi'),
                infCFe.findtext('ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')
        if six.PY2:
            # Python 2: strftime() resulta em str, que precisará ser passado
            # como um objeto unicode para unidecode (em self.texto())
            datahora_emissao = datahora_emissao.decode('utf-8')

        self.normal()
        self.separador()
        self.centro()
        self.negrito()
        self.quebrar('DADOS DO CUPOM FISCAL ELETRÔNICO DE CANCELAMENTO')
        self.texto(sat_numero_serie)
        self.negrito()
        self.texto(datahora_emissao)
        self.avanco()

        self.chave_cfe_code128(ersat.ChaveCFeSAT(infCFe.attrib['Id']))
        self.avanco()

        self.centro()
        self.impressora.qrcode(
                ersat.dados_qrcode(self._tree),
                qrcode_module_size=self._config.qrcode.tamanho_modulo,
                qrcode_ecc_level=self._config.qrcode.nivel_correcao
            )

        self.qrcode_mensagem()
