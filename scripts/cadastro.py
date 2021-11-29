from fiscal.models import *
from cadastro.models import *
from prod.models import *
from comercial.models import *

def __init__(self):
    
    #cadastro do cliente
    cli = Parceiro()
    cli.tipo_id = 1
    cli.pessoa_choices = 'J'
    cli.pessoa = '2'
    cli.nome = 'Cliente teste'
    #docs pj
    cli.cnpj = '04.408.568/0001-05'
    insc_est = '0500054564'
    #endereco
    cli.logradouro = 'João Prancuti'
    cli.numero = '88'
    cli.complemento = 'Pav. 2'
    cli.bairro = 'Brasília'
    cli.cep = '95720-000'
    cli.estado = 'RS'
    cli.cidade = 'Garibaldi'
    #Contato
    cli.fone1 = '54 3463 8222'
    cli.email_nfe = 'nfe@defer.com.br'
    
    obj, created = Parceiro.objects.update_or_create(cnpj = '04.408.568/0001-05', defaults=cli)
    
    return obj