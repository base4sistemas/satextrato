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

import sys

import pytest

from satextrato.venda import ExtratoCFeVenda
from satextrato.cancelamento import ExtratoCFeCancelamento


def test_extrato_venda_simples(
        xml_venda,
        escpos_impl,
        escpos_interface):
    impl = escpos_impl(escpos_interface)
    extrato = ExtratoCFeVenda(xml_venda, impl)
    extrato.imprimir()


def test_extrato_cancelamento_simples(
        xml_cancelamento,
        xml_venda,
        escpos_impl,
        escpos_interface):
    impl = escpos_impl(escpos_interface)
    extrato = ExtratoCFeCancelamento(xml_cancelamento, xml_venda, impl)
    extrato.imprimir()
