Módulo Akatus para integração com Python
==========================================

Author: Alê Borba

Version: v0.0.1

Como usar
-------------------------

from pykatus import Akatus

akatus = Akatus()

akatus.set_ambiente("sandbox")
akatus.set_recebedor("29D4EB49-735E-429D-A5C3-B19DF50ADC47", "aa.borba@yahoo.com.br")
akatus.set_pagador("Alexandre", "alexandre.borba@imasters.com.br")
akatus.set_tel_pagador("residencial","1156321478")
akatus.set_produto("UFC153", "Cueca Velha", "2", "10.00", "2.00", "0.00", "0.00")
akatus.set_transacao("0.00", "4.00", "0.00", "BRL", "cuecanova", "boleto")

akatus.envia()

print akatus.get_resposta()

ToDo
----------------
* Validar campos
* Tratar erros
* Fazer testes automatizados
* Opção de incluir mais de um produto
