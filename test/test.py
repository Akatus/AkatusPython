#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from pykatus import Akatus

class AkatusTest(unittest.TestCase):
    
    def setUp(self):
        self.akatus = Akatus()
        self.akatus.set_ambiente("sandbox")
        self.akatus.set_recebedor("29D4EB49-735E-429D-A5C3-B19DF50ADC47", "aa.borba@yahoo.com.br")
        self.akatus.set_pagador("Alexandre", "alexandre.borba@imasters.com.br")
        self.akatus.set_tel_pagador("residencial","1156321478")
        self.akatus.set_produto("UFC153", "Cueca Velha", "2", "10.00", "2.00", "0.00", "0.00")
        self.akatus.set_transacao("0.00", "4.00", "0.00", "BRL", "cuecanova", "boleto")
        
    def test_ambiente_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_ambiente,ambiente='')
        
    def test_recebedor_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_recebedor,token='', email='')
        
    def test_pagador_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_pagador,nome='', email='')
        
    def test_tel_pagador_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_tel_pagador,tipo='', numero='')
        
    def test_produto_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_produto,codigo='', descricao='', quantidade='', preco='', peso='', frete='', desconto='')
        
    def test_trasacao_is_none(self):
        self.assertRaises(ValueError, self.akatus.set_transacao,desconto_total='', peso_total='', frete_total='', moeda='', referencia='', meio_de_pagamento='')
        
if __name__== '__main__':
    unittest.main()