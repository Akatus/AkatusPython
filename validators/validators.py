# -*- coding: utf-8 -*-

import inspect


def check_parameters(f):
    errors = dict(ambiente="um ambiente",
                  token="o token",
                  email="o e-mail",
                  codigo="o codigo",
                  descricao="uma descricao",
                  quantidade="uma quantidade",
                  preco="um preco",
                  peso="um peso",
                  frete="um frete",
                  referencia="uma referencia",
                  num_tel="o número de telefone",
                  tel_tipo="o tipo de telefone",
                  desconto="um desconto")
    
    def wrapper(*a, **k):
        d = inspect.getcallargs(f, *a, **k)
        for field, value in d.iteritems(): 
            if not value:
                raise ValueError("Voce deve informar %s" %errors[field])
        
        return f(*a, **k)
    return wrapper
            

    


class Validators():

    def email(self, email, error_message='E-mail invalido'):
        
        """
        >>> v = Validators()
        
        >>> v.email('ihercowitz@gmail.com')
        True
        >>> v.email('')
        Traceback (most recent call last):
        ValueError: E-mail invalido
        
        >>> v.email('a@a.com')
        Traceback (most recent call last):
        ValueError: E-mail invalido
        
        >>> v.email('aa@ig.com')
        Traceback (most recent call last):
        ValueError: E-mail invalido

        >>> v.email('ihf@ig.com')
        True
        
        >>> v.email('i.hercowitz@gmail.com')
        True
        
        >>> v.email('.hercowitz@gmail.com')
        Traceback (most recent call last):
        ValueError: E-mail invalido
        
        >>> v.email('i..hercowitz@gmail.com')
        Traceback (most recent call last):
        ValueError: E-mail invalido
               
        """
        import re
        
        #Valida se o email tem pelo menos 3 caracteres antes do @ + 2 caracteres apos e pelo menos 2 caracteres depois do ., sendo esses ultimos somente letras    
        if re.match(r'^((?!\.)([a-z0-9_]|(?<!\.)\.){3,}@[0-9a-zA-Z]+[0-9,a-z,A-Z,.,-]*(.){1}[a-zA-Z]{2,4})+$', email, re.IGNORECASE) :
            return True         
        else:
            raise ValueError(error_message)
    
    
if __name__ == '__main__':
    import doctest
    doctest.testmod()
    
    