
.. image:: https://img.shields.io/pypi/v/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Latest version

.. image:: https://img.shields.io/pypi/pyversions/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Supported Python versions

.. image:: https://img.shields.io/pypi/status/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: Development status

.. image:: https://img.shields.io/pypi/l/satextrato.svg
    :target: https://pypi.python.org/pypi/satextrato/
    :alt: License

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge


Projeto SATExtrato
==================

    This project prints receipts for fiscal electronic documents called "CF-e".
    Those documents are created through a system called `SAT-CF-e`_ which is a
    system for autorization and transmission of fiscal documents, developed by
    Finance Secretary of state of São Paulo, Brazil. The entire project,
    including variables, methods and class names, as well as documentation,
    are written in brazilian portuguese.


Este projeto realiza a impressão dos **Extratos do CF-e-SAT** em impressoras
ESC/POS |reg| e são normalmente impressos em mini-impressoras de cupons,
térmicas ou de impacto, mas não limitado à elas. As impressoras, marcas e
modelos suportados dependem dos modelos suportados no projeto `PyESCPOS`_.

Para autorizar e transmitir documentos eletrônicos através da tecnologia
`SAT-CF-e`_ é preciso comunicar-se com os equipamentos SAT. Para isso, dê uma
olhada no `Projeto SATCFe`_. **Este projeto lida apenas com a impressão do
extrato de documentos CF-e.**


Exemplos de Uso
===============

Há dois tipos de documentos CF-e-SAT: documentos de **venda** e documentos
de **cancelamento** de uma venda anteriormente autorizada.


Extratos do CF-e de Venda
-------------------------

Para emitir um extrato de um CF-e-SAT de venda, você irá precisar do arquivo
`XML`_ do CF-e-SAT de venda, que é o próprio documento fiscal, e de uma
impressora que seja suportada pelo projeto `PyESCPOS`_:

.. sourcecode:: python

    from escpos import SerialConnection
    from escpos.impl.epson import TMT20
    from satextrato import ExtratoCFeVenda

    conn = SerialConnection.create('COM1:9600,8,1,N')
    impressora = TMT20(conn)
    impressora.init()

    with open(r'C:\CFe351702.xml', 'r') as fp:
        extrato = ExtratoCFeVenda(fp, impressora)
        extrato.imprimir()

Veja as implementações ESC/POS |reg| disponíveis no projeto `PyESCPOS`_


Extratos do CF-e de Cancelamento
--------------------------------

Para emitir um extrato de um CF-e-SAT de cancelamento você irá precisar de dois
arquivos `XML`_: o documento de venda e o documento de cancelamento. Seguindo a
mesma linha do exemplo anterior:

.. sourcecode:: python

    cfe_venda = r'C:\CFe_venda.xml'
    cfe_canc = r'C:\CFe_cancelamento.xml'
    with open(cfe_venda, 'r') as fvenda, open(cfe_canc, 'r') as fcanc:
        extrato = ExtratoCFeCancelamento(fvenda, fcanc, impressora)
        extrato.imprimir()


Wiki do Projeto
===============

Visite o `Wiki`_ do projeto para saber como configurar as várias partes do
extrato ou então para encontrar outros exemplos e mais informações.


Você é Bem-vindo para Ajudar
============================

Primeiro, configure seu ambiente de desenvolvimento e execute os testes:

.. sourcecode:: shell

    $ git clone git@github.com:base4sistemas/satextrato.git
    $ cd satextrato
    $ python -m venv .env
    $ source .env/bin/activate
    (.env) $ pip install --upgrade pip
    (.env) $ pip install -r requirements/dev.txt
    (.env) $ tox


Mais Sobre Testes
-----------------

Simplesmente execute ``pytest`` ou então ``tox`` para executar os testes
contra várias versões de Python. Por padrão, as impressões dos extratos de
testes serão enviadas para uma interface que realmente não faz nada
(*dummy printer*).

Você pode mudar isso, realizando testes contra uma impressora ESC/POS real
conectada ao seu computador, usando as opções customizadas.
Use ``pytest --help`` e procure pela seção *custom options*. Por exemplo,
para imprimir em uma Bematech MP-2800 TH conectada à porta serial ``COM1``:

.. sourcecode:: shell-session

    pytest \
        --escpos-impl=escpos.impl.bematech.MP2800TH \
        --escpos-if=serial \
        --escpos-if-settings=COM1:9600,8,1,N,RTSCTS \
        --config-file=/home/user/satextrato.ini

Ou via ``tox``, em uma impressora com interface ETH (*ethernet*):

.. sourcecode:: shell-session

    tox -e py39 -- \
        --escpos-impl=escpos.impl.controlid.PrintIdTouch \
        --escpos-if=network \
        --escpos-if-settings=192.168.1.200:9100 \
        --config-file=/home/user/satextrato.ini

Note que executar os testes de ambientes relacionados à interfaces de conexão
específicos (eg. ``py39-serial``), só faz sentido se você especificar também
as configurações da interface via ``--escpos-if-*`` que irá configurar a
interface onde provavelmente terá uma impressora real conectada ou, no mínimo,
um emulador ou um `null modem <https://en.wikipedia.org/wiki/Null_modem#Virtual_null_modem>`_.


Isenção de Responsabilidade
===========================

Por favor, **leia atentamente**:

    A **Base4 Sistemas** e os desenvolvedores envolvidos neste projeto, NÃO
    ASSUMEM NEM TEM QUALQUER RESPONSABILIDADE sobre os "Extratos do CF-e-SAT"
    gerados por esta biblioteca de código, seja diretamente ou através de uma
    APLICAÇÃO USUÁRIA. **Use por sua própria conta e risco.**

..
    Sphinx Documentation: Substitutions at
    http://sphinx-doc.org/rest.html#substitutions
    Codes copied from reStructuredText Standard Definition Files at
    http://docutils.sourceforge.net/docutils/parsers/rst/include/isonum.txt


.. |reg|  unicode:: U+00AE .. REGISTERED SIGN
    :ltrim:


.. _`SAT-CF-e`: https://portal.fazenda.sp.gov.br/servicos/sat/Paginas/Sobre.aspx
.. _`PyESCPOS`: https://github.com/base4sistemas/pyescpos
.. _`Projeto SATCFe`: https://github.com/base4sistemas/satcfe
.. _`XML`: http://www.w3.org/XML/
.. _`Wiki`: https://github.com/base4sistemas/satextrato/wiki
