from fastapi import APIRouter, Request, HTTPException
from app.services.stripe import StripeService
from app.services.supabase import SupabaseService
from app.models.webhook import WebhookLogCreate


router = APIRouter(prefix="/stripe", tags=["stripe"])

def _process_payment_intent_event(payment_intent: dict, event_type: str) -> None:
    """
    Persiste eventos de payment_intent.* no Supabase.
    """
    amount_cents = payment_intent.get("amount") or payment_intent.get("amount_received", 0)
    customer_email = payment_intent.get("billing_details", {}).get("email")

    # Caso o email não esteja direto no payment_intent, tenta pegar do primeiro charge
    if not customer_email and isinstance(payment_intent.get("charges"), dict):
        first_charge = (payment_intent["charges"].get("data") or [{}])[0]
        customer_email = first_charge.get("billing_details", {}).get("email")

    webhook_log = WebhookLogCreate(
        charge_id=payment_intent["id"],
        amount=amount_cents / 100,
        currency=payment_intent.get("currency", "brl"),
        event_type=event_type,
        customer_id=payment_intent.get("customer", "N/A"),
        customer_email=customer_email or "N/A",
    )
    SupabaseService().webhook_log_insert(webhook_log)


@router.post("/webhook")
async def stripe_webhook(request: Request):
    """
    Endpoint que recebe webhooks do Stripe.
    """

    # Pega o corpo da requisição (bytes)
    payload = await request.body()

    # Pega o header de assinatura
    sig_header = request.headers.get('Stripe-Signature')

    if not sig_header:
        raise HTTPException(status_code=400, detail="Header Stripe-Signature ausente")
    
    # Valida o webhook
    stripe_service = StripeService()
    try:
        event = stripe_service.webhook_signature_verify(payload, sig_header)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))
    
    # Processa apenas eventos de charge
    if event['type'].startswith('charge.'):
        charge = event['data']['object']

        # Cria o objeto para inserir no Supabase
        webhook_log = WebhookLogCreate(
            charge_id = charge['id'],
            amount = charge['amount'] / 100, # Stripe envia em centavos
            currency = charge['currency'],
            event_type = event['type'],
            customer_id = charge.get('customer', 'N/A'),
            customer_email = charge.get("billing_details", {}).get('email', 'N/A')
        )

        # Salva no Supabase
        supabase_service = SupabaseService()
        supabase_service.webhook_log_insert(webhook_log)

    # Processa eventos de payment_intent
    elif event['type'].startswith('payment_intent.'):
        payment_intent = event['data']['object']
        _process_payment_intent_event(payment_intent, event['type'])

    return {"status": "success"}


@router.get("/webhooks")
async def listar_webhooks():
    """
    Lista todos os webhooks salvos no banco de dados.
    """

    supabase_service = SupabaseService()

    # Busca todos os registros
    response = supabase_service.client.table('webhook_log').select('*').execute()

    return {
        "total": len(response.data),
        "webhooks": response.data
    }