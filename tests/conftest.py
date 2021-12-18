# -*- coding: utf-8 -*-
#
# tests/conftest.py
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

import importlib
import os
import shutil

from builtins import str as text

import pytest

from escpos import constants as escpos_const
from escpos.conn import CONNECTION_TYPES


def pytest_addoption(parser):

    parser.addoption(
            '--escpos-impl',
            action='store',
            metavar='CLASSNAME',
            default='escpos.impl.epson.GenericESCPOS',
            help='Implementacao ESC/POS a ser instanciada'
        )

    parser.addoption(
            '--escpos-if',
            action='store',
            default='dummy',
            choices=[alias for alias, type_info in CONNECTION_TYPES],
            help='Interface com o dispositivo'
        )

    parser.addoption(
            '--escpos-if-settings',
            action='store',
            metavar='SETTINGS',
            default='',
            help='String de conexão (conforme a interface com o dispositivo)'
        )

    parser.addoption(
            '--escpos-encoding',
            action='store',
            metavar='ENCODING',
            default=escpos_const.DEFAULT_ENCODING,
            help='Encoding antes de enviar dados ao dispositivo'
        )

    parser.addoption(
            '--escpos-encoding-errors',
            action='store',
            metavar='ERRORS',
            default=escpos_const.DEFAULT_ENCODING_ERRORS,
            help='Como lidar com erros de codificação de caracteres'
        )

    parser.addoption(
            '--config-file',
            action='store',
            metavar='FILENAME',
            default='',
            help=(
                    'Caminho completo para o arquivo de configurações. '
                    'Se não for especificado, serão usadas as '
                    'configurações padrão'
                )
        )


class InterfaceFactory(object):

    def __init__(self, request):
        self._request = request

    def get_connection_interface(self):
        interface = self._request.config.getoption('--escpos-if')
        settings = self._request.config.getoption('--escpos-if-settings')
        method = 'create_{}_connection'.format(interface)
        return getattr(self, method)(settings)

    def create_bluetooth_connection(self, settings):
        from escpos import BluetoothConnection
        conn = BluetoothConnection.create(settings)
        return conn

    def create_dummy_connection(self, settings):
        from escpos import DummyConnection
        conn = DummyConnection.create(settings)
        return conn

    def create_file_connection(self, settings):
        from escpos import FileConnection
        conn = FileConnection.create(settings)
        return conn

    def create_network_connection(self, settings):
        from escpos import NetworkConnection
        conn = NetworkConnection.create(settings)
        return conn

    def create_serial_connection(self, settings):
        from escpos import SerialConnection
        conn = SerialConnection.create(settings)
        return conn

    def create_usb_connection(self, settings):
        from escpos import USBConnection
        conn = USBConnection.create(settings)
        return conn


@pytest.fixture(scope='function')
def datadir(tmpdir, request):
    path, _ = os.path.split(request.module.__file__)
    dirname = os.path.join(path, 'data')
    shutil.copytree(dirname, text(tmpdir.join('data')))
    return tmpdir


@pytest.fixture(scope='session')
def configuracao(request):
    from satextrato import config
    arquivo = request.config.getoption('--config-file')
    if not arquivo:
        conf = config.padrao()
    else:
        conf = config.carregar(arquivo=arquivo)
    return conf


@pytest.fixture(scope='session')
def escpos_impl(request):
    names = request.config.getoption('--escpos-impl').split('.')
    _module = importlib.import_module('.'.join(names[:-1]))
    printer = getattr(_module, names[-1])

    encoding = request.config.getoption('--escpos-encoding')
    encoding_errors = request.config.getoption('--escpos-encoding-errors')

    factory = InterfaceFactory(request)
    device = factory.get_connection_interface()

    impl = printer(
            device,
            encoding=encoding,
            encoding_errors=encoding_errors
        )
    return impl
