'''
JSON request:

{
  "ID": 1137,
  "url_notificacao": "https://webmaniabr.com/retorno.php",
  "operacao": 1,
  "natureza_operacao": "Venda de produção do estabelecimento",
  "modelo": 1,
  "finalidade": 1,
  "ambiente": 1,
  "cliente": {
   "cpf": "980.453.164-03",
   "nome_completo": "Miguel Pereira da Silva",
   "endereco": "Av. Anita Garibaldi",
   "complemento": "Sala 809 Royal",
   "numero": 850,
   "bairro": "Ahú",
   "cidade": "Curitiba",
   "uf": "PR",
   "cep": "80540-180",
   "telefone": "(41) 4063-9102",
   "email": "suporte@webmaniabr.com"
  },
  "produtos": [
     {
      "nome": "Camisetas Night Run",
      "sku": "camiseta-night-run",
      "ean": "0789602015376",
      "ncm": "6109.10.00",
      "cest": "28.038.00",
      "cnpj_produtor": "11.290.027/0001-82",
      "quantidade": 3,
      "unidade": "UN",
      "peso": "0.800",
      "origem": 0,
      "subtotal": "44.90",
      "total": "134.70",
      "classe_imposto": "REF1637"
     },
     {
      "nome": "Camisetas 10 Milhas",
      "sku": "camisetas-10-milhas",
      "ean": "0789602015376",
      "ncm": "6109.10.00",
      "cest": "28.038.00",
      "cnpj_produtor": "11.290.027/0001-82",
      "quantidade": "1",
      "unidade": "UN",
      "peso": "0.200",
      "origem": 0,
      "subtotal": "29.90",
      "total": "29.90",
      "classe_imposto": "REF1637"
     }
  ],
  "pedido": {
     "pagamento": 0,
     "presenca": 2,
     "modalidade_frete": 0,
     "frete": "12.56",
     "desconto": "10.00",
     "total": "174.60"
  },
  "transporte": {
     "cnpj": "11.290.027/0001-82",
     "razao_social": "Transportes LTDA",
     "ie": "123.456.789.123",
     "endereco": "Av. Anita Garibaldi",
     "uf": "PR",
     "cidade": "Curitiba",
     "cep": "80540-180"
  }
}
'''

import http.client
from decouple import config

conn = http.client.HTTPSConnection("webmaniabr.com")

payload = "{\"ID\": 1137,\"url_notificacao\": \"https://webmaniabr.com/retorno.php\",\"operacao\": 1,\"natureza_operacao\": \"Venda de produção do estabelecimento\",\"modelo\": 1,\"finalidade\": 1,\"ambiente\": 1,\"cliente\": {\"cpf\": \"980.453.164-03\",\"nome_completo\": \"Miguel Pereira da Silva\",\"endereco\": \"Av. Anita Garibaldi\",\"complemento\": \"Sala 809 Royal\",\"numero\": 850,\"bairro\": \"Ahú\",\"cidade\": \"Curitiba\",\"uf\": \"PR\",\"cep\": \"80540-180\",\"telefone\": \"(41) 4063-9102\",\"email\": \"suporte@webmaniabr.com\"},\"produtos\": [{\"nome\": \"Camisetas Night Run\",\"sku\": \"camiseta-night-run\",\"ean\": \"0789602015376\",\"ncm\": \"6109.10.00\",\"cest\": \"28.038.00\",\"cnpj_produtor\": \"11.290.027/0001-82\",\"quantidade\": 3,\"unidade\": \"UN\",\"peso\": \"0.800\",\"origem\": 0,\"subtotal\": \"44.90\",\"total\": \"134.70\",\"classe_imposto\": \"REF1637\"},{\"nome\": \"Camisetas 10 Milhas\",\"sku\": \"camisetas-10-milhas\",\"ean\": \"0789602015376\",\"ncm\": \"6109.10.00\",\"cest\": \"28.038.00\",\"cnpj_produtor\": \"11.290.027/0001-82\",\"quantidade\": \"1\",\"unidade\": \"UN\",\"peso\": \"0.200\",\"origem\": 0,\"subtotal\": \"29.90\",\"total\": \"29.90\",\"classe_imposto\": \"REF1637\"}],\"pedido\": {\"pagamento\": 0,\"presenca\": 2,\"modalidade_frete\": 0,\"frete\": \"12.56\",\"desconto\": \"10.00\",\"total\": \"174.60\"},\"transporte\": {\"cnpj\": \"11.290.027/0001-82\",\"razao_social\": \"Transportes LTDA\",\"ie\": \"123.456.789.123\",\"endereco\": \"Av. Anita Garibaldi\",\"uf\": \"PR\",\"cidade\": \"Curitiba\",\"cep\": \"80540-180\"}}"

headers = {
    'cache-control': "no-cache",
    'content-type': "application/json",
    'x-consumer-key': config('x-consumer-key'),
    'x-consumer-secret': config('x-consumer-secret'),
    'x-access-token': config('x-access-token'),
    'x-access-token-secret': config('x-access-token-secret')
}

conn.request("POST", "/api/1/nfe/emissao/", payload, headers)

res = conn.getresponse()
data = res.read()

print(headers)
print(payload)
print(data.decode("utf-8"))
