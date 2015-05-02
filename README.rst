
Projeto Extratos CF-e-SAT
=========================

.. image:: https://img.shields.io/badge/status-planning-red.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Development status

.. image:: https://img.shields.io/badge/python%20version-2.7-blue.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/l/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: License

.. image:: https://img.shields.io/pypi/v/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Latest version

-------

    This project is about printing receipts from eletronic fiscal documents
    related to `SAT-CF-e`_ which is a system for autorization and transmission
    of fiscal documents, developed by Finance Secretary of state of São Paulo,
    Brazil. This entire project, variables, methods and class names, as well as
    documentation, are written in brazilian portuguese.

    Refer to the `oficial web site <http://www.fazenda.sp.gov.br/sat/>`_ for
    more information (in brazilian portuguese only).

Emissão de extratos do `CF-e-SAT`_ diretamente a partir dos documentos
eletrônicos que representam o CF-e de venda e/ou de cancelamento, na forma
de arquivos em formato `XML`_.

Esta implementação é baseada na emissão dos extratos para mini-impressoras,
normalmente térmicas (mas não limitado à elas), através da abstração
`PyESCPOS`_ para o sistema de comandos de impressão ESC/POS |reg| e derivações.


Extratos do CF-e de Venda
-------------------------

Para emissão do extrato para um CF-e de venda, você irá precisar do XML do CF-e,
e uma mini-impressora ESC/POS |reg| (veja as implementações disponíveis no
projeto `PyESCPOS`_):

.. sourcecode:: python

    from escpos.serial import SerialSettings
    from escpos.impl.daruma import DR700
    from satextrato import ExtratoCFeVenda

    # mini-impressora Daruma (DR700) conectada à porta serial COM1
    conn = SerialSettings.as_from('COM1:9600,8,1,N').get_connection()
    impressora = DR700(conn)
    impressora.init()

    # carrega o conteúdo do XML do CF-e de venda
    with open(r'C:\CFe545090.xml', 'r') as f:
        xml = f.read()

    # emite o extrato
    extrato = ExtratoCFeVenda(xml, impressora)
    extrato.imprimir()


Extratos do CF-e de Cancelamento
--------------------------------

Para emitir um extrato do CF-e de cancelamento, além do XML do CF-e de
cancelamento, você também irá precisar do XML do CF-e de venda que foi
cancelado. Seguindo a mesma linha do exemplo anterior:

.. sourcecode:: python

    extrato = ExtratoCFeCancelamento(xml_canc, xml_venda, impressora)
    extrato.imprimir()


Executando Testes
-----------------

Para executar os testes de emissão dos extratos em mini-impressoras conectadas
à portas seriais, ou em impressoras USB a partir de virtualizadores de portas
seriais:

.. sourcecode:: shell

    $ python setup.py test -a \
            "--escpos-impl=escpos.impl.daruma.DR700 "\
            "--escpos-if=serial "\
            "--serial-port=/dev/ttyS7"

Glossário
=========

Alguns termos são confusos e parecem dizer mesma coisa quando, na verdade,
são coisas completamente diferentes. Este pequeno glossário pode ajudar a
desfazer certas confusões.

CF-e
    Cupom Fiscal eletrônico, um documento em formato XML que descreve uma
    transação de venda ao consumidor ou o cancelamento de uma venda anterior.

SAT-CF-e
    Diz respeito à tecnologia SAT-Fiscal e toda a infraestrutura física e
    lógica usada na transmissão de documentos fiscais (CF-e) de venda e/ou
    cancelamento.

CF-e-SAT
    Refere-se ao CF-e que transitou através do SAT-CF-e.

Outros dois termos muito parecidos, mas são coisas totalmente diferentes:

AC-SAT
    Refere-se à **Autoridade Certificadora** que gerencia (emite e revoga)
    certificados digitais de equipamentos SAT.

AC
    Refere-se ao **Aplicativo Comercial** (a.k.a. Automação Comercial).


..
    Sphinx Documentation: Substitutions at
    http://sphinx-doc.org/rest.html#substitutions
    Codes copied from reStructuredText Standard Definition Files at
    http://docutils.sourceforge.net/docutils/parsers/rst/include/isonum.txt


.. |reg|  unicode:: U+00AE .. REGISTERED SIGN
    :ltrim:


.. _`CF-e-SAT`: http://www.fazenda.sp.gov.br/sat/
.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
.. _`PyESCPOS`: https://github.com/base4sistemas/pyescpos
.. _`XML`: http://www.w3.org/XML/
