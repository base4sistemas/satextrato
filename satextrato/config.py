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

import logging
import os

from ConfigParser import SafeConfigParser
from collections import namedtuple

from escpos import barcode


SECAO_QRCODE = 'qrcode'
SECAO_CODE128 = 'code128'
SECAO_RODAPE = 'rodape'
SECAO_CUPOM = 'cupom'

CONFIG_DIR = os.path.join(os.path.expanduser('~'), 'satcfe')

CONFIG_ARQUIVO_PADRAO = os.path.join(CONFIG_DIR, 'extrato.cfg')

_TAMANHO_CHAVE_CFESAT = 44

_CupomConf = namedtuple('_CupomConf', [
        'itens_modo_condensado',
        'avancar_linhas',
        'cortar_documento',
        'cortar_parcialmente',
        'exibir_nome_consumidor',])

_QRCodeConf = namedtuple('_QRCodeConf', [
        'tamanho_modulo',
        'nivel_correcao',
        'nome_aplicativo',
        'mensagem',
        'mensagem_modo_condensado',])

_Code128Conf = namedtuple('_Code128Conf', [
        'ignorar',
        'altura',
        'quebrar',
        'quebrar_partes',
        'truncar',
        'truncar_tamanho',])

_RodapeConf = namedtuple('_RodapeConf', ['direita', 'esquerda'])

cupom = None
qrcode = None
code128 = None
rodape = None

logger = logging.getLogger('satextrato.config')


def configurar(arquivo=None):
    """Esta função dá ao aplicativo usuário uma chance de definir onde o arquivo
    de configurações deve existir. Chamadas subsequentes à esta função não terão
    efeito, a menos que seja invocada a função :func:`reconfigurar`.

    :param str arquivo: Caminho completo para o arquivo de configurações.

    """
    global cupom
    global qrcode
    global code128
    global rodape

    if all([cupom, qrcode, code128, rodape]):
        return

    arquivo = arquivo or CONFIG_ARQUIVO_PADRAO
    _garantir_diretorio(arquivo)

    parser = SafeConfigParser()
    modificado = False

    if os.path.isfile(arquivo):
        with open(arquivo, 'r') as fp:
            parser.readfp(fp)

    if not parser.has_section(SECAO_QRCODE):
        parser.add_section(SECAO_QRCODE)
        parser.set(SECAO_QRCODE, 'tamanho_modulo', str(barcode.QRCODE_MODULE_SIZE_4))
        parser.set(SECAO_QRCODE, 'nivel_correcao', barcode.QRCODE_ERROR_CORRECTION_L)
        parser.set(SECAO_QRCODE, 'nome_aplicativo', 'De Olho Na Nota')
        parser.set(SECAO_QRCODE, 'mensagem', 'Consulte o QRCode pelo '
                'aplicativo %(nome_aplicativo)s, disponivel na '
                'AppStore (Apple) e PlayStore (Android)')
        parser.set(SECAO_QRCODE, 'mensagem_modo_condensado', 'yes')
        modificado = True

    if not parser.has_section(SECAO_CODE128):
        parser.add_section(SECAO_CODE128)
        parser.set(SECAO_CODE128, 'ignorar', 'no')
        parser.set(SECAO_CODE128, 'altura', '56')
        parser.set(SECAO_CODE128, 'quebrar', 'no')
        parser.set(SECAO_CODE128, 'quebrar_partes', '22,22')
        parser.set(SECAO_CODE128, 'truncar', 'no')
        parser.set(SECAO_CODE128, 'truncar_tamanho', '44')
        modificado = True

    if not parser.has_section(SECAO_RODAPE):
        parser.add_section(SECAO_RODAPE)
        parser.set(SECAO_RODAPE, 'direita', 'http://git.io/vJRRk')
        parser.set(SECAO_RODAPE, 'esquerda', 'Extrato CF-e-SAT')
        modificado = True

    if not parser.has_section(SECAO_CUPOM):
        parser.add_section(SECAO_CUPOM)
        parser.set(SECAO_CUPOM, 'itens_modo_condensado', 'yes')
        parser.set(SECAO_CUPOM, 'avancar_linhas', '7')
        parser.set(SECAO_CUPOM, 'cortar_documento', 'no')
        parser.set(SECAO_CUPOM, 'cortar_parcialmente', 'no')
        parser.set(SECAO_CUPOM, 'exibir_nome_consumidor', 'no')
        modificado = True

    if modificado:
        with open(arquivo, 'wb') as fp:
            parser.write(fp)

    cupom=_CupomConf(
            itens_modo_condensado=parser.getboolean(SECAO_CUPOM, 'itens_modo_condensado'),
            avancar_linhas=parser.getint(SECAO_CUPOM, 'avancar_linhas'),
            cortar_documento=parser.getboolean(SECAO_CUPOM, 'cortar_documento'),
            cortar_parcialmente=parser.getboolean(SECAO_CUPOM, 'cortar_parcialmente'),
            exibir_nome_consumidor=parser.getboolean(SECAO_CUPOM, 'exibir_nome_consumidor'))

    qrcode=_QRCodeConf(
            tamanho_modulo=parser.getint(SECAO_QRCODE, 'tamanho_modulo'),
            nivel_correcao=parser.get(SECAO_QRCODE, 'nivel_correcao'),
            nome_aplicativo=parser.get(SECAO_QRCODE, 'nome_aplicativo'),
            mensagem=parser.get(SECAO_QRCODE, 'mensagem'),
            mensagem_modo_condensado=parser.getboolean(SECAO_QRCODE, 'mensagem_modo_condensado'))

    code128=_Code128Conf(
            ignorar=parser.getboolean(SECAO_CODE128, 'ignorar'),
            altura=parser.getint(SECAO_CODE128, 'altura'),
            quebrar=parser.getboolean(SECAO_CODE128, 'quebrar'),
            quebrar_partes=_converter_quebrar_partes(arquivo, parser),
            truncar=parser.getboolean(SECAO_CODE128, 'truncar'),
            truncar_tamanho=parser.getint(SECAO_CODE128, 'truncar_tamanho'))

    rodape=_RodapeConf(
            direita=parser.get(SECAO_RODAPE, 'direita'),
            esquerda=parser.get(SECAO_RODAPE, 'esquerda'))


def reconfigurar(arquivo=None):
    global cupom
    global qrcode
    global code128
    global rodape
    cupom = None
    qrcode = None
    code128 = None
    rodape = None
    configurar(arquivo=arquivo)


def _converter_quebrar_partes(arquivo, parser):
    quebrar_partes = parser.get(SECAO_CODE128, 'quebrar_partes')
    try:
        partes = [int(p) for p in quebrar_partes.split(',')]
    except ValueError:
        raise ValueError('Configuracoes do extrato do CF-e-SAT, Code128 em '
                'partes deve especificar as partes em valores inteiros, pares '
                'e separados por virgulas; quebrar_partes={quebrar_partes!r} '
                '(secao={secao!r}, arquivo={arquivo!r})'.format(
                        secao=SECAO_CODE128,
                        arquivo=arquivo,
                        quebrar_partes=quebrar_partes))
    else:
        calculado = sum(partes)
        if calculado != _TAMANHO_CHAVE_CFESAT:
            raise ValueError('Configuracoes do extrato do CF-e-SAT, Code128 em '
                    'partes deve especificar as partes em valores inteiros, '
                    'pares e separados por virgulas, cuja soma seja igual a '
                    '{tamanho_esperado!r}, exatamente o numero de digitos da '
                    'chave do CF-e; quebrar_partes={quebrar_partes!r} '
                    '(calculado={calculado!r}, secao={secao!r}, '
                    'arquivo={arquivo!r})'.format(
                            arquivo=arquivo,
                            calculado=calculado,
                            secao=SECAO_CODE128,
                            quebrar_partes=quebrar_partes,
                            tamanho_esperado=_TAMANHO_CHAVE_CFESAT))

    # todos os números inteiros em <partes> devem ser pares
    for i, n in enumerate(partes, 1):
        if n <= 0 or n % 2 != 0:
            raise ValueError('Configuracoes do extrato do CF-e-SAT, Code128 em '
                    'partes e invalido: especifique apenas numeros inteiros e '
                    'pares, cuja soma seja a igual {tamamho_esperado!r}: '
                    'quebrar_partes={quebrar_partes!r} (secao={secao!r}, '
                    'arquivo={arquivo!r})'.format(
                            arquivo=arquivo,
                            secao=SECAO_CODE128,
                            quebrar_partes=quebrar_partes,
                            tamanho_esperado=_TAMANHO_CHAVE_CFESAT))

    return partes


def _garantir_diretorio(arquivo):
    caminho, _ = os.path.split(arquivo)
    if not os.path.isdir(caminho):
        logger.warning('criando diretorio de configuracoes para: %r', arquivo)
        os.makedirs(caminho)
