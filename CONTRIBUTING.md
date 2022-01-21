## Como rodar o projeto

> Necessário usar ambiente UNIX, devido o uso do gunicorn.

1. Instalar o `Python 3.10.2`
2. Instalar o `pip`
3. Configurar a `.env` com as variáveis de ambiente

## Comandos
```bash

# Instalar as dependências do projeto
$ pip install -r requirements.txt

# Rodar o projeto local
$ gunicorn --bind 0.0.0.0:5000 src.app:app

# Executar os testes
$ python3 -m pytest -W ignore::DeprecationWarning

```