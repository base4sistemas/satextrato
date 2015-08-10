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

import xml.etree.ElementTree as ET

from datetime import datetime
from decimal import Decimal

from satcomum import br
from satcomum import ersat

from .config import conf
from .base import ExtratoCFe


class ExtratoCFeCancelamento(ExtratoCFe):
    """Implementa impressão do extrato do CF-e de cancelamento."""


    def __init__(self, fp_venda, fp_cancelamento, impressora):
        """Inicia uma instância de :class:`ExtratoCFeCancelamento`.

        :param fp_venda: Um objeto *file-like* para o documento XML que
            contém o CF-e de venda cancelado (o documento eletrônico da venda
            que fora cancelada).

        :param fp_cancelamento: Um objeto *file-like* para o documento XML que
            contém o CF-e de cancelamento (o documento eletrônico que autoriza
            o cancelamento da venda).

        :param impressora: Um objeto :class:`escpos.impl.epson.GenericESCPOS`
            ou especialização.

        """
        super(ExtratoCFeCancelamento, self).__init__(
                fp_cancelamento, impressora)
        # (!) `self.root` mantém uma referência para o elemento `CFeCanc`
        self._tree_venda = ET.parse(fp_venda)
        self.root_venda = self._tree_venda.getroot() # ref. elemento `CFe`


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
        self.texto(u'CUPOM FISCAL ELETRÔNICO - SAT')
        self.texto(u'CANCELAMENTO')
        self.indicacao_de_teste()
        self.negrito()
        self.esquerda()
        self.separador()
        self.negrito()
        self.condensado()
        self.texto(u'DADOS DO CUPOM FISCAL ELETRÔNICO CANCELADO')
        self.condensado()
        self.negrito()


    def corpo_dados_consumidor(self):
        documento = self.root.findtext('./infCFe/dest/CNPJ') or \
                self.root.findtext('./infCFe/dest/CPF') or ''

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

        infCFe = self.root_venda.find('./infCFe') # (!) infCFe do CF-e de venda
        sat_numero_serie = 'SAT no. {}'.format(infCFe.findtext('ide/nserieSAT'))

        datahora = datetime.strptime('{}{}'.format(
                infCFe.findtext('ide/dEmi'),
                infCFe.findtext('ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')

        chave = ersat.ChaveCFeSAT(infCFe.attrib['Id']) # CF-e de venda

        self.normal()
        self.centro()
        self.avanco()
        self.negrito()
        self.texto(sat_numero_serie)
        self.negrito()
        self.texto(datahora_emissao)

        self.avanco()
        self.esquerda()
        self.condensado()
        self.texto(' '.join(chave.partes()))
        self.condensado()

        self.avanco()
        self.centro()

        self.chave_cfe_code128(chave)

        self.avanco(2)
        self.impressora.qrcode(ersat.dados_qrcode(self._tree_venda),
                qrcode_module_size=conf.qrcode.tamanho_modulo,
                qrcode_ecc_level=conf.qrcode.nivel_correcao)



    def rodape(self):

        infCFe = self.root.find('./infCFe') # (!) infCFe do CF-e de cancelamento
        sat_numero_serie = 'SAT no. {}'.format(infCFe.findtext('ide/nserieSAT'))

        datahora = datetime.strptime('{}{}'.format(
                infCFe.findtext('ide/dEmi'),
                infCFe.findtext('ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')

        chave = ersat.ChaveCFeSAT(infCFe.attrib['Id']) # CF-e de cancelamento

        self.normal()
        self.avanco(2)
        self.separador()
        self.centro()
        self.negrito()
        self.quebrar(u'DADOS DO CUPOM FISCAL ELETRÔNICO DE CANCELAMENTO')
        self.avanco()
        self.texto(sat_numero_serie)
        self.negrito()
        self.texto(datahora_emissao)

        self.avanco()
        self.esquerda()
        self.condensado()
        self.texto(' '.join(chave.partes()))
        self.condensado()

        self.avanco()
        self.centro()

        self.chave_cfe_code128(chave)

        self.avanco(2)
        self.impressora.qrcode(ersat.dados_qrcode(self._tree),
                qrcode_module_size=conf.qrcode.tamanho_modulo,
                qrcode_ecc_level=conf.qrcode.nivel_correcao)
