# -*- coding: utf-8 -*-
#
# tests/test_satextrato.py
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

import io

from builtins import str as text

from satextrato.venda import ExtratoCFeVenda
from satextrato.cancelamento import ExtratoCFeCancelamento


def test_extrato_venda(
        configuracao,
        datadir,
        escpos_impl):
    cfe_venda = text(datadir.join('data', 'cfe_venda.xml'))
    with io.open(cfe_venda, 'r') as stream:
        extrato = ExtratoCFeVenda(stream, escpos_impl, config=configuracao)
        extrato.imprimir()


def test_extrato_venda_resumido(
        configuracao,
        datadir,
        escpos_impl):
    cfe_venda = text(datadir.join('data', 'cfe_venda.xml'))
    with io.open(cfe_venda, 'r') as stream:
        extrato = ExtratoCFeVenda(
                stream,
                escpos_impl,
                resumido=True,
                config=configuracao
            )
        extrato.imprimir()


def test_extrato_cancelamento(
        configuracao,
        datadir,
        escpos_impl):
    cfe_venda = text(datadir.join('data', 'cfe_venda.xml'))
    cfe_canc = text(datadir.join('data', 'cfe_cancelamento.xml'))
    with io.open(cfe_venda, 'r') as stream_venda, \
            io.open(cfe_canc, 'r') as stream_canc:
        extrato = ExtratoCFeCancelamento(
                stream_venda,
                stream_canc,
                escpos_impl,
                config=configuracao
            )
        extrato.imprimir()
