import requests, json
from .models import Municipio, Estado
from django.db.models import Q

def get_munis(estado):
    url = 'https://servicodados.ibge.gov.br/api/v1/localidades/estados/{}/municipios'.format(estado)
    m = requests.get(url)
    munis = json.loads(m.content)
    return munis

def get_estados():
    url ='https://servicodados.ibge.gov.br/api/v1/localidades/estados'
    e = requests.get(url)
    est = json.loads(e.content)
    return est 

def lista_munis():
    estados = get_estados()
    lst_munis=[]
    
    for estado in estados:
        #lista_estados.append(str(estado['id']) + ' ' + estado['sigla'] + ' ' + estado['nome'] )
        munis = get_munis(str(estado['id']))
        E = Estado(
                    cod = estado['id'],
                    sigla = estado['sigla'],
                    nome = estado['nome'],
                    )
        E.save()
        
        for muni in munis:
            lst_munis.append(estado['sigla'] + ' ' + muni['nome'])
            M = Municipio(
                            cod = muni['id'],
                            nome = muni['nome'],
                            estado = E,
            )
            M.save()

    return lst_munis



def qr_and_or(campo, pesq):
    var = pesq.split(' && ')
    q = Q()
    for v_and in var:
        v_or = ''
        v_or = v_and.split(' || ')
        if len(v_or)>1:
            for v in v_or:
                q |= Q(**{campo: v})
        else:
            q &= Q(**{campo: v_and})
    return q