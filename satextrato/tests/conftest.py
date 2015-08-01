# -*- coding: utf-8 -*-
#
# satextrato/tests/conftest.py
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

import importlib
import sys

import pytest


def pytest_addoption(parser):

    parser.addoption('--escpos-impl', action='store',
            default='escpos.impl.epson.GenericESCPOS',
            help='implementacao ESC/POS a ser instanciada')

    parser.addoption('--escpos-if', action='store', default='serial',
            help='interface ESC/POS a ser utilizada (serial, usb, bluetooth)')

    # USB, configurações de porta
    # --usb-idvendor
    # --usb-idproduct
    # --usb-bus
    # --usb-ep-out
    # --usb-ep-in
    #

    # Bluetooth, configurações da conexão
    # --bluetooth-mac
    #

    # serial (RS232), configurações de porta
    default_port = 'COM1' if 'win' in sys.platform else '/dev/ttyS0'

    parser.addoption('--serial-port', action='store', default=default_port,
            help='porta serial, nome da porta')

    parser.addoption('--serial-baudrate', action='store', default='9600',
            help='porta serial, velocidade de transmissao')

    parser.addoption('--serial-databits', action='store', default='8',
            help='porta serial, bits de dados')

    parser.addoption('--serial-stopbits', action='store', default='1',
            help='porta serial, bits de parada')

    parser.addoption('--serial-parity', action='store', default='N',
            help='porta serial, paridade')

    parser.addoption('--serial-protocol', action='store', default='RTSCTS',
            help='porta serial, protocolo')


@pytest.fixture(scope='module')
def escpos_interface(request):
    interface = request.config.getoption('--escpos-if')
    if interface == 'serial':
        from escpos.serial import SerialSettings
        options = [
                request.config.getoption('--serial-port'),
                request.config.getoption('--serial-baudrate'),
                request.config.getoption('--serial-databits'),
                request.config.getoption('--serial-stopbits'),
                request.config.getoption('--serial-parity'),
                request.config.getoption('--serial-protocol'),]
        conn = SerialSettings.as_from(':'.join(options)).get_connection()
        return conn
    else:
        raise NotImplementedError('Interface nao disponivel: %s' % interface)


@pytest.fixture(scope='module')
def escpos_impl(request):
    names = request.config.getoption('--escpos-impl').split('.')
    _module = importlib.import_module('.'.join(names[:-1])) # escpos.impl.epson
    return getattr(_module, names[-1]) # GenericESCPOS <class>


@pytest.fixture(scope='module')
def xml_venda():
    return XML_VENDA


@pytest.fixture(scope='module')
def xml_cancelamento():
    return XML_CANCELAMENTO


@pytest.fixture(scope='module')
def xml_venda_complexo():
  return XML_VENDA_COMPLEXO


XML_VENDA = """<?xml version="1.0"?>
<CFe>
  <infCFe Id="CFe35150461099008000141599000017900000015450903"
                versao="0.06" versaoDadosEnt="0.06" versaoSB="010000">
    <ide>
      <cUF>35</cUF>
      <cNF>545090</cNF>
      <mod>59</mod>
      <nserieSAT>900001790</nserieSAT>
      <nCFe>000001</nCFe>
      <dEmi>20150409</dEmi>
      <hEmi>093455</hEmi>
      <cDV>3</cDV>
      <tpAmb>2</tpAmb>
      <CNPJ>08427847000169</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <assinaturaQRCODE>aU3zLH9j0jCrqwvVFAEgfzEaHl4IpdHtrYW8iMdxjUvFcWGvufRjVBesYfvuWKEaqyk7WDkbQ2wEx4rf02+l1HMwkTUevf70rgDVoVL9T22ZvPvXhokzMwdU9EumAMw1+4U8XFj6FCCKbvUar5zzVpG5TLrBmxOmVsBMkksqU4NpBPIZaMWQpqegIFhC4q0yddkbkkVaBO6Spn3BVQYiO7ExmMExLdr8KXPT4aaieUfwbE5F2aN7NDG4uK/IQqWsJK0T2nemy7EwQSgep9jgO5CEL5IQ1LVcUpDQQkNXZ5dyqe2+Cq7d3eZlutsAYFKfcePdSEFX0IEwd/K07hlBUg==</assinaturaQRCODE>
      <numeroCaixa>001</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>61099008000141</CNPJ>
      <xNome>DIMAS DE MELO PIMENTA SISTEMAS DE PONTO E ACESSO LTDA</xNome>
      <xFant>DIMEP</xFant>
      <enderEmit>
        <xLgr>AVENIDA MOFARREJ</xLgr>
        <nro>840</nro>
        <xCpl>908</xCpl>
        <xBairro>VL. LEOPOLDINA</xBairro>
        <xMun>SAO PAULO</xMun>
        <CEP>05311000</CEP>
      </enderEmit>
      <IE>111111111111</IE>
      <IM>12345</IM>
      <cRegTrib>3</cRegTrib>
      <cRegTribISSQN>1</cRegTribISSQN>
      <indRatISSQN>N</indRatISSQN>
    </emit>
    <dest/>
    <det nItem="1">
      <prod>
        <cProd>123456</cProd>
        <cEAN>4007817525074</cEAN>
        <xProd>BORRACHA PVC STAEDTLER</xProd>
        <NCM>40169200</NCM>
        <CFOP>5102</CFOP>
        <uCom>UN</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>7.50</vUnCom>
        <vProd>7.50</vProd>
        <indRegra>A</indRegra>
        <vItem>7.50</vItem>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <total>
      <ICMSTot>
        <vICMS>0.00</vICMS>
        <vProd>7.50</vProd>
        <vDesc>0.00</vDesc>
        <vPIS>0.00</vPIS>
        <vCOFINS>0.00</vCOFINS>
        <vPISST>0.00</vPISST>
        <vCOFINSST>0.00</vCOFINSST>
        <vOutro>0.00</vOutro>
      </ICMSTot>
      <vCFe>7.50</vCFe>
    </total>
    <pgto>
      <MP>
        <cMP>01</cMP>
        <vMP>7.50</vMP>
      </MP>
      <vTroco>0.00</vTroco>
    </pgto>
  </infCFe>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
      <Reference URI="#CFe35150461099008000141599000017900000015450903">
        <Transforms>
          <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
          <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        </Transforms>
        <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <DigestValue>kXw8qpeawla6Lmzc3ne5TlhTJvVC242UvxOUGa5nOU8=</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>irn9nniALO37lGtr5P8Xv+zRs4X/woCle1hWheOVzHJW6jvdOe+dwUU+1F7Q8OITVED9W8aT9GX96xMDAT8oEGZ1mEVOvVGXWTq+QGpr/99zYIf5AUY+X8a4DL1aFtPIGtaZ8UHTxhOg4cUHHkWmWUMkmw/+w3/2fQooC/OAC8vkS+Z3k6rPu2GdPI0fxS+Gz4KDlTLQRRKFWr7knlsLScQr9FnQ3SdOWAvAmAKivuTn6lrad8mdBpsJc+rbwuTeO1FdWB/XSgr1du2OrGWDjG/xP0/9npeKCddgYGuRyDs/c5gc8tTI4VsIvtnXqFZKRn0TxZh40dFyxg0+ou1NmA==</SignatureValue>
    <KeyInfo>
      <X509Data>
        <X509Certificate>LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlHNmpDQ0JOS2dBd0lCQWdJUURmNHQ4cGkyK3A3bHN4NEQrUTJueFRBTkJna3Foa2lHOXcwQkFRc0ZBREJuDQpNUXN3Q1FZRFZRUUdFd0pDVWpFMU1ETUdBMVVFQ2hNc1UyVmpjbVYwWVhKcFlTQmtZU0JHWVhwbGJtUmhJR1J2DQpJRVZ6ZEdGa2J5QmtaU0JUWVc4Z1VHRjFiRzh4SVRBZkJnTlZCQU1UR0VGRElGTkJWQ0JrWlNCVVpYTjBaU0JUDQpSVVpCV2lCVFVEQWVGdzB4TlRBek1UWXdNREF3TURCYUZ3MHlNREF6TVRNeU16VTVOVGxhTUlIbk1Rc3dDUVlEDQpWUVFHRXdKQ1VqRVNNQkFHQTFVRUNCTUpVMkZ2SUZCaGRXeHZNUkV3RHdZRFZRUUtGQWhUUlVaQldpMVRVREVQDQpNQTBHQTFVRUN4UUdRVU10VTBGVU1TZ3dKZ1lEVlFRTEZCOUJkWFJsYm5ScFkyRmtieUJ3YjNJZ1FWSWdVMFZHDQpRVm9nVTFBZ1UwRlVNUnd3R2dZRFZRUUxGQk14TkRJMk5UTXhORE13TVRBMk5qUTBNek15TVJJd0VBWURWUVFGDQpFd2s1TURBd01ERTNPVEF4UkRCQ0JnTlZCQU1UTzBSSlRVRlRSRVZOUlV4UFVFbE5SVTVVUVZOSlUxUkZUVUZUDQpSRVZRVDA1VVQwVkJRMFZUVTA5TVZFUkJPall4TURrNU1EQTRNREF3TVRReE1JSUJJakFOQmdrcWhraUc5dzBCDQpBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF4NUR0eTBrM2FQWFJONW0ydTVKSDIxUXd4OXRsOXlZaHBlQXE2MFpCDQppeGxBR1ZHOFVCV3VrZ2szV0FsRGMwQ1pPUFFuWVNTQmF6WjdsOWpDR09PWWNBUVZzaTJremdEbVA4dmNacXdZDQpGYjdTRDlIa0FzU0pMcVAwVU56NmxFMkZTSE1Od3c4RWJmOHJNREo5a0hiWUhDajcrU2VvdExaUWdTRmg4SFJ2DQpJcTNCTE90eG91aEg3WDdCOXNta01udXhFcHJ1d0tpSDN5Q0twb29LNmRZM3plRTFrRzRSTi9ZWGlhRVdyY3ZEDQpnbWlSVFVrbW0wRHJsdlVQb0JOVCtIY1RxWlpBOXF5SFdNdWY3QXJmN0FHUmRxeHpRbkZnamQxUGxFd014RnJRDQpUWFptTkZzQjJ6RTNDUkJBb1kwSkpUTk1UM0g5dmllU25tUWJ2bmNPZmZtN2V3SURBUUFCbzRJQ0R6Q0NBZ3N3DQpKQVlEVlIwUkJCMHdHNkFaQmdWZ1RBRURBNkFRQkE0Mk1UQTVPVEF3T0RBd01ERTBNVEFKQmdOVkhSTUVBakFBDQpNQTRHQTFVZER3RUIvd1FFQXdJRjREQWZCZ05WSFNNRUdEQVdnQlNPT1VFQVhQSzRCZHFvYlppNUFVWnRibVBmDQpBakJyQmdOVkhSOEVaREJpTUdDZ1hxQmNobHBvZEhSd09pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2DQpabWxqYVdGc0xtTnZiUzVpY2k5eVpYQnZjMmwwYjNKcGJ5OXNZM0l2WVdOellYUnpaV1poZW5Od0wyRmpjMkYwDQpjMlZtWVhwemNHTnliQzVqY213d2V3WURWUjBnQkhRd2NqQndCZ2tyQmdFRUFZSHNMUU13WXpCaEJnZ3JCZ0VGDQpCUWNDQVJaVmFIUjBjRG92TDJGamMyRjBMbWx0Y0hKbGJuTmhiMlpwWTJsaGJDNWpiMjB1WW5JdmNtVndiM05wDQpkRzl5YVc4dlpIQmpMMkZqYzJGMGMyVm1ZWHB6Y0M5a2NHTmZZV056WVhSelpXWmhlbk53TG5Ca1pqQVRCZ05WDQpIU1VFRERBS0JnZ3JCZ0VGQlFjREFqQ0Jwd1lJS3dZQkJRVUhBUUVFZ1pvd2daY3dYd1lJS3dZQkJRVUhNQUtHDQpVMmgwZEhCek9pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2Wm1samFXRnNMbU52YlM1aWNpOXlaWEJ2DQpjMmwwYjNKcGJ5OWpaWEowYVdacFkyRmtiM012WVdOellYUXRkR1Z6ZEdVdWNEZGpNRFFHQ0NzR0FRVUZCekFCDQpoaWhvZEhSd09pOHZiMk56Y0Mxd2FXeHZkQzVwYlhCeVpXNXpZVzltYVdOcFlXd3VZMjl0TG1KeU1BMEdDU3FHDQpTSWIzRFFFQkN3VUFBNElDQVFCNnFBalQ3YVo3MTdqT0RON0JYQnBnS1l3eVFWOUNlT3F1UHdXOWVESjhUQTVEDQpFSUFVZ0hBZHVIR1BtT1ZNYjF4RWFFeWdyeERvWEdhUFlCZzdxSi9DRTlyWTlyQVVobFRudTVhbWZncmx4d3BmDQptTmEvOE9sTjkrcGVoL3YzV3J5WE5vamNzOUNDQUNtTTVOSVVMandVK3R5aC80VUxCL3Z1OUhWd3RrYUdnMnlQDQozZTRkTkVYMjNQUTZ4eXA5T1J4V0xmekJFdmpOQUJZUlZuUUY4TUVBcUJYQzlTbFZodzNvcG1qVFNlUUxaQzNuDQpIZGREUlFHSjYvaW1ySHRpNTRqWS9EOVJYNGFra0JCaVpxYzB4L0RiVEVHbWxFdHdjZ2ttNjQxVy93c204TnI1DQo2UXNzTWQvZlhXYzAyNUg5eFRkZHQwUmhYcEpiRUtPSGlQNnhZSXJJYnhBNVluSWI5Qy9XQkp5SS9uQ0lxblU4DQprcVpvc0g1bE5qbU9Kb2QwZFJMVWVSWUhkYWVTekJXVVRTcDltQUVLVjlPQjU3WGtHVllZUkd5ZnBxL1dZR21wDQpCZ25KRmJ5UmgrcVdEYno5cnFrZzNKeDFzRjRIZ0xEajZXV0tEQzVKb3l5MS83ZENBWm9uNEt6Vi9NOHRkRnc0DQpZWG9xVkJkanBMZEVQbythSEIya29wYmI3MWpYc2JzcDcrdDV4WUh3TmlCa3dBcmFZajdiWWxkZ3FTdHYvWlZ0DQp0UENTMk5SSEo3dFpYN1dVemUrL3YyUG5wbklhMnNtZ0V2SEp5Zlp4WFJyRDNpZXFMV3gvd3RHZTdLOTh1cmUwDQowNGo5TVQwejF3T2RacG5zTGtjQjRUOEFBNlRyMkMrRDBvRE1ESjh4WlRkMUZ2N3k4T0ZvZ0pYeEFET0RFZz09DQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tDQotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0NCk1JSUcxakNDQkw2Z0F3SUJBZ0lRUWt0V0l6WksrU1pNdCtwMWhRd2NaVEFOQmdrcWhraUc5dzBCQVEwRkFEQ0INCmpERUxNQWtHQTFVRUJoTUNRbEl4TlRBekJnTlZCQW9UTEZObFkzSmxkR0Z5YVdFZ1pHRWdSbUY2Wlc1a1lTQmsNCmJ5QkZjM1JoWkc4Z1pHVWdVMkZ2SUZCaGRXeHZNVVl3UkFZRFZRUURFejFCUXlCU1lXbDZJR1JsSUZSbGMzUmwNCklGTmxZM0psZEdGeWFXRWdaR0VnUm1GNlpXNWtZU0JrYnlCRmMzUmhaRzhnWkdVZ1UyRnZJRkJoZFd4dk1CNFgNCkRURXlNVEl4TWpBd01EQXdNRm9YRFRJeU1USXhNakl6TlRrMU9Wb3daekVMTUFrR0ExVUVCaE1DUWxJeE5UQXoNCkJnTlZCQW9UTEZObFkzSmxkR0Z5YVdFZ1pHRWdSbUY2Wlc1a1lTQmtieUJGYzNSaFpHOGdaR1VnVTJGdklGQmgNCmRXeHZNU0V3SHdZRFZRUURFeGhCUXlCVFFWUWdaR1VnVkdWemRHVWdVMFZHUVZvZ1UxQXdnZ0lpTUEwR0NTcUcNClNJYjNEUUVCQVFVQUE0SUNEd0F3Z2dJS0FvSUNBUURuUTVFSThzK0s2bzQvL3RpMmN4TFM1d3VjVkJXcDNtdCsNClRzUGdGOW9odSt1RXlqYmdGcjlWSzVqa0RzZnhtT25lcXMxclFuMjFrTmJmakNmdnNabEVpcEkrdkh3U2h4dVUNCkNHM21KUGRqQlkzeUNvNXpWbUhRYXpLbXJYKzFJTEtsYVl1WWRyckt0bmNYL0p4OWFxRWZWUHo0d2w3dG9vVXQNCmF4eDFVbm9GVmlqZ01kcXArNHVPRGtHUWR2V0RvQStGMXh5eVlOcDJWZ2Nkb1lheUdTRFFodXR0WlBiOEluWTANCmtUczlmZnJETmpDcHY4cHl4cG1ISnFUMWNwYlFONWliTWUvMWd0UU8vMGlTRWloOWNrUnQxOUdoMkNDckdGYzMNCkFHYWZ2akwzY1d6aHNnTlNzdXBwVFRFcUpJTjhJVzMyK2JmUGo3YUxvS0k3MDczSmlCTE9BM2V1RjJUWjNKanUNCnpRSHJZaGVLYzJ2cWhuN0VJYlAzRTdHdG5xbzd5QWgrN3Bzd2E2L2dCYXdFSm45STkycHZYWXJNeHpSRm9JMCsNClRHejlIcjRmdEIwSUlORTNwbU5COFNEMFFGRWN6cWlzSFJwcDF4Z3kxa1UrZlBjSmdZajNsUUtUaDdFY055d0kNClUrQlFwNGJSY21GbDFDUHFIR084QldpbmZJTXR3cUtXVDhxSkdQRHJMNTVWYWx1b1Z5enNDSTBKZS85ZTRoa1INCkpvUmJHQ0UxaWl5ODlIWFVkckQyNVNGL0NJb0ptQkRGbXdDcSt0K0I5ZzdXMWYrSGpxb05xaVdTSnB5WnpLcW8NCkpzQlFPSHZLZm4xSSsrczU1cXlVL1cxN3pXdnFzNmZVWXowZkV2L2xLUlVtWjk0dTh2akkvbWFqT1lhTW82aWoNCmxqSXQ4VFNVNFFJREFRQUJvNElCVmpDQ0FWSXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96Q0JnUVlEVlIwZ0JIb3cNCmVEQjJCZ2tyQmdFRUFZSHNMUU13YVRCbkJnZ3JCZ0VGQlFjQ0FSWmJhSFIwY0RvdkwyRmpjMkYwTFhSbGMzUmwNCkxtbHRjSEpsYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dlpIQmpMMkZqYzJGMGMyVm0NCllYcHpjQzlrY0dOZllXTnpZWFJ6WldaaGVuTndMbkJrWmpCckJnTlZIUjhFWkRCaU1HQ2dYcUJjaGxwb2RIUncNCk9pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2Wm1samFXRnNMbU52YlM1aWNpOXlaWEJ2YzJsMGIzSnANCmJ5OXNZM0l2WVdOellYUnpaV1poZW5Od0wyRmpjMkYwYzJWbVlYcHpjR055YkM1amNtd3dEZ1lEVlIwUEFRSC8NCkJBUURBZ0VHTUIwR0ExVWREZ1FXQkJTT09VRUFYUEs0QmRxb2JaaTVBVVp0Ym1QZkFqQWZCZ05WSFNNRUdEQVcNCmdCVFZrSmFvdWdZbGNhLzhmZVh1b3N3UjRJZDJ2ekFOQmdrcWhraUc5dzBCQVEwRkFBT0NBZ0VBcnNwY0pGZnQNCkhmMlpQNnc1eFlFbXQ3Z0s5K0FtVXFObHlxaVNpODFYWXlJc0swdytSaUFCcDJOWnRKMEFxT1VKcFd0b3hTREYNCjIvM3VjTExoemcwM3JNTktHQ3V5S0R1VEtCSHprZHEySkgrUUJwWE9FQXNnSEZBWjhpbm5WbTNFcGJNTDA1enYNCkNNNDNUYlV4ejRhaEZZTHRrZVVvWGcyUXRjdEpJd2ZVOG5pOTZ3TzAvUVZ4TXV6eXhnY3E3WEpmVEZiejBleTkNCkxvUzJmZjJmMml5dXpDTDg2Q0dSZTF2bjVGUDVBZHBLSTNBcWRvQXMyVUdmZmd5Y3F5VDVWaFpoSmFXWmdTZU4NCnFMU2RnMk95ZkFudVlmZmJOQ0FFRkxDNmtHalBpV0hWbVBKc2VVTlFwWUlXMjNuTWVlMFZtZjMyaDBVU0lSRkcNCkw5d01mQ1JhcHpuaVZUbFo3bUZRK1pLTk1VOWRQbml3R3hTOEhGZzdsN1VjWmRhVmlpSElSdGRHU0h6V1RHTFINCk81WHFtWGJjemxkK0dIMmNCbURLeDVGdGc0VUpjMHBNY05yZ2dBNHFabFgzQU04dWs3N1lDbndkeXB1WjVSL2kNCittV29Mc2dvdUMyelpRS2dWM3cxS0lndi9FZzNnM1BmbGlzQzFQOFp5ay81Z1JyQ0VpVGNZaUduTkhNeXoxY0UNCmY5dkRRVHBJOGcwZmFreXV3Z3F2M2JwYm1oQTJNL3RGSzF1a1AyL01ZTDNvTG8rVzl3dUx4YThRNjZUTlpVR2wNCllkN1hwdUpiWlJuUkJrV3ZyVmRvUGhPRzZyc1BWTlNrOUJDZmZscDQwMGlZZEV2V1VtaUlaRk1OMUY2clpRb2gNCmtQZnBCQkF2YmZCZU1haWQ4UDNUaDFsSTcxd3RTdjEraDljPQ0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQ0KLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlHempDQ0JMYWdBd0lCQWdJUUFpSzJEaVU2Y1dOc2R0bzZBVTlua2pBTkJna3Foa2lHOXcwQkFRMEZBRENCDQpqREVMTUFrR0ExVUVCaE1DUWxJeE5UQXpCZ05WQkFvVExGTmxZM0psZEdGeWFXRWdaR0VnUm1GNlpXNWtZU0JrDQpieUJGYzNSaFpHOGdaR1VnVTJGdklGQmhkV3h2TVVZd1JBWURWUVFERXoxQlF5QlNZV2w2SUdSbElGUmxjM1JsDQpJRk5sWTNKbGRHRnlhV0VnWkdFZ1JtRjZaVzVrWVNCa2J5QkZjM1JoWkc4Z1pHVWdVMkZ2SUZCaGRXeHZNQjRYDQpEVEV5TVRJeE1qQXdNREF3TUZvWERUTXlNVEl4TWpJek5UazFPVm93Z1l3eEN6QUpCZ05WQkFZVEFrSlNNVFV3DQpNd1lEVlFRS0V5eFRaV055WlhSaGNtbGhJR1JoSUVaaGVtVnVaR0VnWkc4Z1JYTjBZV1J2SUdSbElGTmhieUJRDQpZWFZzYnpGR01FUUdBMVVFQXhNOVFVTWdVbUZwZWlCa1pTQlVaWE4wWlNCVFpXTnlaWFJoY21saElHUmhJRVpoDQplbVZ1WkdFZ1pHOGdSWE4wWVdSdklHUmxJRk5oYnlCUVlYVnNiekNDQWlJd0RRWUpLb1pJaHZjTkFRRUJCUUFEDQpnZ0lQQURDQ0Fnb0NnZ0lCQU5OYmlLZm1rOFZTR0Jsbm8xWHVYNXBoaWx3T3lRVmJyNGZ0c1NGdm92NlFBTC85DQpGSWFwelJEczFWdmNSaFRnQXVnK1Myc3RVRi9iU2dQY2JlOWxTTklmM3gyY09TRUg1ZEtMU2ZEWjVwYUY2U3l2DQppT05rS0lWZE95MG5HcUIvZjdmMzBtZDlMU0YwYk1abzI2bmRPNXViak9NU3ZrcjBzdGp2cXMzR2I2NjRPN3c1DQpnenlRcVVmN1ZKVTJWNXhMNzAvYW9IYmp4UTZZcFlIaDVUOHhlUEV2aUdNeHhobW9jdmVrMGVIbXhaMVpBRndmDQpmbWpacGdtKzNBbWUrQWJ1Z0IxcVlkOTdXQlVjL1I2clYzSFVJaEtMdmswQmMyQk5TQWpKVHNtUlJoNnhiNUVPDQpIV3U4SjlVOTNPVDBtQ0RTL0c0ekFwKzIwVlVaTlN5WHozdkhvdzNWQkE0ck43VUthTVA4U0FGcWJQd2pQaGY2DQpWeUhaSkhGeUlramxVL09lOGk4aFJoZSt1S0luem1kUklna3FqQzRKYlM4L0hKd1pCeWJ1clhtZlZnZ0JyWjcyDQp1SWxIeWZLQWVvZE82K1Vudk9RUTNkUXNLc2hsS2l2dUNKenZZbHBUYW5VbHlUeXJ1d0ZWL00zbHVwVXVsSkJ2DQorRVpuY2J3L0gyT1VGSU95cytmaUlqby9yUCtVVEVuRTBaeExMWWZNSE5Ibm95RkZWWlhXMFlLSVZ2d29VMEgyDQpMNEFlcnlzWWxzNGpHWWp6RXU2TXJoNFl2Sy9Fa2pGQnhseVFxQitrLzZZcHZEUEdBRWNDWExlM0xYZy9GR0RLDQpVdjRSSjRHMXd3WGJDU0lpdStsT3hIQndxa3FjYWo0ZVR4aGRyYXZFZmp4UDk1ZXBCN3A5Z1JXZXhLSWZBZ01CDQpBQUdqZ2dFb01JSUJKREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NSHNHQTFVZElBUjBNSEl3Y0FZSkt3WUJCQUdCDQo3QzBDTUdNd1lRWUlLd1lCQlFVSEFnRVdWV2gwZEhBNkx5OWhZM05oZEMxMFpYTjBaUzVwYlhCeVpXNXpZVzltDQphV05wWVd3dVkyOXRMbUp5TDNKbGNHOXphWFJ2Y21sdkwyUndZeTloWTNObFptRjZjM0F2WkhCalgyRmpjMlZtDQpZWHB6Y0M1d1pHWXdaUVlEVlIwZkJGNHdYREJhb0ZpZ1ZvWlVhSFIwY0RvdkwyRmpjMkYwTFhSbGMzUmxMbWx0DQpjSEpsYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dmJHTnlMMkZqYzJWbVlYcHpjQzloDQpZM05sWm1GNmMzQmpjbXd1WTNKc01BNEdBMVVkRHdFQi93UUVBd0lCQmpBZEJnTlZIUTRFRmdRVTFaQ1dxTG9HDQpKWEd2L0gzbDdxTE1FZUNIZHI4d0RRWUpLb1pJaHZjTkFRRU5CUUFEZ2dJQkFFalhiSFhGNGxXVEFDSHJ0MnR3DQoyamRyem5qM1FJdnhNWlBtVVduR0lRRUdJK0Q4SXZRTE1MWDJGd2pERVNkL0JKUXlITHM3Y1AvdDRxeEsyemZIDQo2dldvS1F4cGljQU5CbEhZMEo1ZlZVZ0ptQXR2bWlCbzV5U2FubHN2ek1vZCt3U0pUT2ZEZjBnMktIZmhZMkk2DQpIRGRzcWRoS2M4TFMvWCtBenRiVkVYT1k4c1pIVzhMbU9pOFI0WW9hYmZEY2FDdDBsb2hGQzFmRzV3RHA1OW1tDQpWdDAzTkxZaHZiaTNDdENYRHd1Q3ZmNDhjWmwvb1VWdHFpNHAzbitDSk5qbDN0N0ZBMEZkMGdrVG1wcUtEYnowDQpSbEZtdjUzeVk0cjNpT2NCdU5NZW91RDEvc0QyYkJrU01DU3lFL0pYR3ZQVDBUNjhVYklGTDdHbXExd1h3ckFCDQpsZExyQjJBR0FEbXdXZXc0emxnVjJ1SjNnUkpZL2RSSUVSMVFrSEV6dERRQThnbnFtWkptMVg1WWlBc3hvTkpGDQpBc2ZCNUVURTM5Tk9nMklJcjQ4VzQwSjVOUWRKcGR0bHFSbXAzNjFPUEl5TnpWNGY5NzkxbkZVaGdPOVpkYVJ5DQpoMXk4N3FXSGVJM2ZPS1dGOWdpSjU0NUE5S0gvaWozNnFCWlRoRk9ETE0wRWdRNTRGZ1lCL0pHQ0VrbFBTdkorDQpMYVlDQWZySjNjWFd6K25oTlBMeXhNNUNBT2duVmlGRWdmRU5mRkZvRis4cW1ISU9ENlVYZnA1S1JjSkwzcDhkDQpZUVc2VW9sQ2tpaHUwUzFER2hFa0p6R05WOVd1TUE4T1lWQWtRNDJ0a2VRd1g5NVFRaWNwNFpTaGhyRnBKUVNHDQozSlFMWEdvajc4OXJxR3NqT24xbE1nbzMNCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0=</X509Certificate>
      </X509Data>
    </KeyInfo>
  </Signature>
</CFe>
"""

XML_CANCELAMENTO = """<?xml version="1.0"?>
<CFeCanc>
  <infCFe Id="CFe35150461099008000141599000017900000053222424"
        versao="0.06"
        chCanc="CFe35150461099008000141599000017900000042844470">
    <dEmi>20150418</dEmi>
    <hEmi>165831</hEmi>
    <ide>
      <cUF>35</cUF>
      <cNF>322242</cNF>
      <mod>59</mod>
      <nserieSAT>900001790</nserieSAT>
      <nCFe>000005</nCFe>
      <dEmi>20150418</dEmi>
      <hEmi>165952</hEmi>
      <cDV>4</cDV>
      <CNPJ>08427847000169</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <assinaturaQRCODE>TTwb6m6gFlISC81lrh+dJzIOWCIuhN4ocT3EVxUbfhX/pw/TjlbytvWHYNRC/GMEKxlYnmw1L5shEV0HUG8kToHbgM/0OY91uOTkzbWj4jEt0uOgUn3agC8iWNjoFnsx7Psie1s4gqsq8ho2XGILzQjd/BhItwoc+6n76QtGee7Hh2cAqVXRad/sIa8FtLb/+U3/2szn5tDfBbBrpSYRUrlE1w1wjKV0XrQu3CUXv3IGhJOAaoZREekKBG/rkvFeVTURQ0YpoIB9EoXPBzSEOZHq/7o69SA3k0ObTGrcIxUrjDdlol88ebulB82a1mCgDEW808BCKv0uLbhROkww/Q==</assinaturaQRCODE>
      <numeroCaixa>001</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>61099008000141</CNPJ>
      <xNome>DIMAS DE MELO PIMENTA SISTEMAS DE PONTO E ACESSO LTDA</xNome>
      <xFant>DIMEP</xFant>
      <enderEmit>
        <xLgr>AVENIDA MOFARREJ</xLgr>
        <nro>840</nro>
        <xCpl>908</xCpl>
        <xBairro>VL. LEOPOLDINA</xBairro>
        <xMun>SAO PAULO</xMun>
        <CEP>05311000</CEP>
      </enderEmit>
      <IE>111111111111</IE>
      <IM>12345</IM>
    </emit>
    <dest/>
    <total>
      <vCFe>15.00</vCFe>
    </total>
    <infAdic>
      <obsFisco xCampo="xCampo1">
        <xTexto>xTexto1</xTexto>
      </obsFisco>
    </infAdic>
  </infCFe>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo xmlns="http://www.w3.org/2000/09/xmldsig#">
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
      <Reference URI="#CFe35150461099008000141599000017900000053222424">
        <Transforms>
          <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
          <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        </Transforms>
        <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <DigestValue>ogkxm3+eJgkXtNzz81JVV1E+kOKS/+CprpEk2jzpchE=</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>e56LSV41xwmkrEbBBrImubdJkoOVqB0VgnbVPRmpLUuoKY/HAolcDtsKc+aqq0HMwvAt3HgHiraz8DKHx/0AxuOf78D82j0thS7Toco+RlYk39w+4mizLU2DpktKg9f6BUrQszG4z6UxBLunsYQ9CBrI3EmmaRRBMmaHXQEXwb7NI7KKYXQxtGwjLiTjCz/PDZiLrG2RdsdjqtCAW26mzDPd17tFRCkg/mrQZe4H36Ei5jvV4gGigYP2MwfAuLvaycmlSqJqg6Cr9AMU27+nrogJMxZ7+Hz8mY2oeMvKyu2rJn01N8o+3gGvUuc9l+BzyyB0HRVJX9AThXTghXbINA==</SignatureValue>
    <KeyInfo>
      <X509Data>
        <X509Certificate>LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlHNmpDQ0JOS2dBd0lCQWdJUURmNHQ4cGkyK3A3bHN4NEQrUTJueFRBTkJna3Foa2lHOXcwQkFRc0ZBREJuDQpNUXN3Q1FZRFZRUUdFd0pDVWpFMU1ETUdBMVVFQ2hNc1UyVmpjbVYwWVhKcFlTQmtZU0JHWVhwbGJtUmhJR1J2DQpJRVZ6ZEdGa2J5QmtaU0JUWVc4Z1VHRjFiRzh4SVRBZkJnTlZCQU1UR0VGRElGTkJWQ0JrWlNCVVpYTjBaU0JUDQpSVVpCV2lCVFVEQWVGdzB4TlRBek1UWXdNREF3TURCYUZ3MHlNREF6TVRNeU16VTVOVGxhTUlIbk1Rc3dDUVlEDQpWUVFHRXdKQ1VqRVNNQkFHQTFVRUNCTUpVMkZ2SUZCaGRXeHZNUkV3RHdZRFZRUUtGQWhUUlVaQldpMVRVREVQDQpNQTBHQTFVRUN4UUdRVU10VTBGVU1TZ3dKZ1lEVlFRTEZCOUJkWFJsYm5ScFkyRmtieUJ3YjNJZ1FWSWdVMFZHDQpRVm9nVTFBZ1UwRlVNUnd3R2dZRFZRUUxGQk14TkRJMk5UTXhORE13TVRBMk5qUTBNek15TVJJd0VBWURWUVFGDQpFd2s1TURBd01ERTNPVEF4UkRCQ0JnTlZCQU1UTzBSSlRVRlRSRVZOUlV4UFVFbE5SVTVVUVZOSlUxUkZUVUZUDQpSRVZRVDA1VVQwVkJRMFZUVTA5TVZFUkJPall4TURrNU1EQTRNREF3TVRReE1JSUJJakFOQmdrcWhraUc5dzBCDQpBUUVGQUFPQ0FROEFNSUlCQ2dLQ0FRRUF4NUR0eTBrM2FQWFJONW0ydTVKSDIxUXd4OXRsOXlZaHBlQXE2MFpCDQppeGxBR1ZHOFVCV3VrZ2szV0FsRGMwQ1pPUFFuWVNTQmF6WjdsOWpDR09PWWNBUVZzaTJremdEbVA4dmNacXdZDQpGYjdTRDlIa0FzU0pMcVAwVU56NmxFMkZTSE1Od3c4RWJmOHJNREo5a0hiWUhDajcrU2VvdExaUWdTRmg4SFJ2DQpJcTNCTE90eG91aEg3WDdCOXNta01udXhFcHJ1d0tpSDN5Q0twb29LNmRZM3plRTFrRzRSTi9ZWGlhRVdyY3ZEDQpnbWlSVFVrbW0wRHJsdlVQb0JOVCtIY1RxWlpBOXF5SFdNdWY3QXJmN0FHUmRxeHpRbkZnamQxUGxFd014RnJRDQpUWFptTkZzQjJ6RTNDUkJBb1kwSkpUTk1UM0g5dmllU25tUWJ2bmNPZmZtN2V3SURBUUFCbzRJQ0R6Q0NBZ3N3DQpKQVlEVlIwUkJCMHdHNkFaQmdWZ1RBRURBNkFRQkE0Mk1UQTVPVEF3T0RBd01ERTBNVEFKQmdOVkhSTUVBakFBDQpNQTRHQTFVZER3RUIvd1FFQXdJRjREQWZCZ05WSFNNRUdEQVdnQlNPT1VFQVhQSzRCZHFvYlppNUFVWnRibVBmDQpBakJyQmdOVkhSOEVaREJpTUdDZ1hxQmNobHBvZEhSd09pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2DQpabWxqYVdGc0xtTnZiUzVpY2k5eVpYQnZjMmwwYjNKcGJ5OXNZM0l2WVdOellYUnpaV1poZW5Od0wyRmpjMkYwDQpjMlZtWVhwemNHTnliQzVqY213d2V3WURWUjBnQkhRd2NqQndCZ2tyQmdFRUFZSHNMUU13WXpCaEJnZ3JCZ0VGDQpCUWNDQVJaVmFIUjBjRG92TDJGamMyRjBMbWx0Y0hKbGJuTmhiMlpwWTJsaGJDNWpiMjB1WW5JdmNtVndiM05wDQpkRzl5YVc4dlpIQmpMMkZqYzJGMGMyVm1ZWHB6Y0M5a2NHTmZZV056WVhSelpXWmhlbk53TG5Ca1pqQVRCZ05WDQpIU1VFRERBS0JnZ3JCZ0VGQlFjREFqQ0Jwd1lJS3dZQkJRVUhBUUVFZ1pvd2daY3dYd1lJS3dZQkJRVUhNQUtHDQpVMmgwZEhCek9pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2Wm1samFXRnNMbU52YlM1aWNpOXlaWEJ2DQpjMmwwYjNKcGJ5OWpaWEowYVdacFkyRmtiM012WVdOellYUXRkR1Z6ZEdVdWNEZGpNRFFHQ0NzR0FRVUZCekFCDQpoaWhvZEhSd09pOHZiMk56Y0Mxd2FXeHZkQzVwYlhCeVpXNXpZVzltYVdOcFlXd3VZMjl0TG1KeU1BMEdDU3FHDQpTSWIzRFFFQkN3VUFBNElDQVFCNnFBalQ3YVo3MTdqT0RON0JYQnBnS1l3eVFWOUNlT3F1UHdXOWVESjhUQTVEDQpFSUFVZ0hBZHVIR1BtT1ZNYjF4RWFFeWdyeERvWEdhUFlCZzdxSi9DRTlyWTlyQVVobFRudTVhbWZncmx4d3BmDQptTmEvOE9sTjkrcGVoL3YzV3J5WE5vamNzOUNDQUNtTTVOSVVMandVK3R5aC80VUxCL3Z1OUhWd3RrYUdnMnlQDQozZTRkTkVYMjNQUTZ4eXA5T1J4V0xmekJFdmpOQUJZUlZuUUY4TUVBcUJYQzlTbFZodzNvcG1qVFNlUUxaQzNuDQpIZGREUlFHSjYvaW1ySHRpNTRqWS9EOVJYNGFra0JCaVpxYzB4L0RiVEVHbWxFdHdjZ2ttNjQxVy93c204TnI1DQo2UXNzTWQvZlhXYzAyNUg5eFRkZHQwUmhYcEpiRUtPSGlQNnhZSXJJYnhBNVluSWI5Qy9XQkp5SS9uQ0lxblU4DQprcVpvc0g1bE5qbU9Kb2QwZFJMVWVSWUhkYWVTekJXVVRTcDltQUVLVjlPQjU3WGtHVllZUkd5ZnBxL1dZR21wDQpCZ25KRmJ5UmgrcVdEYno5cnFrZzNKeDFzRjRIZ0xEajZXV0tEQzVKb3l5MS83ZENBWm9uNEt6Vi9NOHRkRnc0DQpZWG9xVkJkanBMZEVQbythSEIya29wYmI3MWpYc2JzcDcrdDV4WUh3TmlCa3dBcmFZajdiWWxkZ3FTdHYvWlZ0DQp0UENTMk5SSEo3dFpYN1dVemUrL3YyUG5wbklhMnNtZ0V2SEp5Zlp4WFJyRDNpZXFMV3gvd3RHZTdLOTh1cmUwDQowNGo5TVQwejF3T2RacG5zTGtjQjRUOEFBNlRyMkMrRDBvRE1ESjh4WlRkMUZ2N3k4T0ZvZ0pYeEFET0RFZz09DQotLS0tLUVORCBDRVJUSUZJQ0FURS0tLS0tDQotLS0tLUJFR0lOIENFUlRJRklDQVRFLS0tLS0NCk1JSUcxakNDQkw2Z0F3SUJBZ0lRUWt0V0l6WksrU1pNdCtwMWhRd2NaVEFOQmdrcWhraUc5dzBCQVEwRkFEQ0INCmpERUxNQWtHQTFVRUJoTUNRbEl4TlRBekJnTlZCQW9UTEZObFkzSmxkR0Z5YVdFZ1pHRWdSbUY2Wlc1a1lTQmsNCmJ5QkZjM1JoWkc4Z1pHVWdVMkZ2SUZCaGRXeHZNVVl3UkFZRFZRUURFejFCUXlCU1lXbDZJR1JsSUZSbGMzUmwNCklGTmxZM0psZEdGeWFXRWdaR0VnUm1GNlpXNWtZU0JrYnlCRmMzUmhaRzhnWkdVZ1UyRnZJRkJoZFd4dk1CNFgNCkRURXlNVEl4TWpBd01EQXdNRm9YRFRJeU1USXhNakl6TlRrMU9Wb3daekVMTUFrR0ExVUVCaE1DUWxJeE5UQXoNCkJnTlZCQW9UTEZObFkzSmxkR0Z5YVdFZ1pHRWdSbUY2Wlc1a1lTQmtieUJGYzNSaFpHOGdaR1VnVTJGdklGQmgNCmRXeHZNU0V3SHdZRFZRUURFeGhCUXlCVFFWUWdaR1VnVkdWemRHVWdVMFZHUVZvZ1UxQXdnZ0lpTUEwR0NTcUcNClNJYjNEUUVCQVFVQUE0SUNEd0F3Z2dJS0FvSUNBUURuUTVFSThzK0s2bzQvL3RpMmN4TFM1d3VjVkJXcDNtdCsNClRzUGdGOW9odSt1RXlqYmdGcjlWSzVqa0RzZnhtT25lcXMxclFuMjFrTmJmakNmdnNabEVpcEkrdkh3U2h4dVUNCkNHM21KUGRqQlkzeUNvNXpWbUhRYXpLbXJYKzFJTEtsYVl1WWRyckt0bmNYL0p4OWFxRWZWUHo0d2w3dG9vVXQNCmF4eDFVbm9GVmlqZ01kcXArNHVPRGtHUWR2V0RvQStGMXh5eVlOcDJWZ2Nkb1lheUdTRFFodXR0WlBiOEluWTANCmtUczlmZnJETmpDcHY4cHl4cG1ISnFUMWNwYlFONWliTWUvMWd0UU8vMGlTRWloOWNrUnQxOUdoMkNDckdGYzMNCkFHYWZ2akwzY1d6aHNnTlNzdXBwVFRFcUpJTjhJVzMyK2JmUGo3YUxvS0k3MDczSmlCTE9BM2V1RjJUWjNKanUNCnpRSHJZaGVLYzJ2cWhuN0VJYlAzRTdHdG5xbzd5QWgrN3Bzd2E2L2dCYXdFSm45STkycHZYWXJNeHpSRm9JMCsNClRHejlIcjRmdEIwSUlORTNwbU5COFNEMFFGRWN6cWlzSFJwcDF4Z3kxa1UrZlBjSmdZajNsUUtUaDdFY055d0kNClUrQlFwNGJSY21GbDFDUHFIR084QldpbmZJTXR3cUtXVDhxSkdQRHJMNTVWYWx1b1Z5enNDSTBKZS85ZTRoa1INCkpvUmJHQ0UxaWl5ODlIWFVkckQyNVNGL0NJb0ptQkRGbXdDcSt0K0I5ZzdXMWYrSGpxb05xaVdTSnB5WnpLcW8NCkpzQlFPSHZLZm4xSSsrczU1cXlVL1cxN3pXdnFzNmZVWXowZkV2L2xLUlVtWjk0dTh2akkvbWFqT1lhTW82aWoNCmxqSXQ4VFNVNFFJREFRQUJvNElCVmpDQ0FWSXdEd1lEVlIwVEFRSC9CQVV3QXdFQi96Q0JnUVlEVlIwZ0JIb3cNCmVEQjJCZ2tyQmdFRUFZSHNMUU13YVRCbkJnZ3JCZ0VGQlFjQ0FSWmJhSFIwY0RvdkwyRmpjMkYwTFhSbGMzUmwNCkxtbHRjSEpsYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dlpIQmpMMkZqYzJGMGMyVm0NCllYcHpjQzlrY0dOZllXTnpZWFJ6WldaaGVuTndMbkJrWmpCckJnTlZIUjhFWkRCaU1HQ2dYcUJjaGxwb2RIUncNCk9pOHZZV056WVhRdGRHVnpkR1V1YVcxd2NtVnVjMkZ2Wm1samFXRnNMbU52YlM1aWNpOXlaWEJ2YzJsMGIzSnANCmJ5OXNZM0l2WVdOellYUnpaV1poZW5Od0wyRmpjMkYwYzJWbVlYcHpjR055YkM1amNtd3dEZ1lEVlIwUEFRSC8NCkJBUURBZ0VHTUIwR0ExVWREZ1FXQkJTT09VRUFYUEs0QmRxb2JaaTVBVVp0Ym1QZkFqQWZCZ05WSFNNRUdEQVcNCmdCVFZrSmFvdWdZbGNhLzhmZVh1b3N3UjRJZDJ2ekFOQmdrcWhraUc5dzBCQVEwRkFBT0NBZ0VBcnNwY0pGZnQNCkhmMlpQNnc1eFlFbXQ3Z0s5K0FtVXFObHlxaVNpODFYWXlJc0swdytSaUFCcDJOWnRKMEFxT1VKcFd0b3hTREYNCjIvM3VjTExoemcwM3JNTktHQ3V5S0R1VEtCSHprZHEySkgrUUJwWE9FQXNnSEZBWjhpbm5WbTNFcGJNTDA1enYNCkNNNDNUYlV4ejRhaEZZTHRrZVVvWGcyUXRjdEpJd2ZVOG5pOTZ3TzAvUVZ4TXV6eXhnY3E3WEpmVEZiejBleTkNCkxvUzJmZjJmMml5dXpDTDg2Q0dSZTF2bjVGUDVBZHBLSTNBcWRvQXMyVUdmZmd5Y3F5VDVWaFpoSmFXWmdTZU4NCnFMU2RnMk95ZkFudVlmZmJOQ0FFRkxDNmtHalBpV0hWbVBKc2VVTlFwWUlXMjNuTWVlMFZtZjMyaDBVU0lSRkcNCkw5d01mQ1JhcHpuaVZUbFo3bUZRK1pLTk1VOWRQbml3R3hTOEhGZzdsN1VjWmRhVmlpSElSdGRHU0h6V1RHTFINCk81WHFtWGJjemxkK0dIMmNCbURLeDVGdGc0VUpjMHBNY05yZ2dBNHFabFgzQU04dWs3N1lDbndkeXB1WjVSL2kNCittV29Mc2dvdUMyelpRS2dWM3cxS0lndi9FZzNnM1BmbGlzQzFQOFp5ay81Z1JyQ0VpVGNZaUduTkhNeXoxY0UNCmY5dkRRVHBJOGcwZmFreXV3Z3F2M2JwYm1oQTJNL3RGSzF1a1AyL01ZTDNvTG8rVzl3dUx4YThRNjZUTlpVR2wNCllkN1hwdUpiWlJuUkJrV3ZyVmRvUGhPRzZyc1BWTlNrOUJDZmZscDQwMGlZZEV2V1VtaUlaRk1OMUY2clpRb2gNCmtQZnBCQkF2YmZCZU1haWQ4UDNUaDFsSTcxd3RTdjEraDljPQ0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQ0KLS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tDQpNSUlHempDQ0JMYWdBd0lCQWdJUUFpSzJEaVU2Y1dOc2R0bzZBVTlua2pBTkJna3Foa2lHOXcwQkFRMEZBRENCDQpqREVMTUFrR0ExVUVCaE1DUWxJeE5UQXpCZ05WQkFvVExGTmxZM0psZEdGeWFXRWdaR0VnUm1GNlpXNWtZU0JrDQpieUJGYzNSaFpHOGdaR1VnVTJGdklGQmhkV3h2TVVZd1JBWURWUVFERXoxQlF5QlNZV2w2SUdSbElGUmxjM1JsDQpJRk5sWTNKbGRHRnlhV0VnWkdFZ1JtRjZaVzVrWVNCa2J5QkZjM1JoWkc4Z1pHVWdVMkZ2SUZCaGRXeHZNQjRYDQpEVEV5TVRJeE1qQXdNREF3TUZvWERUTXlNVEl4TWpJek5UazFPVm93Z1l3eEN6QUpCZ05WQkFZVEFrSlNNVFV3DQpNd1lEVlFRS0V5eFRaV055WlhSaGNtbGhJR1JoSUVaaGVtVnVaR0VnWkc4Z1JYTjBZV1J2SUdSbElGTmhieUJRDQpZWFZzYnpGR01FUUdBMVVFQXhNOVFVTWdVbUZwZWlCa1pTQlVaWE4wWlNCVFpXTnlaWFJoY21saElHUmhJRVpoDQplbVZ1WkdFZ1pHOGdSWE4wWVdSdklHUmxJRk5oYnlCUVlYVnNiekNDQWlJd0RRWUpLb1pJaHZjTkFRRUJCUUFEDQpnZ0lQQURDQ0Fnb0NnZ0lCQU5OYmlLZm1rOFZTR0Jsbm8xWHVYNXBoaWx3T3lRVmJyNGZ0c1NGdm92NlFBTC85DQpGSWFwelJEczFWdmNSaFRnQXVnK1Myc3RVRi9iU2dQY2JlOWxTTklmM3gyY09TRUg1ZEtMU2ZEWjVwYUY2U3l2DQppT05rS0lWZE95MG5HcUIvZjdmMzBtZDlMU0YwYk1abzI2bmRPNXViak9NU3ZrcjBzdGp2cXMzR2I2NjRPN3c1DQpnenlRcVVmN1ZKVTJWNXhMNzAvYW9IYmp4UTZZcFlIaDVUOHhlUEV2aUdNeHhobW9jdmVrMGVIbXhaMVpBRndmDQpmbWpacGdtKzNBbWUrQWJ1Z0IxcVlkOTdXQlVjL1I2clYzSFVJaEtMdmswQmMyQk5TQWpKVHNtUlJoNnhiNUVPDQpIV3U4SjlVOTNPVDBtQ0RTL0c0ekFwKzIwVlVaTlN5WHozdkhvdzNWQkE0ck43VUthTVA4U0FGcWJQd2pQaGY2DQpWeUhaSkhGeUlramxVL09lOGk4aFJoZSt1S0luem1kUklna3FqQzRKYlM4L0hKd1pCeWJ1clhtZlZnZ0JyWjcyDQp1SWxIeWZLQWVvZE82K1Vudk9RUTNkUXNLc2hsS2l2dUNKenZZbHBUYW5VbHlUeXJ1d0ZWL00zbHVwVXVsSkJ2DQorRVpuY2J3L0gyT1VGSU95cytmaUlqby9yUCtVVEVuRTBaeExMWWZNSE5Ibm95RkZWWlhXMFlLSVZ2d29VMEgyDQpMNEFlcnlzWWxzNGpHWWp6RXU2TXJoNFl2Sy9Fa2pGQnhseVFxQitrLzZZcHZEUEdBRWNDWExlM0xYZy9GR0RLDQpVdjRSSjRHMXd3WGJDU0lpdStsT3hIQndxa3FjYWo0ZVR4aGRyYXZFZmp4UDk1ZXBCN3A5Z1JXZXhLSWZBZ01CDQpBQUdqZ2dFb01JSUJKREFQQmdOVkhSTUJBZjhFQlRBREFRSC9NSHNHQTFVZElBUjBNSEl3Y0FZSkt3WUJCQUdCDQo3QzBDTUdNd1lRWUlLd1lCQlFVSEFnRVdWV2gwZEhBNkx5OWhZM05oZEMxMFpYTjBaUzVwYlhCeVpXNXpZVzltDQphV05wWVd3dVkyOXRMbUp5TDNKbGNHOXphWFJ2Y21sdkwyUndZeTloWTNObFptRjZjM0F2WkhCalgyRmpjMlZtDQpZWHB6Y0M1d1pHWXdaUVlEVlIwZkJGNHdYREJhb0ZpZ1ZvWlVhSFIwY0RvdkwyRmpjMkYwTFhSbGMzUmxMbWx0DQpjSEpsYm5OaGIyWnBZMmxoYkM1amIyMHVZbkl2Y21Wd2IzTnBkRzl5YVc4dmJHTnlMMkZqYzJWbVlYcHpjQzloDQpZM05sWm1GNmMzQmpjbXd1WTNKc01BNEdBMVVkRHdFQi93UUVBd0lCQmpBZEJnTlZIUTRFRmdRVTFaQ1dxTG9HDQpKWEd2L0gzbDdxTE1FZUNIZHI4d0RRWUpLb1pJaHZjTkFRRU5CUUFEZ2dJQkFFalhiSFhGNGxXVEFDSHJ0MnR3DQoyamRyem5qM1FJdnhNWlBtVVduR0lRRUdJK0Q4SXZRTE1MWDJGd2pERVNkL0JKUXlITHM3Y1AvdDRxeEsyemZIDQo2dldvS1F4cGljQU5CbEhZMEo1ZlZVZ0ptQXR2bWlCbzV5U2FubHN2ek1vZCt3U0pUT2ZEZjBnMktIZmhZMkk2DQpIRGRzcWRoS2M4TFMvWCtBenRiVkVYT1k4c1pIVzhMbU9pOFI0WW9hYmZEY2FDdDBsb2hGQzFmRzV3RHA1OW1tDQpWdDAzTkxZaHZiaTNDdENYRHd1Q3ZmNDhjWmwvb1VWdHFpNHAzbitDSk5qbDN0N0ZBMEZkMGdrVG1wcUtEYnowDQpSbEZtdjUzeVk0cjNpT2NCdU5NZW91RDEvc0QyYkJrU01DU3lFL0pYR3ZQVDBUNjhVYklGTDdHbXExd1h3ckFCDQpsZExyQjJBR0FEbXdXZXc0emxnVjJ1SjNnUkpZL2RSSUVSMVFrSEV6dERRQThnbnFtWkptMVg1WWlBc3hvTkpGDQpBc2ZCNUVURTM5Tk9nMklJcjQ4VzQwSjVOUWRKcGR0bHFSbXAzNjFPUEl5TnpWNGY5NzkxbkZVaGdPOVpkYVJ5DQpoMXk4N3FXSGVJM2ZPS1dGOWdpSjU0NUE5S0gvaWozNnFCWlRoRk9ETE0wRWdRNTRGZ1lCL0pHQ0VrbFBTdkorDQpMYVlDQWZySjNjWFd6K25oTlBMeXhNNUNBT2duVmlGRWdmRU5mRkZvRis4cW1ISU9ENlVYZnA1S1JjSkwzcDhkDQpZUVc2VW9sQ2tpaHUwUzFER2hFa0p6R05WOVd1TUE4T1lWQWtRNDJ0a2VRd1g5NVFRaWNwNFpTaGhyRnBKUVNHDQozSlFMWEdvajc4OXJxR3NqT24xbE1nbzMNCi0tLS0tRU5EIENFUlRJRklDQVRFLS0tLS0=</X509Certificate>
      </X509Data>
    </KeyInfo>
  </Signature>
</CFeCanc>
"""

XML_VENDA_COMPLEXO = """<?xml version="1.0"?>
<CFe>
  <infCFe Id="CFe35150808723218000186599000040190000229554765" versao="0.06" versaoDadosEnt="0.06" versaoSB="010000">
    <ide>
      <cUF>35</cUF>
      <cNF>955476</cNF>
      <mod>59</mod>
      <nserieSAT>900004019</nserieSAT>
      <nCFe>000022</nCFe>
      <dEmi>20150801</dEmi>
      <hEmi>105343</hEmi>
      <cDV>5</cDV>
      <tpAmb>2</tpAmb>
      <CNPJ>16716114000172</CNPJ>
      <signAC>SGR-SAT SISTEMA DE GESTAO E RETAGUARDA DO SAT</signAC>
      <assinaturaQRCODE>eTqMuIx1KqSw2njqW3zks9AGysXa87kItBCrqzdopmhzKDJfA1+zaptvdpBNYBrqvDq9xTTF6cKv5YqtDuOz/6DCyAh/6uMZ9Flhw/5TzZnt0FGtS9TGlkmliyWLo0Vak2p35eHmIUZy1C2+Bb2LkslgVY+sfo5dT3Lx7mWRxSMke1Oz5H53kvR8EjtYUgeZxs7klYDZIH9uAU8ijRCCyeiti7AgEXZBwp5yAwW6OBvcMhyjalxu3f2wVQSEKM/eIU3b8Sz6IHGHh34Cjl/h9Zudx52UZAci4jzPqg2HWMSudArywUZRw/HQUG7ixIu4KQEhhQl/eut5U8zpSU4gEQ==</assinaturaQRCODE>
      <numeroCaixa>123</numeroCaixa>
    </ide>
    <emit>
      <CNPJ>08723218000186</CNPJ>
      <xNome>TANCA INFORMATICA EIRELI</xNome>
      <xFant>TANCA</xFant>
      <enderEmit>
        <xLgr>RUA ENGENHEIRO JORGE OLIVA</xLgr>
        <nro>73</nro>
        <xBairro>VILA MASCOTE</xBairro>
        <xMun>SAO PAULO</xMun>
        <CEP>04362060</CEP>
      </enderEmit>
      <IE>149626224113</IE>
      <IM>123123</IM>
      <cRegTrib>3</cRegTrib>
      <indRatISSQN>N</indRatISSQN>
    </emit>
    <dest/>
    <det nItem="1">
      <prod>
        <cProd>0001</cProd>
        <cEAN>0012345678905</cEAN>
        <xProd>Trib ICMS Integral Aliquota 10.00% - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>47061000</NCM>
        <CFOP>5001</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>100.00</vUnCom>
        <vProd>100.00</vProd>
        <indRegra>A</indRegra>
        <vItem>100.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>1.00</vItem12741>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>00</CST>
            <pICMS>10.00</pICMS>
            <vICMS>10.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="2">
      <prod>
        <cProd>0002</cProd>
        <xProd>Trib ICMS red BC Aliquota 20% - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>48021000</NCM>
        <CFOP>5002</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>20.00</vUnCom>
        <vProd>20.00</vProd>
        <indRegra>A</indRegra>
        <vItem>20.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>2.00</vItem12741>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>20</CST>
            <pICMS>20.00</pICMS>
            <vICMS>4.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="3">
      <prod>
        <cProd>0003</cProd>
        <xProd>Trib ICMS Isento - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>54031000</NCM>
        <CFOP>5003</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>30.00</vUnCom>
        <vProd>30.00</vProd>
        <indRegra>A</indRegra>
        <vItem>30.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>0.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>40</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="4">
      <prod>
        <cProd>0004</cProd>
        <xProd>Trib ICMS N&#xE3;o Tributado - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>55031100</NCM>
        <CFOP>5004</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>40.00</vUnCom>
        <vProd>40.00</vProd>
        <indRegra>A</indRegra>
        <vItem>40.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>0.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>41</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="5">
      <prod>
        <cProd>0005</cProd>
        <xProd>Trib ICMS Susp - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>56031130</NCM>
        <CFOP>5005</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>50.00</vUnCom>
        <vProd>50.00</vProd>
        <indRegra>A</indRegra>
        <vItem>50.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>5.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>50</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="6">
      <prod>
        <cProd>0006</cProd>
        <xProd>Trib ICMS Com Ant por ST - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>57029100</NCM>
        <CFOP>5006</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>60.00</vUnCom>
        <vProd>60.00</vProd>
        <indRegra>A</indRegra>
        <vItem>60.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>6.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>60</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="7">
      <prod>
        <cProd>0007</cProd>
        <xProd>Trib ICMS pelo Simples - PIS e COFINS cod 08 sem incidencia</xProd>
        <NCM>58042990</NCM>
        <CFOP>5007</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>70.00</vUnCom>
        <vProd>70.00</vProd>
        <indRegra>A</indRegra>
        <vItem>70.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>7.00</vItem12741>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>08</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="8">
      <prod>
        <cProd>0011</cProd>
        <xProd>Trib Integral Aliquota 10.00% - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>58081000</NCM>
        <CFOP>5011</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>100.00</vUnCom>
        <vProd>100.00</vProd>
        <indRegra>A</indRegra>
        <vItem>100.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>00</CST>
            <pICMS>10.00</pICMS>
            <vICMS>10.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>100.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>1.50</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>100.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>1.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="9">
      <prod>
        <cProd>0012</cProd>
        <xProd>Trib red BC Aliquota 20%  - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>60019100</NCM>
        <CFOP>5012</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>20.00</vUnCom>
        <vProd>20.00</vProd>
        <indRegra>A</indRegra>
        <vItem>20.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>4.00</vItem12741>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>20</CST>
            <pICMS>20.00</pICMS>
            <vICMS>4.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>20.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>0.30</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>20.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>0.30</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="10">
      <prod>
        <cProd>0013</cProd>
        <xProd>Trib ICMS Isento - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>60052300</NCM>
        <CFOP>5013</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>30.00</vUnCom>
        <vProd>30.00</vProd>
        <indRegra>A</indRegra>
        <vItem>30.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>0.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>40</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>30.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>0.45</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>30.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>0.45</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="11">
      <prod>
        <cProd>0014</cProd>
        <xProd>Trib ICMS N&#xE3;o Tributado - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>61033300</NCM>
        <CFOP>5014</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>40.00</vUnCom>
        <vProd>40.00</vProd>
        <indRegra>A</indRegra>
        <vItem>40.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>0.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>41</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>40.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>0.60</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>40.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>0.60</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="12">
      <prod>
        <cProd>0015</cProd>
        <xProd>Trib ICMS Susp - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>61071200</NCM>
        <CFOP>5015</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>50.00</vUnCom>
        <vProd>50.00</vProd>
        <indRegra>A</indRegra>
        <vItem>50.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>5.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>50</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>50.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>0.75</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>50.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>0.75</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="13">
      <prod>
        <cProd>0016</cProd>
        <xProd>Trib ICMS Com Ant por ST - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>57029100</NCM>
        <CFOP>5016</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>60.00</vUnCom>
        <vProd>60.00</vProd>
        <indRegra>A</indRegra>
        <vItem>60.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>6.00</vItem12741>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>60</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>60.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>0.90</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>60.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>0.90</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="14">
      <prod>
        <cProd>0017</cProd>
        <xProd>Trib ICMS pelo Simples - PIS e COFINS cod 01 aliquota 0.0150</xProd>
        <NCM>58042990</NCM>
        <CFOP>5017</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>70.00</vUnCom>
        <vProd>70.00</vProd>
        <indRegra>A</indRegra>
        <vItem>70.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>01</CST>
            <vBC>70.00</vBC>
            <pPIS>0.0150</pPIS>
            <vPIS>1.05</vPIS>
          </PISAliq>
        </PIS>
        <COFINS>
          <COFINSAliq>
            <CST>01</CST>
            <vBC>70.00</vBC>
            <pCOFINS>0.0150</pCOFINS>
            <vCOFINS>1.05</vCOFINS>
          </COFINSAliq>
        </COFINS>
      </imposto>
    </det>
    <det nItem="15">
      <prod>
        <cProd>0018</cProd>
        <xProd>Trib Integral Aliquota 10.00% - PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>58081000</NCM>
        <CFOP>5018</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>100.00</vUnCom>
        <vProd>100.00</vProd>
        <indRegra>A</indRegra>
        <vItem>100.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>00</CST>
            <pICMS>10.00</pICMS>
            <vICMS>10.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>2.50</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>100.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>2.50</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>2.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>100.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>2.50</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="16">
      <prod>
        <cProd>0019</cProd>
        <xProd>Trib red BC Aliquota 0.20 -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>60019100</NCM>
        <CFOP>5019</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>20.00</vUnCom>
        <vProd>20.00</vProd>
        <indRegra>A</indRegra>
        <vItem>20.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <Orig>0</Orig>
            <CST>20</CST>
            <pICMS>20.00</pICMS>
            <vICMS>4.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>20.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>0.50</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>20.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>0.50</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>20.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>0.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>20.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>0.50</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="17">
      <prod>
        <cProd>0020</cProd>
        <xProd>Trib ICMS Isento -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>60052300</NCM>
        <CFOP>5020</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>30.00</vUnCom>
        <vProd>30.00</vProd>
        <indRegra>A</indRegra>
        <vItem>30.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>40</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>30.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>0.75</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>30.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>0.75</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>30.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>0.75</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>30.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>0.75</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="18">
      <prod>
        <cProd>0021</cProd>
        <xProd>Trib ICMS N&#xE3;o Tributado -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>61033300</NCM>
        <CFOP>5021</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>40.00</vUnCom>
        <vProd>40.00</vProd>
        <indRegra>A</indRegra>
        <vItem>40.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>41</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>40.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>1.00</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>40.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>1.00</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>40.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>1.00</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>40.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>1.00</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="19">
      <prod>
        <cProd>0022</cProd>
        <xProd>Trib ICMS Susp -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>61071200</NCM>
        <CFOP>5022</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>50.00</vUnCom>
        <vProd>50.00</vProd>
        <indRegra>A</indRegra>
        <vItem>50.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>50</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>50.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>1.25</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>50.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>1.25</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>50.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>1.25</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>50.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>1.25</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="20">
      <prod>
        <cProd>0023</cProd>
        <xProd>Trib ICMS Com Ant por ST -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>61124100</NCM>
        <CFOP>5023</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>60.00</vUnCom>
        <vProd>60.00</vProd>
        <indRegra>A</indRegra>
        <vItem>60.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS40>
            <Orig>0</Orig>
            <CST>60</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>60.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>1.50</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>60.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>1.50</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>60.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>1.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>60.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>1.50</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="21">
      <prod>
        <cProd>0024</cProd>
        <xProd>Trib ICMS pelo Simples -  PIS e COFINS ST aliquota 0.0250</xProd>
        <NCM>61149010</NCM>
        <CFOP>5024</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>70.00</vUnCom>
        <vProd>70.00</vProd>
        <indRegra>A</indRegra>
        <vItem>70.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>70.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>1.75</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>70.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>1.75</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>70.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>1.75</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>70.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>1.75</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="22">
      <prod>
        <cProd>0031</cProd>
        <xProd>Trib sem ICMS -  PIS e COFINS ST aliquota 2.5 - ISSQN 3.21</xProd>
        <NCM>62061000</NCM>
        <CFOP>5025</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>100.00</vUnCom>
        <vProd>100.00</vProd>
        <indRegra>A</indRegra>
        <vItem>100.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>1.00</vItem12741>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>2.50</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>100.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>2.50</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>2.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>100.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>2.50</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="23">
      <prod>
        <cProd>0032</cProd>
        <xProd>ISSQN sem cListServ, cServTribMun e cMunFG</xProd>
        <NCM>62061000</NCM>
        <CFOP>5025</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>100.00</vUnCom>
        <vProd>100.00</vProd>
        <indRegra>A</indRegra>
        <vItem>100.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <vItem12741>1.00</vItem12741>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pPIS>0.0250</pPIS>
            <vPIS>2.50</vPIS>
          </PISAliq>
        </PIS>
        <PISST>
          <vBC>100.00</vBC>
          <pPIS>0.0250</pPIS>
          <vPIS>2.50</vPIS>
        </PISST>
        <COFINS>
          <COFINSAliq>
            <CST>02</CST>
            <vBC>100.00</vBC>
            <pCOFINS>0.0250</pCOFINS>
            <vCOFINS>2.50</vCOFINS>
          </COFINSAliq>
        </COFINS>
        <COFINSST>
          <vBC>100.00</vBC>
          <pCOFINS>0.0250</pCOFINS>
          <vCOFINS>2.50</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <det nItem="24">
      <prod>
        <cProd>0025</cProd>
        <xProd>Trib ICMS pelo Simples - PIS e COFINS pelo Simples</xProd>
        <NCM>62061000</NCM>
        <CFOP>5025</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>80.00</vUnCom>
        <vProd>80.00</vProd>
        <indRegra>T</indRegra>
        <vItem>80.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>0</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <det nItem="25">
      <prod>
        <cProd>0026</cProd>
        <xProd>PISQtidade e COFINS Qtidade</xProd>
        <NCM>61071200</NCM>
        <CFOP>5234</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>10.00</vUnCom>
        <vProd>10.00</vProd>
        <indRegra>T</indRegra>
        <vItem>10.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <Orig>8</Orig>
            <CST>90</CST>
            <pICMS>10.00</pICMS>
            <vICMS>1.00</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISQtde>
            <CST>03</CST>
            <qBCProd>1.0000</qBCProd>
            <vAliqProd>0.0200</vAliqProd>
            <vPIS>0.02</vPIS>
          </PISQtde>
        </PIS>
        <COFINS>
          <COFINSQtde>
            <CST>03</CST>
            <qBCProd>1.0000</qBCProd>
            <vAliqProd>0.0200</vAliqProd>
            <vCOFINS>0.02</vCOFINS>
          </COFINSQtde>
        </COFINS>
      </imposto>
    </det>
    <det nItem="26">
      <prod>
        <cProd>0027</cProd>
        <xProd>ICMSOutros PISOutros COFINSOutros</xProd>
        <NCM>61033300</NCM>
        <CFOP>5687</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>10.00</vUnCom>
        <vProd>10.00</vProd>
        <indRegra>A</indRegra>
        <vItem>10.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <Orig>7</Orig>
            <CST>90</CST>
            <pICMS>5.00</pICMS>
            <vICMS>0.50</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="27">
      <prod>
        <cProd>0028</cProd>
        <xProd>ICMS Simples IMUNE PIS e COFINS SN</xProd>
        <NCM>62093000</NCM>
        <CFOP>5375</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>15.00</vUnCom>
        <vProd>15.00</vProd>
        <indRegra>A</indRegra>
        <vItem>15.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>8</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <det nItem="28">
      <prod>
        <cProd>0029</cProd>
        <xProd>Simples Nacional Cobrado Anteriormente</xProd>
        <NCM>62113990</NCM>
        <CFOP>5924</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>20.00</vUnCom>
        <vProd>20.00</vProd>
        <indRegra>A</indRegra>
        <vItem>20.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>8</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <det nItem="29">
      <prod>
        <cProd>0030</cProd>
        <xProd>Simples Nacional Outros</xProd>
        <NCM>62149010</NCM>
        <CFOP>5298</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>23.00</vUnCom>
        <vProd>23.00</vProd>
        <indRegra>T</indRegra>
        <vItem>23.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN900>
            <Orig>7</Orig>
            <CSOSN>900</CSOSN>
            <pICMS>15.00</pICMS>
            <vICMS>3.45</vICMS>
          </ICMSSN900>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSSN>
            <CST>49</CST>
          </COFINSSN>
        </COFINS>
      </imposto>
    </det>
    <det nItem="30">
      <prod>
        <cProd>0008</cProd>
        <xProd>PISOutr Qtdade COFINSOutr Qtdade</xProd>
        <NCM>60019100</NCM>
        <CFOP>5978</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>45.00</vUnCom>
        <vProd>45.00</vProd>
        <indRegra>A</indRegra>
        <vItem>45.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMS40>
            <Orig>7</Orig>
            <CST>41</CST>
          </ICMS40>
        </ICMS>
        <PIS>
          <PISSN>
            <CST>49</CST>
          </PISSN>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>08</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <det nItem="31">
      <prod>
        <cProd>0009</cProd>
        <xProd>ICMS Imune PISST Qtidade COFINSST Qtidade</xProd>
        <NCM>82</NCM>
        <CFOP>5218</CFOP>
        <uCom>kg</uCom>
        <qCom>1.0000</qCom>
        <vUnCom>15.00</vUnCom>
        <vProd>15.00</vProd>
        <indRegra>A</indRegra>
        <vItem>15.00</vItem>
        <vRatDesc>0.00</vRatDesc>
        <vRatAcr>0.00</vRatAcr>
      </prod>
      <imposto>
        <ICMS>
          <ICMSSN102>
            <Orig>6</Orig>
            <CSOSN>500</CSOSN>
          </ICMSSN102>
        </ICMS>
        <PIS>
          <PISQtde>
            <CST>03</CST>
            <qBCProd>1.0000</qBCProd>
            <vAliqProd>0.0500</vAliqProd>
            <vPIS>0.05</vPIS>
          </PISQtde>
        </PIS>
        <PISST>
          <qBCProd>1.0000</qBCProd>
          <vAliqProd>0.0230</vAliqProd>
          <vPIS>0.02</vPIS>
        </PISST>
        <COFINS>
          <COFINSQtde>
            <CST>03</CST>
            <qBCProd>1.0000</qBCProd>
            <vAliqProd>0.0230</vAliqProd>
            <vCOFINS>0.02</vCOFINS>
          </COFINSQtde>
        </COFINS>
        <COFINSST>
          <qBCProd>1.0000</qBCProd>
          <vAliqProd>0.0230</vAliqProd>
          <vCOFINS>0.02</vCOFINS>
        </COFINSST>
      </imposto>
    </det>
    <total>
      <ICMSTot>
        <vICMS>46.95</vICMS>
        <vProd>1528.00</vProd>
        <vDesc>0.00</vDesc>
        <vPIS>19.87</vPIS>
        <vCOFINS>19.84</vCOFINS>
        <vPISST>14.27</vPISST>
        <vCOFINSST>14.27</vCOFINSST>
        <vOutro>0.00</vOutro>
      </ICMSTot>
      <vCFe>1528.00</vCFe>
    </total>
    <pgto>
      <MP>
        <cMP>01</cMP>
        <vMP>900.00</vMP>
      </MP>
      <MP>
        <cMP>02</cMP>
        <vMP>300.00</vMP>
      </MP>
      <MP>
        <cMP>03</cMP>
        <vMP>150.00</vMP>
        <cAdmC>004</cAdmC>
      </MP>
      <MP>
        <cMP>13</cMP>
        <vMP>150.00</vMP>
      </MP>
      <MP>
        <cMP>04</cMP>
        <vMP>150.00</vMP>
        <cAdmC>003</cAdmC>
      </MP>
      <MP>
        <cMP>04</cMP>
        <vMP>300.00</vMP>
      </MP>
      <MP>
        <cMP>05</cMP>
        <vMP>5.00</vMP>
      </MP>
      <MP>
        <cMP>10</cMP>
        <vMP>5.00</vMP>
      </MP>
      <MP>
        <cMP>11</cMP>
        <vMP>5.00</vMP>
      </MP>
      <MP>
        <cMP>12</cMP>
        <vMP>5.00</vMP>
      </MP>
      <vTroco>442.00</vTroco>
    </pgto>
    <infAdic>
      <obsFisco xCampo="xCampo1">
        <xTexto>xTexto1</xTexto>
      </obsFisco>
    </infAdic>
  </infCFe>
  <Signature xmlns="http://www.w3.org/2000/09/xmldsig#">
    <SignedInfo>
      <CanonicalizationMethod Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
      <SignatureMethod Algorithm="http://www.w3.org/2001/04/xmldsig-more#rsa-sha256"/>
      <Reference URI="#CFe35150808723218000186599000040190000229554765">
        <Transforms>
          <Transform Algorithm="http://www.w3.org/2000/09/xmldsig#enveloped-signature"/>
          <Transform Algorithm="http://www.w3.org/TR/2001/REC-xml-c14n-20010315"/>
        </Transforms>
        <DigestMethod Algorithm="http://www.w3.org/2001/04/xmlenc#sha256"/>
        <DigestValue>KexY2o0wqEon1wR5sVPdvSCvsTJuoKhOYcLOelcP2xY=</DigestValue>
      </Reference>
    </SignedInfo>
    <SignatureValue>bdDf8FDmGtpBBfYbsH+QeBiOkUtWUg9Y7v4+GOGzo8U9ynb7XL/Zc05knq5kz9LZQaS65p3SoaU4uPQ8cNIwlN2OcWRhDgLO7oogVD4g7LIbKVRdQ9bAvReSCsJgraSvk3I/aV5d/bV/jbZYTPALmvp8NafalemUehCexmSVFRkUmH26Qo+Z0kcVrx1NYbxRyKSSaTMER5Ura6Xn0jJqaX+fIeZ0q94CNut7O0PjR9sPi/5VrBUyBqEITAG3oJ+x6m4usUx+TtnD3e7fCOhKzJQtL6cP0eDoV354Mkrpu0QlttBlKkQ0S95NOqcqYQmH4XOiQbg4iILz3YIhMr5YaA==</SignatureValue>
    <KeyInfo>
      <X509Data>
        <X509Certificate>MIIGsDCCBJigAwIBAgIJARjgvIzmd2BGMA0GCSqGSIb3DQEBCwUAMGcxCzAJBgNVBAYTAkJSMTUwMwYDVQQKEyxTZWNyZXRhcmlhIGRhIEZhemVuZGEgZG8gRXN0YWRvIGRlIFNhbyBQYXVsbzEhMB8GA1UEAxMYQUMgU0FUIGRlIFRlc3RlIFNFRkFaIFNQMB4XDTE1MDcwODE1MzYzNloXDTIwMDcwODE1MzYzNlowgbUxEjAQBgNVBAUTCTkwMDAwNDAxOTELMAkGA1UEBhMCQlIxEjAQBgNVBAgTCVNBTyBQQVVMTzERMA8GA1UEChMIU0VGQVotU1AxDzANBgNVBAsTBkFDLVNBVDEoMCYGA1UECxMfQXV0ZW50aWNhZG8gcG9yIEFSIFNFRkFaIFNQIFNBVDEwMC4GA1UEAxMnVEFOQ0EgSU5GT1JNQVRJQ0EgRUlSRUxJOjA4NzIzMjE4MDAwMTg2MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAl89PfjfjZy0QatgBzvV+Du04ekjbiYmnVe5S9AHNiexno8Vdp9B79hwLKiDrvvwAtVqrocWOQmM3SIx5OECy/vvFi46wawJT9Y2a4zuEFGvHZSuE/Up3PB52dP34aGbplis0d1RqIoXoKWq+FljWs+N89rwvPxgJGafGp3e3t8CqIjqBPSCX8Bmy/2YDj1C/J1CLW91q94qVX0CxhKFHAwfgIKe7ZHeZpws2jiOmtLFWKofCSaconQu5PHUVzOv7kTpK8ZbvsvnzwLwHa6/rDJsORW/33V+ryfuDtRH+nos3usE/avc/8mU25q3rj7fTNax4ggb6rpFtSyTAWRkFZQIDAQABo4ICDjCCAgowDgYDVR0PAQH/BAQDAgXgMHsGA1UdIAR0MHIwcAYJKwYBBAGB7C0DMGMwYQYIKwYBBQUHAgEWVWh0dHA6Ly9hY3NhdC5pbXByZW5zYW9maWNpYWwuY29tLmJyL3JlcG9zaXRvcmlvL2RwYy9hY3NhdHNlZmF6c3AvZHBjX2Fjc2F0c2VmYXpzcC5wZGYwawYDVR0fBGQwYjBgoF6gXIZaaHR0cDovL2Fjc2F0LXRlc3RlLmltcHJlbnNhb2ZpY2lhbC5jb20uYnIvcmVwb3NpdG9yaW8vbGNyL2Fjc2F0c2VmYXpzcC9hY3NhdHNlZmF6c3BjcmwuY3JsMIGmBggrBgEFBQcBAQSBmTCBljA0BggrBgEFBQcwAYYoaHR0cDovL29jc3AtcGlsb3QuaW1wcmVuc2FvZmljaWFsLmNvbS5icjBeBggrBgEFBQcwAoZSaHR0cDovL2Fjc2F0LXRlc3RlLmltcHJlbnNhb2ZpY2lhbC5jb20uYnIvcmVwb3NpdG9yaW8vY2VydGlmaWNhZG9zL2Fjc2F0LXRlc3RlLnA3YzATBgNVHSUEDDAKBggrBgEFBQcDAjAJBgNVHRMEAjAAMCQGA1UdEQQdMBugGQYFYEwBAwOgEAQOMDg3MjMyMTgwMDAxODYwHwYDVR0jBBgwFoAUjjlBAFzyuAXaqG2YuQFGbW5j3wIwDQYJKoZIhvcNAQELBQADggIBAEmyNu2JbRf7geMopWPAWgaspxVOCQz56P/iA0xWmEpeayPjSzPNFr79FpEHEF5by4it0xiHj3cZmXnmkTNVDXSx03C1SNOBy6p9p5ps8bvSMlYVmiyr5C7sjp9AcvS92BXekNazcr/cHsTUmlGTHZRmwWYkdNzaVLMgQJ5RyLnWPyacP6KMuuU+y1SjgrKHcseaw987NHO2q/fCRL5Lgg/O6aA2sFP/QMO3WuAEzIBPT0k9g80L4DnnZBInyU5jdGB6/CvZhd7lau6ncQZPl4cnr+Y6Dr4TZ1ytA/Mpf2/MJjW8w5XqtatgRCl3DZ7W7D5ThxIW7oBnNbtkjvokH38OSQJg+Fvtd7Ab6b0o8RDyxVjUi5Kla+4CAxZs10vyW4BkD7fFktiTzSPsyStqbinsWiPW/XzNmlmCX+PDsQmkaziox4MHQ2XPFRngBLLjZOBWTNdMPo+zDTyfG9jVAeLEr4vtY/zRITP5I5Gk7c0VGi7uUUgqsqdluH+ygHqs52lNo1oxLYmODUFq1xejgmGu4CMcJhz3RuFjXDX6BUc0U0cJbvtzETKq5psOYklZmA4nSHeWE4p5xI1o0/8DKEfEs4GtImIBYPubUSLEoGFnDF45PeQU7cI+yMIYrct5Czn0M52l/77anc+9NyIGi+lCVW/IHfEZawYziMiUUiBx</X509Certificate>
      </X509Data>
    </KeyInfo>
  </Signature>
</CFe>
"""
