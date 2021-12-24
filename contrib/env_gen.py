#!/usr/bin/env python

"""
Django SECRET_KEY generator.
"""
from django.utils.crypto import get_random_string

chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'

CONFIG_STRING = """
DEBUG=True
SECRET_KEY=%s
ALLOWED_HOSTS=127.0.0.1, .localhost
#DATABASE_URL=postgres://USER:PASSWORD@HOST:PORT/NAME
#DEFAULT_FROM_EMAIL=
#EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
#EMAIL_HOST=
#EMAIL_PORT=
#EMAIL_USE_TLS=
#EMAIL_HOST_USER=
#EMAIL_HOST_PASSWORD=
#Web mania
x-consumer-key = "oeVmTBe48Em8qLhPodRwjHPQsWxTZNtt",
x-consumer-secret = "5zLmEoiCPGyrBLnfuA2YdhsFtIl8SNPKnjNOVch8jQesULZq",
x-access-token = "3026-NDYK34iYJpDB2bxVa37cZk2U0utAbLZyvpHtSTqC1VhhOA7n",
x-access-token-secret = "GJ6APs8LCFhj9kS05xbCArYZ5RvzmTAFppuvJrU8kInBdIlj"
""".strip() % get_random_string(50, chars)

# Writing our configuration file to '.env'
with open('.env', 'w') as configfile:
    configfile.write(CONFIG_STRING)



#rodar este comanda para gerar o arquivo .env
# python contrib/env_gen.py