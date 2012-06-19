#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl

from lxml import etree

class Akatus():
    
    def __init__(self):
        carrinho = etree.Element("carrinho")
        self.carrinho = carrinho
        
    
    def set_ambiente(self,ambiente):
        if not ambiente:
            raise ValueError("Você deve definir um ambiente")
        
        if ambiente == "sandbox":
            self.url = "https://dev.akatus.com/api/v1/carrinho.xml"
            
        if ambiente == "producao":
            self.url = "https://www.akatus.com/api/v1/carrinho.xml"

            
    
    def set_recebedor(self,token, email):
        if not token:
            raise ValueError("Você deve definir o token")
        if not email:
            raise ValueError("Você deve definir o email")
        
        carrinho        = self.carrinho
        _recebedor      = etree.SubElement(carrinho, "recebedor")
        _api_key        = etree.SubElement(_recebedor, "api_key")
        _api_key.text   = token
        _email          = etree.SubElement(_recebedor, "email")
        _email.text     = email
        
        return self
    
    def set_pagador(self,nome, email):
        if not nome:
            raise ValueError("Você deve definir o nome do pagador")
        if not email:
            raise ValueError("Você deve definir o email do pagador")
        
        carrinho    = self.carrinho
        _pagador    = etree.SubElement(carrinho, "pagador")
        _nome       = etree.SubElement(_pagador, "nome")
        _nome.text  = nome
        _email      = etree.SubElement(_pagador, "email")
        _email.text = email
        
        return self
    
    
    def set_tel_pagador(self,tipo, numero):
        if not tipo:
            raise ValueError("Você deve definir um tipo de telefone")
        if not numero:
            raise ValueError("Você deve passar um número de telefone")
        
        pagador         = self.carrinho[1]
        _telefones      = etree.SubElement(pagador, "telefones")
        _telefone       = etree.SubElement(_telefones, "telefone")
        _tipo           = etree.SubElement(_telefone, "tipo")
        _tipo.text      = tipo
        _numero         = etree.SubElement(_telefone, "numero")
        _numero.text    = numero
        
        return self
    
    def set_produto(self,codigo, descricao, quantidade, preco, peso, frete, desconto):
        if not codigo:
            raise ValueError("Você deve definir um código")
        if not descricao:
            raise ValueError("Você deve definir uma descrição")
        if not quantidade:
            raise ValueError("Você deve definir uma quantidade")
        if not preco:
            raise ValueError("Você deve definir um preco")
        if not peso:
            raise ValueError("Você deve definir um peso")
        if not frete:
            raise ValueError("Você deve definir um frete")
        if not desconto:
            raise ValueError("Você deve definir um desconto")
        
        carrinho            = self.carrinho
        _produtos           = etree.SubElement(carrinho, "produtos")
        _produto            = etree.SubElement(_produtos, "produto")
        _codigo             = etree.SubElement(_produto, "codigo")
        _codigo.text        = codigo
        _descricao          = etree.SubElement(_produto, "descricao")
        _descricao.text     = descricao
        _quantidade         = etree.SubElement(_produto, "quantidade")
        _quantidade.text    = quantidade
        _preco              = etree.SubElement(_produto, "preco")
        _preco.text         = preco
        _peso               = etree.SubElement(_produto, "peso")
        _peso.text          = peso
        _frete              = etree.SubElement(_produto, "frete")
        _frete.text         = frete
        _desconto           = etree.SubElement(_produto, "desconto")
        _desconto.text      = desconto
        
        return self
    
    
    def set_transacao(self, desconto_total, peso_total, frete_total, moeda, referencia, meio_de_pagamento):
        if not desconto_total:
            raise ValueError("Você deve definir o desconto total")
        if not peso_total:
            raise ValueError("Você deve definir o peso total")
        if not frete_total:
            raise ValueError("Você deve definir o frete total")
        if not moeda:
            raise ValueError("Você deve definir a moeda")
        if not referencia:
            raise ValueError("Você deve definir a referencia")
        if not meio_de_pagamento:
            raise ValueError("Você deve definir um meio de pagamento")
        
        carrinho                = self.carrinho
        _transacao              = etree.SubElement(carrinho, "transacao")
        _desconto_total         = etree.SubElement(_transacao, "desconto_total")
        _desconto_total.text    = desconto_total
        _peso_total             = etree.SubElement(_transacao, "peso_total")
        _peso_total.text        = peso_total
        _frete_total            = etree.SubElement(_transacao, "frete_total")
        _frete_total.text       = frete_total
        _moeda                  = etree.SubElement(_transacao, "moeda")
        _moeda.text             = moeda
        _referencia             = etree.SubElement(_transacao, "referencia")
        _referencia.text        = referencia
        _meio_de_pagamento      = etree.SubElement(_transacao, "meio_de_pagamento")
        _meio_de_pagamento.text = meio_de_pagamento
        
        return self
    
    
    def get_xml(self):
        return etree.tostring(self.carrinho)
    
    
    def envia(self):
        
        resposta = RespostaAkatus()
        
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.USERAGENT, "Mozilla/4.0")
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        curl.setopt(pycurl.POSTFIELDS, self.get_xml())
        curl.setopt(pycurl.WRITEFUNCTION, resposta.callback)
        curl.perform()
        curl.close
        
        self.retorno = resposta.conteudo
        return self
    
    def get_resposta(self):
        
        resposta = etree.XML(self.retorno)
        
        return {'carrinho':resposta[0].text,'status':resposta[1].text, 'transacao':resposta[2].text,'url_retorno':resposta[3].text} 
    
    
class RespostaAkatus:
    def __init__(self):
        self.conteudo = ""
        
    def callback(self, buff):
        self.conteudo = buff
