# Notas de desenvolvimento

## Passos iniciais
Criar ambiente virtual

    python3 -m venv venv

Ativar o ambiente virtual

    venv\Scripts\activate.ps1

Instalar Django

    pip install django

Criar o projeto

    django-admin startproject feito .

### Ativar o GIT

Inicializar o GIT

    git init

Criar o gitignore

    .gitignore

Adicionar todo conteúdo da pasta do projeto (exceto o que estiver no gitignore)

    git add .

Verificar o status do git

    git status

Se identificar no git

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"

Fazer o commit do projeto

    git commit -m "Início do projeto"

Seguindo os passos apresentados no github

    git branch -M main
    git remote add origin https://github.com/<conta>/<projeto>.git

Mandando os dados do commit para o github
    git push -u origin main
    
## Adicionar a APP core
Esta app será o núcleo do projeto, lidando com a autenticação dos usuários

    python manage.py startapp core

Atualizar o `Setings.py` Installed_apps:

    INSTALLED_APPS = [
        ...
        #apps de terceiros

        #My apps
        'core'
    ]

Atualizar o idioma e fuso horário:

    LANGUAGE_CODE = 'pt-br'
    TIME_ZONE = 'America/Sao_Paulo'

Rodar o servidor
    python manage.py runserver

Se estiver tudo bem, hora de criar as tabelas
    python manage.py migrate

Criar o superuser
    python manage.py createsuperuser

## Protegendo a Secret Key

Criar a pasta `contrib` dentro da pasta do projeto, incluir o arquivo `env_gen.py` com o seguinte conteúdo:

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
    """.strip() % get_random_string(50, chars)

    # Writing our configuration file to '.env'
    with open('.env', 'w') as configfile:
        configfile.write

Instalar o python-decouple

    pip install python-decouple

Alterar o setings.py

    import os
    from decouple import Csv, config
    SECRET_KEY = config('SECRET_KEY')
    DEBUG = config('DEBUG', default=False, cast=bool)
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default=[], cast=Csv())


