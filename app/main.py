from fastapi import FastAPI
from app.routes import stripe

app = FastAPI(
    title = "Uptide Webhook API",
    description = "API para receber webhooks do Stripe e salvar no Supabase",
    version = "1.0.0"
)

# Registra as rotas
"""
Conecta as rotas do routes/stripe.py na aplicação principal.
"""
app.include_router(stripe.router)


@app.get("/")
async def root():
    """
    Rota raiz - verifica se a API está funcionando
    """

    return {
        "message": "Uptide API está rodando!",
        "status": "online"
    }

@app.get("/health")
async def health_check():
    """
    Rota para verificar se a API está saudável.
    """
    return {"status": "healthy"}

