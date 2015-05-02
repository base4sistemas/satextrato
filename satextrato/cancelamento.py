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

from datetime import datetime

from satcomum import br
from satcomum import util

from .config import conf
from .base import ExtratoCFe


class ExtratoCFeCancelamento(ExtratoCFe):


    def __init__(self, xmlstr, xmlstr_cfe_cancelado, impressora):
        """

        :param xmlstr: String (unicode) contendo o XML do CF-e-SAT de
            cancelamento.

        :param xmlstr_cfe_cancelado: String (unicode) contendo o XML do
            CF-e-SAT de venda para o qual o extrato de cancelamento será
            emitido (o CF-e de venda que foi cancelado).

        :param impressora: Um objeto :class:`escpos.impl.epson.GenericESCPOS`
            ou especialização.
        """
        super(ExtratoCFeCancelamento, self).__init__(xmlstr, impressora)
        self._xmlstr_cfe_cancelado = xmlstr_cfe_cancelado
        self.xml_cfe_cancelado = \
                util.XMLFacadeFromString(self._xmlstr_cfe_cancelado)


    def corpo(self):
        self.corpo_titulo()
        self.corpo_dados_consumidor()
        self.corpo_total_cupom()
        self.corpo_dados_cfe_cancelado()


    def corpo_titulo(self):
        self.normal()
        self.centro()
        self.negrito()
        self.texto('Extrato No. {}'.format(self.xml.text('infCFe/ide/nCFe')))
        self.texto(u'CUPOM FISCAL ELETRÔNICO - SAT')
        self.texto(u'CANCELAMENTO')
        self.negrito()
        self.esquerda()
        self.separador()
        self.negrito()
        self.condensado()
        self.texto(u'DADOS DO CUPOM FISCAL ELETRÔNICO CANCELADO')
        self.condensado()
        self.negrito()


    def corpo_dados_consumidor(self):
        documento = self.xml.text('infCFe/dest/CPF',
                alternative_xpath='infCFe/dest/CNPJ', default='')

        if br.is_cnpjcpf(documento):
            self.normal()
            self.esquerda()
            self.avanco()
            self.texto('CPF/CNPJ do Consumidor: {}'.format(
                    br.as_cnpjcpf(documento)))
        else:
            # apenas normaliza e avança;
            # o total do cupom fiscal cancelado será impresso em seguida;
            self.normal()
            self.avanco()


    def corpo_total_cupom(self):
        self.normal()
        self.esquerda()
        self.negrito()
        self.texto('TOTAL R$ {:n}'.format(
                self.xml.decimal('infCFe/total/vCFe')))
        self.negrito()


    def corpo_dados_cfe_cancelado(self):

        sat_numero_serie = 'SAT no. {}'.format(
                self.xml.text('infCFe/ide/nserieSAT'))

        datahora = datetime.strptime('{}{}'.format(
                self.xml.text('infCFe/dEmi'),
                self.xml.text('infCFe/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')

        chave = self.xml.attr('infCFe', 'chCanc')[3:] # ignora prefixo "CFe"
        chave_consulta_partes = ' '.join(util.partes_chave_cfe(chave))

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
        self.texto(chave_consulta_partes)
        self.condensado()

        self.avanco()
        self.centro()

        self.chave_cfe_code128(chave)

        self.avanco(2)
        self.impressora.qrcode(util.dados_qrcode(self.xml_cfe_cancelado),
                qrcode_module_size=conf.qrcode.tamanho_modulo,
                qrcode_ecc_level=conf.qrcode.nivel_correcao)



    def rodape(self):

        sat_numero_serie = 'SAT no. {}'.format(
                self.xml.text('infCFe/ide/nserieSAT'))

        datahora = datetime.strptime('{}{}'.format(
                self.xml.text('infCFe/ide/dEmi'),
                self.xml.text('infCFe/ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')

        chave = self.xml.attr('infCFe', 'Id')[3:] # ignora prefixo "CFe"
        chave_consulta_partes = ' '.join(util.partes_chave_cfe(chave))

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
        self.texto(chave_consulta_partes)
        self.condensado()

        self.avanco()
        self.centro()

        self.chave_cfe_code128(chave)

        self.avanco(2)
        self.impressora.qrcode(util.dados_qrcode(self.xml),
                qrcode_module_size=conf.qrcode.tamanho_modulo,
                qrcode_ecc_level=conf.qrcode.nivel_correcao)
