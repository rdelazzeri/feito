# Biblioteca de comunicação http/https
import http.client
from decouple import config

#  Define o Host para a comunicação com a API
conn = http.client.HTTPSConnection("webmaniabr.com")
print(config('x-consumer-key'))
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
conn.request("GET", "/api/1/nfe/certificado/", headers=headers)

# Retorno da API
res = conn.getresponse()
data = res.read()

# Exibir retorno
print(data.decode("utf-8"))

