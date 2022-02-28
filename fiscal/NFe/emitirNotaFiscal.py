# Biblioteca de comunicação http/https
import http.client
# Biblioteca para manipulação de json
import json
from decouple import config
from fiscal.models import NFe_transmissao, NF_config

import json
from contextlib import suppress
'''
# Busca o arquivo que contém o json para Emissão de Nota Fiscal
with open('ExemploJson/emitirNotaFiscal.json', 'r') as json_file:
   # Carrega o conteudo do arquivo e converte em array
   array = json.load(json_file)
   # Converte o array em json novamente
   json = json.dumps(array)
'''



def emitirNotaFiscal(pre_nota):
    
    print('fiscal.nfe.emitirNotaFiscal.emitirNotaFiscal()')
    print('transmissão pre_nota id: ' + str(pre_nota.id))
    
    #  Define o Host para a comunicação com a API
    conn = http.client.HTTPSConnection("webmaniabr.com")

    

    nfe = NFe_transmissao.objects.filter(pre_nota = pre_nota).first()
    nfe_json = nfe.nfe_json

    #print(str(nfe_json))

    # Credenciais de acesso
    headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'x-consumer-key': config('x-consumer-key'),
    'x-consumer-secret': config('x-consumer-secret'),
    'x-access-token': config('x-access-token'),
    'x-access-token-secret': config('x-access-token-secret')
    }

    # Comunicando com a API
    conn.request("POST", "/api/1/nfe/emissao/", nfe_json, headers)

    # Retorno da API
    res = conn.getresponse()
    data = res.read()

    # Exibir retorno
    retorno = data.decode("utf-8")
    print('Retorno do Sefaz:')
    print(retorno)
    ret_json = json.loads(retorno)
    
    try:
        nfe.error = ret_json['error']
        erro = True
    except:
        nfe.nfe = ret_json['nfe']
        nfe.serie = ret_json['serie']
        nfe.uuid = ret_json['uuid']
        nfe.status = ret_json['status']
        if ret_json['motivo']: nfe.motivo = ret_json['motivo']
        nfe.chave = ret_json['chave']
        nfe.modelo = ret_json['modelo']
        nfe.log = ret_json['log']
        nfe.xml = ret_json['xml']
        nfe.danfe = ret_json['danfe']
        nfe.danfe_simples = ret_json['danfe_simples']
        nfe.error = '-'
        erro = False
    nfe.save()
    
    print('teste do númro da nf')
    if erro:
        pre_nota.entrega.status = 1
    else:
        pre_nota.entrega.status = 2
        pre_nota.num_nf = nfe.nfe
        pre_nota.entrega.num_nf = nfe.nfe
        pre_nota.save()
        cfg = NF_config.objects.filter(pk = 1).first()
        cfg.last_num = nfe.nfe
        cfg.save()
    return 'Transmissão concluída'