
Projeto Extratos CF-e-SAT
=========================

.. image:: https://img.shields.io/pypi/status/satextrato.svg
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

.. image:: https://badges.gitter.im/Join%20Chat.svg
   :alt: Join the chat at https://gitter.im/base4sistemas/satcfe
   :target: https://gitter.im/base4sistemas/satcfe?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge

-------

This project prints receipts for fiscal electronic documents called "CF-e".
Those documents are created through a system called `SAT-CF-e`_ which is a
system for autorization and transmission of fiscal documents, developed by
Finance Secretary of state of São Paulo, Brazil. The entire project, variables,
methods and class names, as well as documentation, are written in brazillian
portuguese.

-------

Este projeto realiza a impressão dos **Extratos do CF-e-SAT** em impressoras
ESC/POS |reg| e são normalmente impressos em mini-impressoras de cupons,
térmicas ou de impacto, mas não limitado à elas. As impressoras, marcas e
modelos suportados dependem dos modelos suportados no projeto `PyESCPOS`_.

Para autorizar e transmitir documentos eletrônicos através da tecnologia
`SAT-CF-e`_ é preciso comunicar-se com os equipamentos SAT. Para isso, dê uma
olhada no `Projeto SATCFe`_. **Este projeto lida apenas com a questão da
impressão do extrato para documentos CF-e.**

.. warning::

    A **Base4 Sistemas** e os desenvolvedores envolvidos neste projeto, NÃO
    ASSUMEM NEM TEM QUALQUER RESPONSABILIDADE sobre os "Extratos do CF-e-SAT"
    gerados por esta biblioteca de código, nem diretamente nem através de uma
    APLICAÇÃO USUÁRIA. Use por sua própria conta e risco.


Exemplos de Uso
===============

Há dois tipos de documentos CF-e-SAT: de **venda** e de **cancelamento** de uma
venda anteriormente autorizada.


Extratos do CF-e de Venda
-------------------------

Para emitir um extrato de um CF-e de venda, você irá precisar do `XML`_ do
CF-e-SAT de venda, que é o documento fiscal, e uma impressora ESC/POS |reg|
(veja as implementações disponíveis no projeto `PyESCPOS`_):

.. sourcecode:: python

    from escpos import SerialConnection
    from escpos.impl.daruma import DR700
    from satextrato import ExtratoCFeVenda

    conn = SerialConnection.create('COM1:9600,8,1,N')
    impressora = DR700(conn)
    impressora.init()

    with open(r'C:\CFe351702.xml', 'r') as fp:
        extrato = ExtratoCFeVenda(fp, impressora)
        extrato.imprimir()


Extratos do CF-e de Cancelamento
--------------------------------

Para emitir um extrato do CF-e-SAT de cancelamento, além do documento de
cancelamento você também irá precisar do documento da venda, ao qual o documento
de cancelamento se refere. Seguindo a mesma linha do exemplo anterior:

.. sourcecode:: python

    with open('CFe_1.xml', 'r') as fvenda, open('CFeCanc_1.xml', 'r') as fcanc:
        extrato = ExtratoCFeCancelamento(fvenda, fcanc, impressora)
        extrato.imprimir()


Outros Exemplos
---------------

Eventualmente, você poderá encontrar outros exemplos no `Wiki`_ do projeto.


Configurações do Extrato
========================

Vários detalhes da impressão dos extratos podem ser configurados. A aplicação
poderá indicar onde o arquivo de configurações pode ser encontrado invocando a
função ``satextrato.config.configurar()`` antes de comandar a impressão:

.. sourcecode:: python

    from satextrato import config
    config.configurar(arquivo='/caminho/para/arquivo.cfg')

.. note::

    Invocar a função ``configurar()`` uma segunda vez não terá qualquer efeito.
    Se a aplicação precisar recarregar as configurações invoque a função
    ``satextrato.config.reconfigurar()``.

Se um caminho não for especificado o arquivo de configurações será gravado no
diretório do usuário, normalmente em ``~/.satcfe/extrato.cfg``. O formato do
arquivo de configurações é simples, como em um arquivo *INI*, cujo conteúdo
padrão é:

.. sourcecode:: ini

    [cupom]
    avancar_linhas = 7
    cortar_documento = no
    cortar_parcialmente = no
    exibir_nome_consumidor = no
    itens_modo_condensado = yes

    [qrcode]
    tamanho_modulo = 4
    nivel_correcao = L
    nome_aplicativo = De Olho Na Nota
    mensagem = Consulte o QRCode pelo aplicativo %(nome_aplicativo)s, disponivel na AppStore (Apple) e PlayStore (Android)
    mensagem_modo_condensado = yes

    [code128]
    ignorar = no
    altura = 56
    quebrar = yes
    quebrar_partes = 14,14,14,2
    truncar = yes
    truncar_tamanho = 22

    [rodape]
    direita = http://git.io/vJRRk
    esquerda = Extrato CF-e-SAT

Para saber quais valores usar dependendo do tipo de dados de cada opção,
consulte a documentação do módulo `ConfigParser`_ da biblioteca padrão do
Python.

.. note::

    **Note que algumas opções podem fazer com que o extrato não seja impresso
    em conformidade com a legislação.** Algumas opções são úteis quando estiver
    **em desenvolvimento**. No entanto, tenha certeza de consultar o "Manual de
    Orientação" do SAT, **item 4**, "Leiaute de Impressão" antes de modificar
    certas opções de impressão, ou de permitir que o usuário as modifique,
    quando estiver imprimindo extratos SAT **em produção**.


Seção ``cupom``
---------------

Corpo do extrato e opções para finalização do cupom.

+---------------------------------+------+----------------------------------------------+
| Opção                           | Tipo | Comentários                                  |
+=================================+======+==============================================+
| ``avancar_linhas``              | int  | Número de linhas a avançar no final do       |
|                                 |      | documento, antes de guilhotinar (se for o    |
|                                 |      | caso).                                       |
+---------------------------------+------+----------------------------------------------+
|  ``cortar_documento``           | bool | Indica se ao final do documento a guilhotina |
|                                 |      | deverá ser acionada (se disponível).         |
+---------------------------------+------+----------------------------------------------+
| ``cortar_parcialmente``         | bool | Indica se o documento deverá ser apenas      |
|                                 |      | parcialmente guilhotinado. Esta opção terá   |
|                                 |      | efeito apenas se ``cortar_documento``        |
|                                 |      | estiver ligada.                              |
+---------------------------------+------+----------------------------------------------+
| ``exibir_nome_consumidor``      | bool | Indica se o nome do consumidor (se houver)   |
|                                 |      | deverá ser impresso no extrato. Normalmente, |
|                                 |      | apenas o número do documento é impresso.     |
+---------------------------------+------+----------------------------------------------+
| ``itens_modo_condensado``       | bool | Indica se os itens deverão ser impressos em  |
|                                 |      | modo condensado. Senão, serão impressos no   |
|                                 |      | modo normal.                                 |
+---------------------------------+------+----------------------------------------------+

O avaço de linhas será honrado mesmo que a opção para cortar o documento esteja
ligada e a impressora possuir uma guilhotina. Isso é útil devido ao fato de que
a posição do cabeçote de impressão (e isso depende de cada modelo de impressora)
pode requerer que o documento avançe um pouco antes da guilhotina ser acionada,
para evitar que o documento seja cortado com dados abaixo da guilhotina.


Seção ``qrcode``
----------------

Código bidimensional `QRCode`_ e a mensagem logo após, sobre o aplicativo para
autenticação/validação do documento emitido. O código QR contém diversas
informações à respeito do documento fiscal. Para detalhes, consulte a
"Especificação de Requisitos" do SAT-CF-e e/ou o "Manual de Orientação".

+---------------------------------+------+----------------------------------------------+
| Opção                           | Tipo | Comentários                                  |
+=================================+======+==============================================+
| ``tamanho_modulo``              | int  | Tamanho do módulo QRCode.                    |
|                                 |      | Consulte a documentação da `PyESCPOS`_ para  |
|                                 |      | mais detalhes sobre esta opção.              |
+---------------------------------+------+----------------------------------------------+
| ``nivel_correcao``              | str  | Nível de correção de erros.                  |
|                                 |      | Consulte a documentação da `PyESCPOS`_ para  |
|                                 |      | mais detalhes sobre esta opção.              |
+---------------------------------+------+----------------------------------------------+
| ``nome_aplicativo``             | str  | Nome do aplicativo capaz de consultar a      |
|                                 |      | validade do documento fiscal através do      |
|                                 |      | QRCode impresso no extrato. Veja mais sobre  |
|                                 |      | isso mais adiante.                           |
+---------------------------------+------+----------------------------------------------+
| ``mensagem``                    | str  | Mensagem a ser impressa logo após o QRCode.  |
|                                 |      | Veja mais sobre isso mais adiante.           |
+---------------------------------+------+----------------------------------------------+
| ``mensagem_modo_condensado``    | bool | Se a mensagem deverá ser impressa em modo    |
|                                 |      | condensado ou em modo normal de impressão.   |
+---------------------------------+------+----------------------------------------------+

A mensagem a ser impressa logo após o QRCode normalmente irá instruir o
consumidor a utilizar um certo aplicativo que, em tese, é capaz de verificar a
autenticidade do documento fiscal que aquele extrato representa. O nome do
aplicativo é configurado separado da mensagem e, embora a mensagem possa incluir
o nome do aplicativo diretamente (*hardcoded*), você poderá optar por usar o
recurso de interpolação para facilitar a configuração da mensagem, caso esta
precise conter o nome do aplicativo, por exemplo:

.. sourcecode:: ini

    nome_aplicativo = Super Validador
    mensagem = Utilize o app %(nome_aplicativo)s para validar este extrato.

Mais sobre interpolação na documentação do módulo `ConfigParser`_ da biblioteca
padrão do Python.


Seção ``code128``
-----------------

Opções para impressão do código de barras `Code128`_ (*em inglês*). Este código
contém os quarenta e quatro dígitos da "Chave de Acesso" que identifica o
documento fiscal.

+---------------------------------+------+----------------------------------------------+
| Opção                           | Tipo | Comentários                                  |
+=================================+======+==============================================+
| ``ignorar``                     | bool | Ignora a impressão do código de barras.      |
+---------------------------------+------+----------------------------------------------+
| ``altura``                      | int  | Determina a altura das barras. Para saber o  |
|                                 |      | significado desse valor, consulte a          |
|                                 |      | documentação da `PyESCPOS`_.                 |
+---------------------------------+------+----------------------------------------------+
| ``quebrar``                     | bool | Indica se o código de barras deverá ser      |
|                                 |      | quebrado em partes. Mais detalhes abaixo.    |
+---------------------------------+------+----------------------------------------------+
| ``quebrar_partes``              | str  | Lista de tamanhos para quebra do código de   |
|                                 |      | barras. Mais detalhes abaixo.                |
+---------------------------------+------+----------------------------------------------+
| ``truncar``                     | bool | Indica se o código de barras deverá ser      |
|                                 |      | truncado ao invés de ser quebrado. Um código |
|                                 |      | truncado irá renderizar apenas um número     |
|                                 |      | especificado de dígitos da chave de acesso.  |
+---------------------------------+------+----------------------------------------------+
| ``truncar_tamanho``             | int  | Se for para truncar, esta propriedade indica |
|                                 |      | quantos digitos da chave de acesso serão     |
|                                 |      | considerados na impressão do código.         |
+---------------------------------+------+----------------------------------------------+

As opções para **truncar** e **quebrar** o código de barras são mutuamente
exclusivas e **truncar** possui precedência sobre **quebrar**. Veja os detalhes
sobre estas opções, a seguir.

A motivação para **quebrar** o código de barras é devido a uma limitação em que
certos modelos de impressoras podem não ser capazes de imprimir todos os 44
dígitos da chave de acesso em uma única linha. Assim, o código de 44 dígitos
pode ser quebrado em partes para tornar a impressão possível. Por exemplo, para
quebrar o código em duas partes, você poderá especificar ``quebrar_partes = 22,22``,
ou seja, duas partes com 22 dígitos cada. Certas impressoras com bobinas muito
estreitas podem ter uma quebra especificada em mais partes com menos dígitos em
cada parte. A regra é que a lista em ``quebrar_partes`` deverá especificar
apenas números inteiros, pares, maiores que zero, cuja soma seja igual a 44.

Truncar é uma opção que lhe permitirá imprimir o código de barras contendo
apenas parte dos dígitos da chave de acesso. Truncar tem precedência sobre a
quebra, o que significa que, se a opção ``truncar`` estiver ligada, então a
opção para quebra será ignorada.


Seção ``rodape``
----------------

Opções para configuração do rodapé.

+---------------------------------+------+----------------------------------------------+
| Opção                           | Tipo | Comentários                                  |
+=================================+======+==============================================+
| ``esquerda``                    | str  | Texto (curto) para ser exibido no rodapé do  |
|                                 |      | extrato, à esquerda da borda do cupom.       |
+---------------------------------+------+----------------------------------------------+
| ``direita``                     | str  | Texto (curto) para ser exibido no rodapé do  |
|                                 |      | extrato, à direita da borda do cupom.        |
+---------------------------------+------+----------------------------------------------+


Executando Testes
=================

Para executar os testes de emissão dos extratos em impressoras conectadas
à portas seriais, ou em impressoras USB a partir de virtualizadores de portas
seriais:

.. sourcecode:: shell-session

    $ python setup.py test -a \
            "--escpos-impl=escpos.impl.daruma.DR700 "\
            "--escpos-if=serial "\
            "--escpos-if-settings=\"/dev/ttyS7:9600,8,1,N\""

Para executar os testes em uma impressora conectada à rede, via TCP/IP no
endereço ``192.168.1.200`` porta ``9100``:

.. sourcecode:: shell-session

    $ python setup.py test -a \
            "--escpos-impl=escpos.impl.epson.TMT20 "\
            "--escpos-if=network "\
            "--escpos-if-settings=\"192.168.1.200:9100\""

Para mais opções sobre testes invoque a ajuda e procure por "custom options":

.. sourcecode:: shell-session

    $ python setup.py test -a --help

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
.. _`QRCode`: https://pt.wikipedia.org/wiki/C%C3%B3digo_QR
.. _`Code128`: https://en.wikipedia.org/wiki/Code_128
.. _`ConfigParser`: https://docs.python.org/2.7/library/configparser.html
