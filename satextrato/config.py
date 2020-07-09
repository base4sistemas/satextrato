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
from __future__ import absolute_import
from __future__ import unicode_literals

import io
import os
import sys

from collections import namedtuple

try:
    # http://python-future.org/compatible_idioms.html#configparser
    # Python 2 and 3 (after ``pip install configparser``)
    from configparser import ConfigParser
except ImportError:
    # fallback to Python 2 SafeConfigParser module
    from ConfigParser import SafeConfigParser as ConfigParser


SECAO_CUPOM = 'cupom'
SECAO_RODAPE = 'rodape'
SECAO_CODE128 = 'code128'
SECAO_QRCODE = 'qrcode'

_TAMANHO_CHAVE_CFESAT = 44


Cupom = namedtuple('Cupom', [
        'itens_modo_condensado',  # bool
        'exibir_nome_consumidor',  # bool
        'avancar_linhas',  # int
        'cortar_documento',  # bool
        'cortar_parcialmente',  # bool
        'cortar_avanco',  # int
    ])

Rodape = namedtuple('Rodape', [
        'esquerda',  # str
        'direita',  # str
    ])

Code128 = namedtuple('Code128', [
        'ignorar',  # bool
        'altura',  # int
        'quebrar',  # bool
        'quebrar_partes',  # tuple(int, ...)
        'truncar',  # bool
        'truncar_tamanho',  # int
    ])

QRCode = namedtuple('QRCode', [
        'tamanho_modulo',  # int
        'nivel_correcao',  # str
        'nome_aplicativo',  # str
        'mensagem_modo_condensado',  # bool
        'mensagem',  # str
    ])

Configuracoes = namedtuple('Configuracoes', [
        'cupom',  # Cupom
        'rodape',  # Rodape
        'code128',  # Code128
        'qrcode',  # QRCode
    ])


def carregar(
        arquivo=None,
        secao_cupom=SECAO_CUPOM,
        secao_rodape=SECAO_RODAPE,
        secao_code128=SECAO_CODE128,
        secao_qrcode=SECAO_QRCODE
        ):
    """Carrega as configurações do extrato do CF-e-SAT.

    :param str arquivo: Opcional. Caminho completo para o arquivo de
        onde serão carregadas as configurações. O arquivo será interpretado
        pela classe ``ConfigParser`` da biblioteca padrão.
        Se arquivo não existir, será criado um com os valores padrão.
        Se um nome de arquivo não for informado, as configurações serão
        carregadas do caminho e arquivo definidos nas variáveis de ambiente
        ``SATEXTRATO_CONFIG_DIR`` e ``SATEXTRATO_CONFIG_FILENAME``.

    :param str secao_cupom: Opcional. Nome da seção onde ficam as
        propriedades associadas ao cupom do extrato. Veja :attr:`Cupom`.

    :param str secao_rodape: Opcional. Nome da seção onde ficam as
        propriedades associadas ao rodapé do extrato. Veja :attr:`Rodape`.

    :param str secao_code128: Opcional. Nome da seção onde ficam as
        propriedades associadas ao código de barras padrão Code-128 que é
        impresso no extrato. Veja :attr:`Code128`.

    :param str secao_qrcode: Opcional. Nome da seção onde ficam as
        propriedades associadas ao QRCode que é impresso no extrato.
        Veja :attr:`QRCode`.

    :rtype: satextrato.config.Configuracoes

    """
    arquivo = arquivo or os.path.join(_config_dir(), _config_filename())
    if not os.path.isfile(arquivo):
        salvar(
                padrao(),
                arquivo=arquivo,
                secao_cupom=secao_cupom,
                secao_rodape=secao_rodape,
                secao_code128=secao_code128,
                secao_qrcode=secao_qrcode
            )

    parser = ConfigParser()

    with io.open(arquivo, 'r', encoding='utf-8') as f:
        if hasattr(parser, 'read_file'):
            parser.read_file(f)
        else:
            # fallback to Python 2 ConfigParser.readfp() (deprecated)
            parser.readfp(f)

    cupom = Cupom(
            itens_modo_condensado=parser.getboolean(
                    secao_cupom,
                    'itens_modo_condensado'
                ),
            exibir_nome_consumidor=parser.getboolean(
                    secao_cupom,
                    'itens_modo_condensado'
                ),
            avancar_linhas=parser.getint(secao_cupom, 'avancar_linhas'),
            cortar_documento=parser.getboolean(
                    secao_cupom,
                    'itens_modo_condensado'
                ),
            cortar_parcialmente=parser.getboolean(
                    secao_cupom,
                    'itens_modo_condensado'
                ),
            cortar_avanco=parser.getint(secao_cupom, 'cortar_avanco')
        )

    rodape = Rodape(
            esquerda=parser.get(secao_rodape, 'esquerda'),
            direita=parser.get(secao_rodape, 'direita')
        )

    code128 = Code128(
            ignorar=parser.getboolean(secao_code128, 'ignorar'),
            altura=parser.getint(secao_code128, 'altura'),
            quebrar=parser.getboolean(secao_code128, 'quebrar'),
            quebrar_partes=parser.get(secao_code128, 'quebrar_partes'),
            truncar=parser.getboolean(secao_code128, 'truncar'),
            truncar_tamanho=parser.getint(secao_code128, 'truncar_tamanho')
        )

    qrcode = QRCode(
        tamanho_modulo=parser.getint(secao_qrcode, 'tamanho_modulo'),
        nivel_correcao=parser.get(secao_qrcode, 'nivel_correcao'),
        nome_aplicativo=parser.get(secao_qrcode, 'nome_aplicativo'),
        mensagem=parser.get(secao_qrcode, 'mensagem'),
        mensagem_modo_condensado=parser.getboolean(
                secao_qrcode,
                'mensagem_modo_condensado'
            )
        )

    if sys.version_info >= (3,):
        # Python 3, converte o valor do nível de correção para byte
        qrcode = qrcode._replace(
                nivel_correcao=qrcode.nivel_correcao.encode('ascii')
            )

    partes = _validar_code128_quebrar_partes(code128.quebrar_partes)
    code128 = code128._replace(quebrar_partes=partes)

    conf = Configuracoes(
            cupom=cupom,
            rodape=rodape,
            code128=code128,
            qrcode=qrcode
        )

    return conf


def salvar(
        conf,
        arquivo=None,
        secao_cupom=SECAO_CUPOM,
        secao_rodape=SECAO_RODAPE,
        secao_code128=SECAO_CODE128,
        secao_qrcode=SECAO_QRCODE
        ):
    """Salva configurações do extrato do CF-e-SAT.

    :param conf: Instância de :attr:`Configuracoes` (``namedtuple``).

    :param str arquivo: Opcional. Caminho completo para o arquivo onde
        serão salvas as configurações. Se não informado, será salvo no
        caminho e arquivo definidos nas variáveis de ambiente
        ``SATEXTRATO_CONFIG_DIR`` e ``SATEXTRATO_CONFIG_FILENAME``.

    :param str secao_cupom: Opcional. Nome da seção onde ficam as
        propriedades associadas ao cupom do extrato. Veja :attr:`Cupom`.

    :param str secao_rodape: Opcional. Nome da seção onde ficam as
        propriedades associadas ao rodapé do extrato. Veja :attr:`Rodape`.

    :param str secao_code128: Opcional. Nome da seção onde ficam as
        propriedades associadas ao código de barras padrão Code-128 que é
        impresso no extrato. Veja :attr:`Code128`.

    :param str secao_qrcode: Opcional. Nome da seção onde ficam as
        propriedades associadas ao QRCode que é impresso no extrato.
        Veja :attr:`QRCode`.

    """
    parser = ConfigParser()

    sec = _SectionHelper(secao_cupom, parser, conf.cupom)
    sec.setboolean('itens_modo_condensado')
    sec.setboolean('exibir_nome_consumidor')
    sec.setint('avancar_linhas')
    sec.setboolean('cortar_documento')
    sec.setboolean('cortar_parcialmente')
    set.setint('cortar_avanco')

    sec = _SectionHelper(secao_rodape, parser, conf.rodape)
    sec.set('esquerda')
    sec.set('direita')

    # converte a partir de uma tupla de inteiros
    partes = ','.join(str(p) for p in conf.code128.quebrar_partes)

    sec = _SectionHelper(secao_code128, parser, conf.code128)
    sec.setboolean('ignorar')
    sec.setint('altura')
    sec.setboolean('quebrar')
    sec.setvalue('quebrar_partes', partes)
    sec.setboolean('truncar')
    sec.setint('truncar_tamanho')

    qr_level = conf.qrcode.nivel_correcao  # no Python 3 é do tipo byte
    if sys.version_info >= (3,):
        # converte de byte para str no Python 3
        qr_level = qr_level.decode('utf-8')

    sec = _SectionHelper(secao_qrcode, parser, conf.qrcode)
    sec.setint('tamanho_modulo')
    sec.setvalue('nivel_correcao', qr_level)
    sec.set('nome_aplicativo')
    sec.set('mensagem')
    sec.setboolean('mensagem_modo_condensado')

    arquivo = arquivo or os.path.join(_config_dir(), _config_filename())
    with io.open(arquivo, 'w', encoding='utf-8') as f:
        parser.write(f)


class _SectionHelper(object):

    def __init__(self, section_name, parser, obj):
        self._section_name = section_name
        self._parser = parser
        self._obj = obj

    def _set(self, option_name, value):
        return self._parser.set(self._section_name, option_name, value)

    def set(self, option_name):
        return self._set(option_name, getattr(self._obj, option_name))

    def setboolean(self, option_name):
        value = 'yes' if getattr(self._obj, option_name) else 'no'
        return self._set(option_name, value)

    def setint(self, option_name):
        value = str(getattr(self._obj, option_name))
        return self._set(option_name, value)

    def setvalue(self, option_name, value):
        return self._parser.set(self._section_name, option_name, value)


def _config_dir():
    default_path = os.path.join(os.path.expanduser('~'), '.satextrato')
    path = os.getenv('SATEXTRATO_CONFIG_DIR', default_path)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _config_filename():
    return os.getenv('SATEXTRATO_CONFIG_FILENAME', 'satextrato.ini')


def padrao():
    from escpos import barcode

    cupom = Cupom(
            itens_modo_condensado=True,
            exibir_nome_consumidor=False,
            avancar_linhas=7,
            cortar_documento=True,
            cortar_parcialmente=True,
            cortar_avanco=0
        )

    rodape = Rodape(
            esquerda='Extrato CF-e-SAT',
            direita='http://git.io/vJRRk'
        )

    code128 = Code128(
            ignorar=False,
            altura=56,
            quebrar=True,
            quebrar_partes=(22, 22),
            truncar=False,
            truncar_tamanho=44
        )

    qrcode = QRCode(
            tamanho_modulo=barcode.QRCODE_MODULE_SIZE_4,
            nivel_correcao=barcode.QRCODE_ERROR_CORRECTION_L,
            nome_aplicativo='De Olho Na Nota',
            mensagem_modo_condensado=True,
            mensagem=(
                    u'Consulte o QRCode pelo aplicativo De Olho Na Nota, '
                    u'disponível na AppStore (Apple) e PlayStore (Android)'
                )
        )

    conf = Configuracoes(
            cupom=cupom,
            rodape=rodape,
            code128=code128,
            qrcode=qrcode
        )

    return conf


def _validar_code128_quebrar_partes(partes):
    # <partes> str - uma lista de inteiros separados por vírgulas
    try:
        lista_partes = [int(p) for p in partes.split(',')]
    except ValueError:
        raise ValueError(
                (
                    'Configuracoes do extrato do CF-e-SAT, Code128 em '
                    'partes deve especificar as partes em valores inteiros, '
                    'todos numeros pares e separados por virgulas; '
                    'obtido: {!r}'
                ).format(partes)
            )
    else:
        calculado = sum(lista_partes)
        if calculado != _TAMANHO_CHAVE_CFESAT:
            raise ValueError(
                (
                    'Configuracoes do extrato do CF-e-SAT, Code128 em '
                    'partes deve especificar as partes em valores inteiros, '
                    'todos numeros pares e separados por virgulas; a soma '
                    'das partes deve ser igual ao tamanho da chave do '
                    'CF-e-SAT; obtido: {!r} (esperado: {!r})'
                ).format(
                    calculado,
                    _TAMANHO_CHAVE_CFESAT
                )
            )

    # todos os números inteiros em <partes> devem ser pares
    for i, n in enumerate(lista_partes, 1):
        if n <= 0 or n % 2 != 0:
            raise ValueError(
                (
                    'Configuracoes do extrato do CF-e-SAT, Code128, '
                    'elemento {!r} deve ser um número par; obtido {!r}'
                ).format(i, n)
            )

    return tuple(lista_partes)
