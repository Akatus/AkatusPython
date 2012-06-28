#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pykatus import Akatus
from lxml import etree
from lxml import objectify

class AkatusTest(unittest.TestCase):
    
    def setUp(self):
        self.akatus = Akatus()
        self.akatus.set_ambiente("sandbox")
        self.akatus.set_recebedor("29D4EB49-735E-429D-A5C3-B19DF50ADC47", "aa.borba@yahoo.com.br")
        self.akatus.set_pagador("Alexandre", "alexandre.borba@imasters.com.br", "residencial", "1156321478")
        self.akatus.set_produto("UFC153", "Cueca Velha", "2", "10.00", "2.00", "0.00", "0.00")
        self.akatus.set_transacao("0.00", "4.00", "0.00", "BRL", "cuecanova", "boleto")
        
    def test_ambiente_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_ambiente,ambiente='')
        
    def test_recebedor_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_recebedor,token='', email='')
        
    def test_pagador_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_pagador,nome='', email='', tipo_tel='', num_tel='')
        
    def test_produto_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_produto,codigo='', descricao='', quantidade='', preco='', peso='', frete='', desconto='')
        
    def test_trasacao_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_transacao,desconto_total='', peso_total='', frete_total='', moeda='', referencia='', meio_de_pagamento='')
        
    def test_xml(self):
        xml_valid = '''
        <carrinho>
            <recebedor>
                <api_key>29D4EB49-735E-429D-A5C3-B19DF50ADC47</api_key>
                <email>aa.borba@yahoo.com.br</email>
            </recebedor>
            <pagador>
                <telefones>
                    <telefone>
                        <tipo>residencial</tipo>
                        <numero>1156321478</numero>
                    </telefone>
                </telefones>
                <email>alexandre.borba@imasters.com.br</email>
                <nome>Alexandre</nome>
            </pagador>
            <produtos>
                <produto>
                    <quantidade>2</quantidade>
                    <peso>2.00</peso>
                    <frete>0.00</frete>
                    <preco>10.00</preco>
                    <codigo>UFC153</codigo>
                    <descricao>Cueca Velha</descricao>
                    <desconto>0.00</desconto>
                </produto>
            </produtos>
            <transacao>
                <referencia>cuecanova</referencia>
                <meio_de_pagamento>boleto</meio_de_pagamento>
                <desconto_total>0.00</desconto_total>
                <peso_total>4.00</peso_total>
                <frete_total>0.00</frete_total>
                <moeda>BRL</moeda>
            </transacao>
        </carrinho>
        '''
        
        obj_xml_e   = objectify.fromstring(xml_valid)
        xml_expect  = etree.tostring(obj_xml_e)
        
        obj_xml_t   = objectify.fromstring(self.akatus._get_xml())
        xml_test    = etree.tostring(obj_xml_t)
        
        self.assertEquals(xml_expect,xml_test)
        
if __name__== '__main__':
    unittest.main()