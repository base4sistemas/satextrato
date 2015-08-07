# -*- coding: utf-8 -*-
#
# satextrato/tests/test_satextrato.py
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

import io
import sys

import pytest

from satextrato.venda import ExtratoCFeVenda
from satextrato.cancelamento import ExtratoCFeCancelamento


def test_extrato_venda(
        xml_venda,
        escpos_impl,
        escpos_interface):
    stream = io.StringIO(xml_venda)
    impl = escpos_impl(escpos_interface)
    extrato = ExtratoCFeVenda(stream, impl)
    extrato.imprimir()


def test_extrato_venda_resumido(
        xml_venda,
        escpos_impl,
        escpos_interface):
    stream = io.StringIO(xml_venda)
    impl = escpos_impl(escpos_interface)
    extrato = ExtratoCFeVenda(stream, impl, resumido=True)
    extrato.imprimir()


def test_extrato_cancelamento(
        xml_venda,
        xml_cancelamento,
        escpos_impl,
        escpos_interface):
    stream_venda = io.StringIO(xml_venda)
    stream_canc = io.StringIO(xml_cancelamento)
    impl = escpos_impl(escpos_interface)
    extrato = ExtratoCFeCancelamento(stream_venda, stream_canc, impl)
    extrato.imprimir()
