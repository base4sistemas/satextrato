# -*- coding: utf-8 -*-
#
# tests/test_config.py
#
# Copyright 2021 Base4 Sistemas
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

import pytest

from satextrato.config import code128_quebrar_partes
from satextrato.config import fopen


def test_code128_quebrar_partes_listas_ok():
    """
    Testa listas válidas, contendo elementos inteiros, pares, maiores que
    zero, cuja soma deve ser igual a 44, que é o número de dígitos que
    possue a chave de um CF-e-SAT.
    """
    assert code128_quebrar_partes('44') == (44,)
    assert code128_quebrar_partes('22, 22') == (22, 22)
    assert code128_quebrar_partes('10, 10, 10, 10, 4') == (10, 10, 10, 10, 4)

    # caso extremo, de quebra de 2 em 2 dígitos
    assert code128_quebrar_partes(', '.join('2' * 22)) == tuple([2] * 22)


def test_code128_quebrar_partes_lista_vazia():
    """Uma lista vazia deve levantar uma exceção ``ValueError``."""
    with pytest.raises(ValueError):
        code128_quebrar_partes('')


def test_code128_quebrar_partes_lista_com_elementos_nao_inteiros():
    """
    Deve ser lançado um ``ValueError`` se a lista possuir algum
    elemento que não possa ser convertido para um inteiro.
    """
    with pytest.raises(ValueError):
        code128_quebrar_partes('a')

    with pytest.raises(ValueError):
        code128_quebrar_partes('22, 22, a')


def test_code128_quebrar_partes_lista_nao_soma_44():
    """
    A soma da lista deve ser igual a 44, que é o número de dígitos que
    possue a chave de um CF-e-SAT.
    """
    with pytest.raises(ValueError):
        code128_quebrar_partes('40')

    with pytest.raises(ValueError):
        code128_quebrar_partes('2, 2, 2')

    with pytest.raises(ValueError):
        code128_quebrar_partes('2, 40')


def test_fopen(tmp_path):
    """
    O *contextmanager* ``fopen`` deve retornar um *file-like* tanto para
    um nome de arquivo quanto para um *file-like*.
    """
    file_like = io.StringIO()
    with fopen(file_like) as f:
        assert f is file_like

    filename = str(tmp_path / 'test.txt')
    with fopen(filename, 'w', encoding='utf-8') as f:
        assert f != filename
