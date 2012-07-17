#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Modulo de Integracao com a API Akatus"""

import pycurl

from lxml import etree
from validators import Validators, check_parameters
from urllib2 import urlopen


class Akatus():
    """Classe que trata toda a coleta de dados e envio para a API"""
    
    def __init__(self, xml_node = "carrinho", namespace = "http://connect.akatus.com/"):
        """Metodo construtor que recebe o nome do node pai do XML de envio
        e o namespace para a validacao no XML Schema"""
        
        self.validators = Validators()
        
        if xml_node:
            self.xml_node = etree.Element(xml_node, xmlns=namespace)
        
    def _monta_xml(self, parent, unique=False, **kwargs):
        """Metodo interno que monta o XML utilizando os parametros passados
        por outros metodos."""
        
        if isinstance(parent, etree._Element):
            node_parent = parent
        else:
            node_parent = etree.Element(parent)
        
        for k,v in kwargs.items():
            if unique and node_parent.find(k) is not None:
                node = node_parent.find(k) 
            else:
                node = etree.SubElement(node_parent, k)
               
            if isinstance(v, dict):
                self._monta_xml(node, **v)
            else:
                node.text = v
                
        return node_parent
    
    
    @check_parameters
    def set_ambiente(self,ambiente):
        """Metodo que define qual o ambiente sera usado, as opcoes
        sao: 'sandbox' ou 'producao' """
        
        ambientes = dict(sandbox="dev", producao="www")
        
        try:
            self.url = "https://%s.akatus.com/api/v1/carrinho.xml" %ambientes[ambiente]
        except KeyError:
            raise ValueError("O ambiente escolhido é inválido")
        
            
    @check_parameters
    def set_recebedor(self,token, email):
        """Metodo que insere no XML as informacoes do recebedor que constam na
        conta cadastrada na Akatus"""
        
        self.validators.email(email)
        
        self._monta_xml(self.xml_node, recebedor=dict(api_key=token,email=email))

        return self
    
    
    @check_parameters
    def set_pagador(self,nome, email, tipo_tel, num_tel):
        """Metodo que insere no XML as informacoes obrigatorias da pessoa que efetuara o pagamento"""
        
        self.validators.email(email)
        
        self._monta_xml(self.xml_node, pagador=dict(nome=nome, email=email, telefones=dict(
                                                                                          telefone=dict(
                                                                                                        tipo=tipo_tel,
                                                                                                        numero=num_tel))))
        
        return self
    
    
    @check_parameters
    def set_produto(self,codigo, descricao, quantidade, preco, peso, frete, desconto):
        """Metodo que insere no XML as informacoes do produto comprado. A cada nova iteracao
        deste metodo, um produto novo é adicionado ao XML"""
        
        self._monta_xml(self.xml_node, unique=True, produtos=dict(produto=dict(codigo=codigo,
                                                                             descricao=descricao,
                                                                             quantidade=quantidade,
                                                                             preco=preco,
                                                                             peso=peso,
                                                                             frete=frete,
                                                                             desconto=desconto)))
                    
        return self
    
    
    @check_parameters
    def set_transacao(self, desconto_total, peso_total, frete_total, moeda, referencia, meio_de_pagamento):
        """Metodo que insere no XML as informacoes a respeito da transacao"""
        
        self._monta_xml(self.xml_node, transacao=dict(desconto_total=desconto_total,
                                                     peso_total=peso_total,
                                                     frete_total=frete_total,
                                                     moeda=moeda,
                                                     referencia=referencia,
                                                     meio_de_pagamento=meio_de_pagamento))
        
        return self
    
    
    def _get_xml(self):
        """Metodo interno que retorna o objeto etree em formato string"""
        
        return etree.tostring(self.xml_node)
    
    
    def envia(self):
        """Metodo que faz a validacao do XML usando um XML Schema e envia os dados para 
        o sistema Akatus."""
        
        xmlbase = urlopen("https://raw.github.com/Akatus/AkatusXMLSchema/master/cart.xsd")
        
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
        """Metodo que retorna a resposta da API Akatus depois do envio dos dados."""
        
        resposta = etree.XML(self.retorno)
        
        if resposta[0].tag == 'status':
            return {resposta[0].tag:resposta[0].text, resposta[1].tag:resposta[1].text}
        
        return {resposta[0].tag:resposta[0].text,resposta[1].tag:resposta[1].text, resposta[2].tag:resposta[2].text,resposta[3].tag:resposta[3].text} 
    
    
class RespostaAkatus:
    """Classe que captura a resposta da API Akatus."""
    
    def __init__(self):
        self.conteudo = ""
        
    def _callback(self, buff):
        self.conteudo = buff
