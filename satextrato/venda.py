# -*- coding: utf-8 -*-
#
# satextrato/venda.py
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

from datetime import datetime

from satcomum import br
from satcomum import util

from .config import ZERO
from .config import conf
from .base import _bordas
from .base import ExtratoCFe


class ExtratoCFeVenda(ExtratoCFe):

    anotacoes_antes_obs_contribuinte = None

    anotacoes_corpo = None


    def __init__(self, xmlstr, impressora, resumido=False):
        super(ExtratoCFeVenda, self).__init__(xmlstr, impressora)
        self._resumido = resumido
        self.anotacoes_antes_obs_contribuinte = []
        self.anotacoes_corpo = []


    def apresentar_item(self, item):
        """
        Apresenta um item (produto/serviço) do CF-e.

        Nesta abordagem, os detalhes do item utilizam uma linha exclusiva,
        abaixo das linhas que mostram o número do item, código e descrição.
        Por exemplo (considerando 48 caracteres por linha):

        .. sourcecode:: text

                    10        20        30        40      48 :
            ....:....|....:....|....:....|....:....|....:..! :
            001 7891234567891 PELLENTESQUE HABITANT MORBI    :
            TRISTIQUE SENECTUS ET NETUS ET MALESUADA FAMES   :
            AC TURPIS EGESTAS VESTIBULUM TORTOR QUAM AMET    :
                                   1 UN x 12,75 (0,30) 12,75 :

        Mesmo no caso em que o nome do produto é muito pequeno, serão utilizadas
        duas linhas para apresentar o item.

        .. sourcecode:: text

                    10        20        30        40      48 :
            ....:....|....:....|....:....|....:....|....:..! :
            001 7891234567891 AB                             :
                                   1 UN x 12,75 (0,30) 12,75 :

        Mas, como é muito rara a situação em que o produto poderia ser
        apresentado em uma única linha, o ganho na facilidade de leitura
        compensa (pelo menos para o consumidor).

        Este método ainda faz um esforço de apresentar o item em apenas uma
        linha tentando "encaixar" o detalhamento do item na mesma linha de
        descrição, desde que caiba. Isso pode ser mais comum, se estiver
        configurado para apresentar os itens em modo condensado (padrão).
        """
        nItem = int(item.root_attr('nItem'))
        cProd = item.text('prod/cProd')
        xProd = item.text('prod/xProd')
        qCom = item.decimal('prod/qCom')
        uCom = item.text('prod/uCom')
        vUnCom = item.decimal('prod/vUnCom')
        vProd = item.decimal('prod/vProd')
        vItem12741 = item.decimal('imposto/vItem12741', default=ZERO)

        if vItem12741.is_zero():
            detalhe = u'{:s} {:s} x {:n} {:n}'.format(
                    util.texto_decimal(qCom), uCom, vUnCom, vProd)
        else:
            detalhe = u'{:s} {:s} x {:n} ({:n}) {:n}'.format(
                    util.texto_decimal(qCom), uCom, vUnCom, vItem12741, vProd)

        texto_item = u'{0:03d} {1:s} {2:s}'.format(nItem, cProd, xProd)

        self.normal()
        self.esquerda()

        if conf.itens_modo_condensado:
            self.condensado() # liga

        largura = self._colunas
        linhas = textwrap.wrap(texto_item, largura)

        ultima_linha = linhas[-1]

        if (len(ultima_linha) + len(detalhe) + 1) > largura:
            # não cabe, o detalhe será apresentado em uma linha exclusiva
            linhas.append(_bordas('', detalhe,
                    largura=largura, espacamento_minimo=1))
        else:
            # cabe; o detalhe será apresentado junto com a última linha
            linhas[-1] = _bordas(ultima_linha, detalhe,
                    largura=largura, espacamento_minimo=1)

        for linha in linhas:
            self.texto(linha)

        if conf.itens_modo_condensado:
            self.condensado() # desliga

        return self


    def corpo(self):
        self.corpo_I_titulo()
        self.corpo_II_consumidor()
        if not self._resumido:
            self.corpo_III_legenda()
            self.corpo_IV_itens()
        self.corpo_V_total_cupom()
        self.corpo_VI_meio_pagamento()
        self.corpo_VII_observacoes_fisco()
        self.corpo_VIII_dados_entrega()

        if self.anotacoes_antes_obs_contribuinte:
            self.normal()
            self.esquerda()
            self.avanco()
            for anotacao in self.anotacoes_antes_obs_contribuinte:
                self.texto(anotacao)

        self.corpo_IX_observacoes_contribuinte()

        if self.anotacoes_corpo:
            self.normal()
            self.esquerda()
            self.avanco()
            for anotacao in self.anotacoes_corpo:
                self.texto(anotacao)

        self.anotacoes_antes_obs_contribuinte[:] = []
        self.anotacoes_corpo[:] = []


    def corpo_I_titulo(self):
        self.normal()
        self.centro()
        self.negrito()
        self.texto('Extrato No. {}'.format(self.numero_extrato()))
        self.texto(u'CUPOM FISCAL ELETRÔNICO - SAT')
        self.indicacao_de_teste()
        self.negrito()
        self.esquerda()
        self.separador()


    def corpo_II_consumidor(self):
        # (!) Com a introdução do Anexo I, "Correlação de Campos do Extrato
        #     do CF-e-SAT", parece que ficou claro que o grupo II não deverá
        #     exibir o nome do consumidor, nem se estiver presente.
        #
        #     Como havia implementado originalmente com o nome, apenas
        #     deixei configurável a apresentação do nome do consumidor.
        #
        nome = self.xml.text('infCFe/dest/xNome', default='')
        documento = self.xml.text('infCFe/dest/CPF',
            alternative_xpath='infCFe/dest/CNPJ', default='')

        if br.is_cnpjcpf(documento):
            self.normal()
            self.esquerda()
            self.texto('CPF/CNPJ do Consumidor: {}'.format(
                    br.as_cnpjcpf(documento)))

            if nome and conf.exibir_nome_consumidor:
                self.quebrar(nome)

            self.separador()


    def corpo_III_legenda(self):
        legendas = ' | '.join([
                '#', 'COD', 'DESC', 'QTD', 'UN',
                'VL UN R$', '(VL TR R$)*', 'VL ITEM R$',])

        self.normal()
        self.condensado()
        self.quebrar(legendas)
        self.condensado()
        self.separador()

        self.anotacoes_antes_obs_contribuinte.append(
                u'*Valor aproximado dos tributos do item.')


    def corpo_IV_itens(self):

        for item in self.xml.iterate('infCFe/det'):
            self.apresentar_item(item)

            vProd = item.decimal('prod/vProd')
            vDesc = item.decimal('prod/vDesc', default=ZERO)
            vRatDesc = item.decimal('prod/vRatDesc', default=ZERO)
            vOutro = item.decimal('prod/vOutro', default=ZERO)
            vRatAcr = item.decimal('prod/vRatAcr', default=ZERO)

            # (!) Do modo como está implementado, descontos e acréscimos
            # serão ambos tratados como se pudessem coexistir, embora o
            # Manual de Orientação seja claro quando diz que "valores de
            # descontos e acréscimos são mutuamente exclusivos".
            forcar_exibir = False

            if not vDesc.is_zero() or forcar_exibir:
                self.bordas('desconto sobre item', '- {:n}'.format(vDesc))

            if not vRatDesc.is_zero() or forcar_exibir:
                self.bordas('rateio de desconto sobre subtotal',
                        '- {:n}'.format(vRatDesc))

            if not vOutro.is_zero() or forcar_exibir:
                self.bordas(u'acréscimo sobre item', '+ {:n}'.format(vOutro))

            if not vRatAcr.is_zero() or forcar_exibir:
                self.bordas(u'rateio de acréscimo sobre subtotal',
                        '+ {:n}'.format(vRatAcr))

            # item tributado pelo ISSQN?
            if item.text('imposto/ISSQN/cNatOp', default='@') != '@':
                # o campo cNatOp (U09) retornou algo diferente do valor default
                # indicado; logo, assume que o item foi tributado pelo ISSQN...
                vBC = item.decimal('imposto/ISSQN/vBC', default=ZERO)
                vDeducISSQN = item.decimal('imposto/ISSQN/vDeducISSQN',
                        default=ZERO)

                if not vDeducISSQN.is_zero():
                    self.bordas(u'dedução para ISSQN',
                            '- {:n}'.format(vDeducISSQN))

                self.bordas(u'base de cálculo ISSQN', '{:n}'.format(vBC))


    def corpo_V_total_cupom(self):

        # calcula o total de descontos apenas dos itens tributados por ISSQN,
        # usando os campos vDesc (I12) e vOutro (I13);
        issqn_total_desc = ZERO
        issqn_total_acres = ZERO

        for item in self.xml.iterate('infCFe/det'):
            # item tributado pelo ISSQN?
            if item.text('imposto/ISSQN/cNatOp', default='@') != '@':
                # o campo cNatOp (U09) retornou algo diferente do valor default
                # indicado; logo, assume que o item foi tributado pelo ISSQN...
                issqn_total_desc += item.decimal('prod/vDesc', default=ZERO)
                issqn_total_acres += item.decimal('prod/vOutro', default=ZERO)

        # total de descontos sobre itens (vDesc, W05);
        # total de outras despesas acessórias sobre itens (vOutro W10);
        total_desc = self.xml.decimal(
                'infCFe/total/ICMSTot/vDesc', default=ZERO) + issqn_total_desc

        total_acres = self.xml.decimal(
                'infCFe/total/ICMSTot/vOutro', default=ZERO) + issqn_total_acres

        # vProd (W04)
        vProd = self.xml.decimal('infCFe/total/ICMSTot/vProd')
        vDescSubtot = self.xml.decimal(
                'infCFe/total/DescAcrEntr/vDescSubtot', default=ZERO)
        vAcresSubtot = self.xml.decimal(
                'infCFe/total/DescAcrEntr/vAcresSubtot', default=ZERO)

        self.normal()
        self.avanco()

        forcar_exibir = False

        ha_desc_itens = not total_desc.is_zero() or forcar_exibir
        ha_desc_subtotal = not vDescSubtot.is_zero() or forcar_exibir
        ha_desconto = ha_desc_itens or ha_desc_subtotal or forcar_exibir

        ha_acres_itens = not total_acres.is_zero() or forcar_exibir
        ha_acres_subtotal = not vAcresSubtot.is_zero() or forcar_exibir
        ha_acrescimo = ha_acres_itens or ha_acres_subtotal or forcar_exibir

        if ha_desconto or ha_acrescimo:
            # há desconto ou acréscimo sobre os itens e/ou sobre o subtotal
            self.bordas('Total bruto de itens', '{:n}'.format(vProd))

        if ha_desc_itens:
            # há desconto sobre itens
            self.bordas('Total de descontos sobre item',
                    '- {:n}'.format(total_desc))

        if ha_desc_subtotal:
            # há desconto sobre o subtotal
            self.bordas('Desconto sobre subtotal', '- {:n}'.format(vDescSubtot))

        if ha_acres_itens:
            # há acréscimo sobre itens
            self.bordas(u'Total de acréscimos sobre item',
                    '+ {:n}'.format(total_acres))

        if ha_acres_subtotal:
            # há acréscimo sobre o subtotal
            self.bordas(u'Acréscimo sobre subtotal',
                    '+ {:n}'.format(vAcresSubtot))

        vCFe = self.xml.decimal('infCFe/total/vCFe')

        self.negrito()
        self.bordas('TOTAL R$', '{:n}'.format(vCFe))
        self.negrito()


    def corpo_VI_meio_pagamento(self):
        self.normal()
        self.avanco()

        for pagto in self.xml.iterate('infCFe/pgto/MP'):
            self.bordas(util.meio_pagamento(pagto.text('cMP')),
                    '{:n}'.format(pagto.decimal('vMP')))

        valor_troco = self.xml.decimal('infCFe/pgto/vTroco')
        if not valor_troco.is_zero():
            self.bordas('Troco R$', '{:n}'.format(valor_troco))


    def corpo_VII_observacoes_fisco(self):
        """
        Grupo VII, Observações do Fisco. Redação atual, efeitos até 31-12-2016.
        Usa o atributo ``xCampo`` (Z04) e o elemento ``xTexto`` (Z05):

        .. sourcecode:: xml

            <CFe>
              <infCFe>
                <infAdic>
                  <obsFisco xCampo="Foo">
                      <xTexto>Conteúdo de Foo</xTexto>
                  </obsFisco>
                  <obsFisco xCampo="Bar">
                      <xTexto>Conteúdo de Bar</xTexto>
                  </obsFisco>
                </infAdic>
              </infCFe>
            </CFe>

        Nova redação, efeitos a partir de 01-01-2017.
        Usa o atributo ``xCampo`` (ZA02) e o elemento ``xTexto`` (ZA03):

        .. sourcecode:: xml

            <CFe>
              <infCFe>
                <obsFisco xCampo="Spam">
                    <xTexto>Conteúdo de Spam</xTexto>
                </obsFisco>
                <obsFisco xCampo="Eggs">
                    <xTexto>Conteúdo de Eggs</xTexto>
                </obsFisco>
              </infCFe>
            </CFe>

        """
        iniciado = False

        for obs in self.xml.iterate('infCFe/infAdic/obsFisco'):

            if not iniciado:
                self.normal()
                self.esquerda()
                self.avanco()
                self.condensado()
                iniciado = True

            self.quebrar(u'{}: {}'.format(
                    obs.root_attr('xCampo'),
                    obs.text('xTexto')))

        if iniciado:
            self.condensado() # desliga


    def corpo_VIII_dados_entrega(self):

        logradouro = self.xml.text('infCFe/entrega/xLgr', default='')
        if not logradouro:
            return

        # há endereço de entrega;
        # prepara para imprimir, por que será necessário considerar o número
        # de colunas para construir o endereço o mais legível possível;
        self.normal()

        # uma vez que há o logradouro, então existe um endereço de entrega;
        # se existe um endereço de entrega então os únicos elementos que
        # NÃO SÃO OBRIGATÓRIOS são `nro` (G03) e `xCpl` (G04);
        numero = self.xml.text('infCFe/entrega/nro', default='')
        complemento = self.xml.text('infCFe/entrega/xCpl', default='')
        bairro = self.xml.text('infCFe/entrega/xBairro')

        if numero: # número não é obrigatório
            # mas existe, então o coloca próximo ao logradouro
            logradouro = u'{}, {}'.format(logradouro, numero)

        if complemento: # complemento não é obrigatório
            # faz um esforço para manter o complemento na mesma linha que o
            # logradouro/número se couber, senão o complemento irá usar uma
            # linha exclusiva...
            if len(logradouro) + len(complemento) < self._colunas:
                # ok, mantém o complemento na mesma linha que o logradouro
                logradouro = u'{}, {}'.format(logradouro, complemento)
                complemento = '' # ignora a linha que deveria conter o xCpl

        cidade = u'{}/{}'.format(
                self.xml.text('infCFe/entrega/xMun'),
                self.xml.text('infCFe/entrega/UF'))

        partes_endereco = [logradouro, complemento, bairro, cidade,]
        endereco = '\r\n'.join([e for e in partes_endereco if e])

        self.esquerda()
        self.separador()
        self.negrito()
        self.texto('DADOS PARA ENTREGA')
        self.negrito()
        self.quebrar(u'Endereço: {}'.format(endereco))

        nome_destinatario = self.xml.text('infCFe/dest/xNome', default='')
        if nome_destinatario:
            self.quebrar(u'Destinatário: {}'.format(nome_destinatario))


    def corpo_IX_observacoes_contribuinte(self):
        infCpl = self.xml.text('infCFe/infAdic/infCpl', default='')
        vCFeLei12741 = self.xml.decimal(
                'infCFe/total/vCFeLei12741', default=ZERO)

        if infCpl or not vCFeLei12741.is_zero():
            self.normal()
            self.esquerda()
            self.separador()
            self.negrito()
            self.texto(u'OBSERVAÇÕES DO CONTRIBUINTE')
            self.negrito()

            if infCpl:
                self.condensado()
                self.quebrar(infCpl)
                self.condensado()

            if not vCFeLei12741.is_zero():
                self.condensado()
                self.quebrar(u'Valor aproximado dos tributos deste cupom')
                self.bordas(
                        u'(Lei Fed. 12.741/2012) R$',
                        '{:n}'.format(vCFeLei12741))
                self.condensado()


    def rodape(self):

        sat_numero_serie = 'SAT no. {}'.format(
                self.xml.text('infCFe/ide/nserieSAT'))

        datahora = datetime.strptime('{}{}'.format(
                self.xml.text('infCFe/ide/dEmi'),
                self.xml.text('infCFe/ide/hEmi')), '%Y%m%d%H%M%S')

        datahora_emissao = datahora.strftime('%d/%m/%Y - %H:%M:%S')

        chave_cfe = self.xml.attr('infCFe', 'Id')[3:] # ignora prefixo "CFe"
        chave_consulta_partes = ' '.join(util.partes_chave_cfe(chave_cfe))

        self.normal()
        self.separador()
        self.centro()
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

        self.chave_cfe_code128(chave_cfe)

        self.avanco(2)
        self.impressora.qrcode(util.dados_qrcode(self.xml),
                qrcode_module_size=conf.qrcode.tamanho_modulo,
                qrcode_ecc_level=conf.qrcode.nivel_correcao)
