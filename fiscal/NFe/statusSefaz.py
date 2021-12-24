# Status do Sefaz
#
# OBS: A utilização do endpoint deve ser realizada como demonstrativo do Status do
# Sefaz em sua plataforma, sendo necessário trabalhar com cache de ao menos 10 minutos.
# Não é necessário realizar a requisição antes da emissão de cada Nota Fiscal,
# porque este procedimento é realizado de forma automática em todos os endpoints.

# Biblioteca de comunicação http/https
import http.client
import os
from decouple import Csv, config

#  Define o Host para a comunicação com a API
conn = http.client.HTTPSConnection("webmaniabr.com")

# Credenciais de acesso

headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'x-consumer-key': config('x-consumer-key'),
    'x-consumer-secret': config('x-consumer-secret'),
    'x-access-token': config('x-access-token'),
    'x-access-token-secret': config('x-access-token-secret')
}

print(headers)

# Comunicando com a API
conn.request("GET", "/api/1/nfe/sefaz/", headers=headers)

# Retorno da API
res = conn.getresponse()
data = res.read()

# Exibir retorno
print(data.decode("utf-8"))
