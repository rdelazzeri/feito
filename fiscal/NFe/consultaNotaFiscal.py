import http.client
from decouple import config

conn = http.client.HTTPSConnection("webmaniabr.com")

headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'x-consumer-key': config('x-consumer-key'),
    'x-consumer-secret': config('x-consumer-secret'),
    'x-access-token': config('x-access-token'),
    'x-access-token-secret': config('x-access-token-secret')
}

conn.request("GET", "/api/1/nfe/consulta/?chave=43211204408568000105550010000131351001046555&ambiente=1", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
