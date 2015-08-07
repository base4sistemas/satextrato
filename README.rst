
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

Para comunicar-se com equipamentos SAT veja o `Projeto SATCFe`_.

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


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

    # abre o arquivo do CF-e e emite o extrato
    with open(r'C:\CFe545090.xml', 'r') as fp:
        extrato = ExtratoCFeVenda(fp, impressora)
        extrato.imprimir()


Extratos do CF-e de Cancelamento
--------------------------------

Para emitir um extrato do CF-e de cancelamento, além do do CF-e de cancelamento,
você também irá precisar do do CF-e de venda que fora cancelado. Seguindo a
mesma linha do exemplo anterior:

.. sourcecode:: python

    with open('CFe_1.xml', 'r') as fvenda, open('CFeCanc_1.xml', 'r') as fcanc:
        extrato = ExtratoCFeCancelamento(fvenda, fcanc, impressora)
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


.. _`CF-e-SAT`: http://www.fazenda.sp.gov.br/sat/
.. _`SAT-CF-e`: http://www.fazenda.sp.gov.br/sat/
.. _`PyESCPOS`: https://github.com/base4sistemas/pyescpos
.. _`Projeto SATCFe`: https://github.com/base4sistemas/satcfe
.. _`XML`: http://www.w3.org/XML/
