#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pycurl

from lxml import etree
from validators import Validators, check_parameters


class Akatus():
    
    def __init__(self, xml_node = "carrinho", namespace = "http://connect.akatus.com/"):
        self.validators = Validators()
        
        if xml_node:
            self.xml_node = etree.Element(xml_node, xmlns=namespace)
        
    def monta_xml(self, parent, **kwargs):
        if isinstance(parent, etree._Element):
            node_parent = parent
        else:
            node_parent = etree.Element(parent)
        
        for k,v in kwargs.items():
            node = etree.SubElement(node_parent, k)
            if isinstance(v, dict):
                self.monta_xml(node, **v)
            else:
                node.text = v
                
        return node_parent
    
    
    @check_parameters
    def set_ambiente(self,ambiente):
        ambientes = dict(sandbox="dev", producao="www")
        
        try:
            self.url = "https://%s.akatus.com/api/v1/carrinho.xml" %ambientes[ambiente]
        except KeyError:
            raise ValueError("O ambiente escolhido é inválido")
        
            
    @check_parameters
    def set_recebedor(self,token, email):
        
        self.validators.email(email)
        
        self.monta_xml(self.xml_node, recebedor=dict(api_key=token,email=email))

        return self
    
    
    @check_parameters
    def set_pagador(self,nome, email, tipo_tel, num_tel):
        
        self.validators.email(email)
        
        self.monta_xml(self.xml_node, pagador=dict(nome=nome, email=email, telefones=dict(
                                                                                          telefone=dict(
                                                                                                        tipo=tipo_tel,
                                                                                                        numero=num_tel))))
        
        return self
    
    
    @check_parameters
    def set_produto(self,codigo, descricao, quantidade, preco, peso, frete, desconto):
        
        self.monta_xml(self.xml_node, produtos=dict(produto=dict(codigo=codigo,
                                                                             descricao=descricao,
                                                                             quantidade=quantidade,
                                                                             preco=preco,
                                                                             peso=peso,
                                                                             frete=frete,
                                                                             desconto=desconto)))
                    
        return self
    
    
    @check_parameters
    def set_transacao(self, desconto_total, peso_total, frete_total, moeda, referencia, meio_de_pagamento):
        
        self.monta_xml(self.xml_node, transacao=dict(desconto_total=desconto_total,
                                                     peso_total=peso_total,
                                                     frete_total=frete_total,
                                                     moeda=moeda,
                                                     referencia=referencia,
                                                     meio_de_pagamento=meio_de_pagamento))
        
        return self
    
    
    def _get_xml(self):
        return etree.tostring(self.xml_node)
    
    
    def envia(self):
        
        xmlbase = open("test/xmlschema.xsd","r")
        
        xmlparser   = etree.parse(xmlbase)
        xmlschema   = etree.XMLSchema(xmlparser)
        
        xml_enviado = etree.fromstring(self._get_xml())
        
        if not xmlschema.validate(xml_enviado):
            raise ValueError(xmlschema.error_log)
        
        resposta = RespostaAkatus()
        
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, self.url)
        curl.setopt(pycurl.USERAGENT, "Mozilla/4.0")
        curl.setopt(pycurl.POST, True)
        curl.setopt(pycurl.SSL_VERIFYPEER, False)
        curl.setopt(pycurl.POSTFIELDS, self._get_xml())
        curl.setopt(pycurl.WRITEFUNCTION, resposta._callback)
        curl.perform()
        curl.close
        
        self.retorno = resposta.conteudo
        return self
    
    def get_resposta(self):
        
        resposta = etree.XML(self.retorno)
        
        if resposta[0].tag == 'status':
            return {resposta[0].tag:resposta[0].text, resposta[1].tag:resposta[1].text}
        
        return {resposta[0].tag:resposta[0].text,resposta[1].tag:resposta[1].text, resposta[2].tag:resposta[2].text,resposta[3].tag:resposta[3].text} 
    
    
class RespostaAkatus:
    def __init__(self):
        self.conteudo = ""
        
    def _callback(self, buff):
        self.conteudo = buff
