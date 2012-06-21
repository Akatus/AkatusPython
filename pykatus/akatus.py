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
        
        carrinho       = self.carrinho
        recebedor      = etree.SubElement(carrinho, "recebedor")
        api_key        = etree.SubElement(recebedor, "api_key")
        api_key.text   = token
        email_tag      = etree.SubElement(recebedor, "email")
        email_tag.text = email
        
        return self
    
    def set_pagador(self,nome, email):
        if not nome:
            raise ValueError("Você deve definir o nome do pagador")
        if not email:
            raise ValueError("Você deve definir o email do pagador")
        
        carrinho        = self.carrinho
        pagador         = etree.SubElement(carrinho, "pagador")
        nome_tag        = etree.SubElement(pagador, "nome")
        nome_tag.text   =  nome
        email_tag       = etree.SubElement(pagador, "email")
        email_tag.text  = email
        
        return self
    
    
    def set_tel_pagador(self,tipo, numero):
        if not tipo:
            raise ValueError("Você deve definir um tipo de telefone")
        if not numero:
            raise ValueError("Você deve passar um número de telefone")
        
        pagador         = self.carrinho[1]
        telefones       = etree.SubElement(pagador, "telefones")
        telefone        = etree.SubElement(telefones, "telefone")
        tipo_tag        = etree.SubElement(telefone, "tipo")
        tipo_tag.text   = tipo
        numero_tag      = etree.SubElement(telefone, "numero")
        numero_tag.text = numero
        
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
        produtos            = etree.SubElement(carrinho, "produtos")
        produto             = etree.SubElement(produtos, "produto")
        codigo_tag          = etree.SubElement(produto, "codigo")
        codigo_tag.text     = codigo
        descricao_tag       = etree.SubElement(produto, "descricao")
        descricao_tag.text  = descricao
        quantidade_tag      = etree.SubElement(produto, "quantidade")
        quantidade_tag.text = quantidade
        preco_tag           = etree.SubElement(produto, "preco")
        preco_tag.text      = preco
        peso_tag            = etree.SubElement(produto, "peso")
        peso_tag.text       = peso
        frete_tag           = etree.SubElement(produto, "frete")
        frete_tag.text      = frete
        desconto_tag        = etree.SubElement(produto, "desconto")
        desconto_tag.text   = desconto
        
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
        
        carrinho                    = self.carrinho
        transacao                   = etree.SubElement(carrinho, "transacao")
        desconto_total_tag          = etree.SubElement(transacao, "desconto_total")
        desconto_total_tag.text     = desconto_total
        peso_total_tag              = etree.SubElement(transacao, "peso_total")
        peso_total_tag.text         = peso_total
        frete_total_tag             = etree.SubElement(transacao, "frete_total")
        frete_total_tag.text        = frete_total
        moeda_tag                   = etree.SubElement(transacao, "moeda")
        moeda_tag.text              = moeda
        referencia_tag              = etree.SubElement(transacao, "referencia")
        referencia_tag.text         = referencia
        meio_de_pagamento_tag       = etree.SubElement(transacao, "meio_de_pagamento")
        meio_de_pagamento_tag.text  = meio_de_pagamento
        
        return self
    
    
    def _get_xml(self):
        return etree.tostring(self.carrinho)
    
    
    def envia(self):
        
        resposta = RespostaAkatus()
        
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.USERAGENT, "Mozilla/4.0")
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        curl.setopt(pycurl.POSTFIELDS, self.__get_xml())
        curl.setopt(pycurl.WRITEFUNCTION, resposta.__callback)
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
        
    def __callback(self, buff):
        self.conteudo = buff
