
Projeto Extratos SAT-CF-e
=========================

.. image:: https://pypip.in/status/satextrato/badge.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Development status

.. image:: https://pypip.in/py_versions/satextrato/badge.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Supported Python versions

.. image:: https://pypip.in/license/satextrato/badge.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: License

.. image:: https://pypip.in/version/satextrato/badge.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Latest version

-------

    This project is about printing receipts from eletronic fiscal documents
    called **CF-e-SAT** which is a system for autorization and transmission of
    fiscal documents, developed by Finance Secretary of state of São Paulo,
    Brazil. This entire project, variables, methods and class names, as well as
    documentation, are written in brazilian portuguese.
    Refer to `this link <www.fazenda.sp.gov.br/sat/>`_ for more information.

Emissão de extratos do `CF-e-SAT <http://www.fazenda.sp.gov.br/sat/>`_
diretamente a partir dos documentos eletrônicos que representam o CF-e de
venda e/ou de cancelamento.

Esta implementação é baseada na emissão do extrato para mini-impressoras,
normalmente térmicas (mas não limitado à elas), através da abstração
`PyESCPOS <https://github.com/base4sistemas/pyescpos>`_ para o sistema de
comandos de impressão ESC/POS |reg| e derivações.


Extratos do CF-e de Venda
-------------------------

Para emissão do extrato para um CF-e de venda, você irá precisar do XML do CF-e,
e uma mini-impressora ESC/POS |reg| (veja as implementações disponíveis no
projeto `PyESCPOS <https://github.com/base4sistemas/pyescpos>`_):

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


..
    Sphinx Documentation: Substitutions at
    http://sphinx-doc.org/rest.html#substitutions
    Codes copied from reStructuredText Standard Definition Files at
    http://docutils.sourceforge.net/docutils/parsers/rst/include/isonum.txt

.. |reg|  unicode:: U+00AE .. REGISTERED SIGN
    :ltrim:
