# ChurchManager Pro

Sistema de administração para igrejas com portal público + painel interno em Django.

## O que foi adicionado nesta versão

- Layout profissional (site público e telas internas) com tema moderno e responsivo.
- White-label para revenda: branding e tema editáveis por igreja.
- Admin Django com visual premium (branding, login e tema customizado).
- Módulo novo: `Pedido de Oração` público com gestão no admin.
- Rotas internas organizadas (`membros`, `visitantes`, `ministerios`, `dashboard`).
- Segurança e configuração por ambiente já preparadas em `settings.py`.

## White-label (revenda para outras igrejas)

No Admin, em **Configurações do Portal**, agora você pode editar:

- Nome do sistema e slogan
- Nome da igreja e pastor
- Chave da igreja (identificador)
- Domínio oficial
- Cidade/estado e contatos
- Redes sociais
- Cores do tema (`primária`, `secundária`, `destaque`, `fundo`)
- Flag comercial para revenda

## Setup local

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 manage.py migrate
python3 manage.py createsuperuser
python3 manage.py runserver
```

## Variáveis de ambiente importantes

- `SECRET_KEY`
- `DEBUG`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `CSRF_TRUSTED_ORIGINS`
- `SERVE_MEDIA_IN_PROD`

## Deploy (Render)

O projeto já possui suporte para deploy com:

- `gunicorn`
- `whitenoise`
- leitura de `DATABASE_URL`
- segurança para produção (`SSL`, cookies seguros, HSTS)

## Testes

```bash
python3 manage.py test
python3 manage.py check
```
