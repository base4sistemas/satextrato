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

from collections import namedtuple
from contextlib import contextmanager

try:
    # http://python-future.org/compatible_idioms.html#configparser
    # Python 2 and 3 (after ``pip install configparser``)
    from configparser import ConfigParser
except ImportError:
    # fallback to Python 2 SafeConfigParser module
    from ConfigParser import SafeConfigParser as ConfigParser

import six

from decouple import config as getenv

from unidecode import unidecode


SATEXTRATO_CONFIG_DIR = 'SATEXTRATO_CONFIG_DIR'
"""
Variável de ambiente que determina o caminho onde deve ser encontrado ou
gravado o arquivo de configurações. O padrão é ``~/.satextrato/``.
"""

SATEXTRATO_CONFIG_FILENAME = 'SATEXTRATO_CONFIG_FILENAME'
"""
Variável de ambiente que determina o nome do arquivo de configurações.
O padrão é :attr:`DEFAULT_FILENAME`.
"""

SATEXTRATO_UNIDECODE_VALUES_ON_PY2 = 'SATEXTRATO_UNIDECODE_VALUES_ON_PY2'
"""
Variável de ambiente que determina se os valores das configurações deverão
ser transliterados (via `Unidecode <https://pypi.org/project/Unidecode/>`_)
quando estiver executando sob Python 2. O padrão é ``True``.

O valor desta variável deverá ser ``y``, ``yes``, ``t``, ``true``, ``on``
ou ``1`` para ser considerado verdadeiro ``True`` e só terá efeito quando
estiver executando sob Python 2.
"""

SATEXTRATO_SECAO_CUPOM = 'SATEXTRATO_SECAO_CUPOM'
"""
Variável de ambiente que determina o nome da seção que contém as configurações
do cupom. Veja :class:`Cupom`. O padrão é :attr:`DEFAULT_SECAO_CUPOM`.
"""

SATEXTRATO_SECAO_RODAPE = 'SATEXTRATO_SECAO_RODAPE'
"""
Variável de ambiente que determina o nome da seção que contém as configurações
do rodapé. Veja :class:`Rodape`. O padrão é :attr:`DEFAULT_SECAO_RODAPE`.
"""

SATEXTRATO_SECAO_CODE128 = 'SATEXTRATO_SECAO_CODE128'
"""
Variável de ambiente que determina o nome da seção que contém as configurações
do Code128. Veja :class:`Code128`. O padrão é :attr:`DEFAULT_SECAO_CODE128`.
"""

SATEXTRATO_SECAO_QRCODE = 'SATEXTRATO_SECAO_QRCODE'
"""
Variável de ambiente que determina o nome da seção que contém as configurações
do QRCode. Veja :class:`QRCode`. O padrão é :attr:`DEFAULT_SECAO_QRCODE`.
"""

DEFAULT_FILENAME = 'satextrato.ini'
"""Nome padrão do arquivo de configurações."""

DEFAULT_SECAO_CUPOM = 'cupom'
"""Nome padrão da seção de configurações do cupom."""

DEFAULT_SECAO_RODAPE = 'rodape'
"""Nome padrão da seção de configurações do rodapé."""

DEFAULT_SECAO_CODE128 = 'code128'
"""Nome padrão da seção de configurações do Code128."""

DEFAULT_SECAO_QRCODE = 'qrcode'
"""Nome padrão da seção de configurações do QRCode."""


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
        'pular_linha_entre_partes',  # bool
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


@contextmanager
def fopen(filename_or_file_pointer, *args, **kwargs):
    from past.builtins import basestring
    if isinstance(filename_or_file_pointer, basestring):
        if six.PY2:
            import codecs
            with codecs.open(filename_or_file_pointer, *args, **kwargs) as fp:
                yield fp
        else:
            with io.open(filename_or_file_pointer, *args, **kwargs) as fp:
                yield fp
    else:
        yield filename_or_file_pointer


def carregar(
        arquivo=None,
        secao_cupom=None,
        secao_rodape=None,
        secao_code128=None,
        secao_qrcode=None,
        encoding='utf-8'
        ):
    """
    Carrega as configurações do extrato do CF-e-SAT.

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
    from past.builtins import basestring

    arquivo = arquivo or _default_config_filename()

    if isinstance(arquivo, basestring):
        # se `arquivo` for uma string (nome de arquivo) e esse arquivo
        # ainda não existir, cria o arquivo com as configurações padrão
        if not os.path.isfile(arquivo):
            conf = padrao()
            salvar(
                    conf,
                    arquivo=arquivo,
                    secao_cupom=secao_cupom,
                    secao_rodape=secao_rodape,
                    secao_code128=secao_code128,
                    secao_qrcode=secao_qrcode,
                    encoding=encoding
                )
            return conf

    # neste ponto, `arquivo` existe (se for uma string contendo um nome
    # de arquivo) ou é um file-like de onde as configurações devem ser
    # carregadas
    parser = ConfigParser()

    with fopen(arquivo, 'r', encoding=encoding) as f:
        if hasattr(parser, 'read_file'):
            parser.read_file(f)
        else:
            # fallback to Python 2 ConfigParser.readfp() (deprecated)
            parser.readfp(f)

    secao_cupom = secao_cupom or getenv(
            SATEXTRATO_SECAO_CUPOM,
            default=DEFAULT_SECAO_CUPOM
        )

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

    secao_rodape = secao_rodape or getenv(
            SATEXTRATO_SECAO_RODAPE,
            default=DEFAULT_SECAO_RODAPE
        )

    rodape = Rodape(
            esquerda=parser.get(secao_rodape, 'esquerda'),
            direita=parser.get(secao_rodape, 'direita')
        )

    secao_code128 = secao_code128 or getenv(
            SATEXTRATO_SECAO_CODE128,
            default=DEFAULT_SECAO_CODE128
        )

    code128 = Code128(
            ignorar=parser.getboolean(secao_code128, 'ignorar'),
            altura=parser.getint(secao_code128, 'altura'),
            quebrar=parser.getboolean(secao_code128, 'quebrar'),
            quebrar_partes=parser.get(secao_code128, 'quebrar_partes'),
            truncar=parser.getboolean(secao_code128, 'truncar'),
            truncar_tamanho=parser.getint(secao_code128, 'truncar_tamanho'),
            pular_linha_entre_partes=parser.getboolean(
                    secao_code128,
                    'pular_linha_entre_partes'
                )
        )

    secao_qrcode = secao_qrcode or getenv(
            SATEXTRATO_SECAO_QRCODE,
            default=DEFAULT_SECAO_QRCODE
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

    partes = code128_quebrar_partes(code128.quebrar_partes)
    code128 = code128._replace(quebrar_partes=partes)

    if six.PY3:
        # converte o valor do nível de correção para byte
        qrcode = qrcode._replace(
                nivel_correcao=qrcode.nivel_correcao.encode('ascii')
            )

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
        secao_cupom=None,
        secao_rodape=None,
        secao_code128=None,
        secao_qrcode=None,
        encoding='utf-8'
        ):
    """
    Salva configurações do extrato do CF-e-SAT.

    :param conf: Instância de :attr:`Configuracoes` (``namedtuple``).

    :param str arquivo: Opcional. Um objeto *file-like* ou o caminho
        completo para o arquivo onde serão salvas as configurações.
        Se não informado, será salvo no caminho e arquivo definidos nas
        variáveis de ambiente ``SATEXTRATO_CONFIG_DIR`` e
        ``SATEXTRATO_CONFIG_FILENAME``.

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

    :param str encoding: Opcional. Se não for especificado, será
        usado ``utf-8`` quando o argumento ``arquivo`` for um nome de
        arquivo (uma string). Se ``arquivo`` for um objeto *file-like*
        este argumento será ignorado.

    """
    parser = ConfigParser()

    secao_cupom = secao_cupom or getenv(
            SATEXTRATO_SECAO_CUPOM,
            default=DEFAULT_SECAO_CUPOM
        )

    sec = _SectionHelper(secao_cupom, parser, conf.cupom)
    sec.setboolean('itens_modo_condensado')
    sec.setboolean('exibir_nome_consumidor')
    sec.setint('avancar_linhas')
    sec.setboolean('cortar_documento')
    sec.setboolean('cortar_parcialmente')
    sec.setint('cortar_avanco')

    secao_rodape = secao_rodape or getenv(
            SATEXTRATO_SECAO_RODAPE,
            default=DEFAULT_SECAO_RODAPE
        )

    sec = _SectionHelper(secao_rodape, parser, conf.rodape)
    sec.set('esquerda')
    sec.set('direita')

    secao_code128 = secao_code128 or getenv(
            SATEXTRATO_SECAO_CODE128,
            default=DEFAULT_SECAO_CODE128
        )

    # converte a partir de uma tupla de inteiros e valida
    partes = ', '.join(str(p) for p in conf.code128.quebrar_partes)
    code128_quebrar_partes(partes)

    sec = _SectionHelper(secao_code128, parser, conf.code128)
    sec.setboolean('ignorar')
    sec.setint('altura')
    sec.setboolean('quebrar')
    sec.setvalue('quebrar_partes', partes)
    sec.setboolean('truncar')
    sec.setint('truncar_tamanho')
    sec.setboolean('pular_linha_entre_partes')

    secao_qrcode = secao_qrcode or getenv(
            SATEXTRATO_SECAO_QRCODE,
            default=DEFAULT_SECAO_QRCODE
        )

    # espera-se que `nivel_correcao` seja um byte (str no Python 2)
    qr_level = conf.qrcode.nivel_correcao.decode(encoding)

    sec = _SectionHelper(secao_qrcode, parser, conf.qrcode)
    sec.setint('tamanho_modulo')
    sec.setvalue('nivel_correcao', qr_level)
    sec.set('nome_aplicativo')
    sec.set('mensagem')
    sec.setboolean('mensagem_modo_condensado')

    arquivo = arquivo or _default_config_filename()
    with fopen(arquivo, 'w', encoding=encoding) as f:
        parser.write(f)


def padrao():
    """
    Retorna um objeto :class:`~satextrato.config.Configuracoes` contendo as
    configurações padrão.

    :rtype: satextrato.config.Configuracoes

    """
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
            truncar_tamanho=_TAMANHO_CHAVE_CFESAT,
            pular_linha_entre_partes=False,
        )

    qrcode = QRCode(
            tamanho_modulo=barcode.QRCODE_MODULE_SIZE_4,
            nivel_correcao=barcode.QRCODE_ERROR_CORRECTION_L,
            nome_aplicativo='De Olho Na Nota',
            mensagem_modo_condensado=True,
            mensagem=(
                    'Consulte o QRCode pelo aplicativo De Olho Na Nota, '
                    'disponível na AppStore (Apple) e PlayStore (Android)'
                )
        )

    conf = Configuracoes(
            cupom=cupom,
            rodape=rodape,
            code128=code128,
            qrcode=qrcode
        )

    return conf


def code128_quebrar_partes(partes):
    """
    Obtém as partes em que o Code128 deverá ser quebrado.

    Os códigos de barras Code128 requerem que os dados possuam um
    comprimento par, para que os dados possam ser codificados nessa
    simbologia.

    Embora a chave do CF-e-SAT possua 44 digitos, nem todas as mídias
    acomodam a impressão completa de 44 dígitos na simbologia Code128,
    por isso, o Manual de Orientação do SAT permite que o código de
    barras da chave seja quebrado em duas ou mais partes, ficando, por
    exemplo, um Code128 com os primeiros 22 dígitos da chave do CF-e e
    outro Code128 logo abaixo com os 22 dígitos restantes.

    Essa quebra pode ser feita em 4 códigos de barras, mas eles não
    podem ser formados por 4 partes de 11 dígitos, devido à limitação da
    simbologia Code128 de codificar os dados em sequências pares.

    Para dar certo quebrar o Code128 em 4 partes, cada parte precisaria
    indicar comprimentos de ``10, 10, 10, 14``, somando 44 dígitos, ou
    indicar comprimentos de ``12, 12, 12, 8``, somando 44 dígitos.

    :param str partes: Uma string que especifica uma lista de números
        inteiros, pares, maiores que zero e separados por vírgulas,
        cuja soma deve ser igual a 44, que é o comprimento da chave do
        CF-e-SAT.

    :returns: Retorna uma tupla de números inteiros, extraídos da string
        informada no argumento.

    :rtype: tuple

    """
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

    # checa se a lista contém apenas números pares
    for i, n in enumerate(lista_partes, 1):
        if n <= 0 or n % 2 != 0:
            raise ValueError(
                (
                    'Configuracoes do extrato do CF-e-SAT, Code128, '
                    'elemento {!r} deve ser um número par; obtido {!r}'
                ).format(i, n)
            )

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

    return tuple(lista_partes)


class _SectionHelper(object):

    def __init__(self, section_name, parser, obj):
        self._unidecode_values = six.PY2 and getenv(
                SATEXTRATO_UNIDECODE_VALUES_ON_PY2,
                cast=bool,
                default=True
            )
        self._section_name = section_name
        self._parser = parser
        self._obj = obj

    def _set(self, option_name, value):
        if not self._parser.has_section(self._section_name):
            self._parser.add_section(self._section_name)
        value = unidecode(value) if self._unidecode_values else value
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
    path = getenv(SATEXTRATO_CONFIG_DIR, default=default_path)
    if not os.path.isdir(path):
        os.makedirs(path)
    return path


def _config_filename():
    return getenv(SATEXTRATO_CONFIG_FILENAME, default=DEFAULT_FILENAME)


def _default_config_filename():
    return os.path.join(_config_dir(), _config_filename())
