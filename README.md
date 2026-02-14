# Uptide Webhook API

Pequena API para receber webhooks do Stripe e salvar no Supabase.

## Setup rápido

1. Criar e ativar um virtualenv (recomendado):

```bash
cd /home/manoel/Documents/estudos/python/stripe-api/uptide
python3 -m venv .venv
. .venv/bin/activate
```

2. Instalar dependências:

```bash
pip install -r requirements.txt
```

3. Criar arquivo `.env` na raiz do projeto (veja `app/core/config.py`) com as variáveis necessárias, por exemplo:

```
STRIPE_API_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx
SUPABASE_URL=https://...
SUPABASE_KEY=...
ENVIRONMENT=development
```

4. Rodar a aplicação (dentro do venv):

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

5. Testar healthcheck:

```bash
curl http://127.0.0.1:8000/health
# deve retornar: {"status":"healthy"}
```

## Observações

- O projeto já possui `.env` no `.gitignore`.
- Recomendo usar o `.venv` local para evitar conflitos de dependências globais.

