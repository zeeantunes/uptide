import stripe
from app.core.config import get_settings

class StripeService:
    """
    Serviço para interagir com a API do Stripe.
    """

    def __init__(self):
        settings = get_settings()
        stripe.api_key = settings.stripe_api_key
        self.webhook_secret = settings.stripe_webhook_secret
    
    def webhook_signature_verify(self, payload: bytes, sig_header: str) -> stripe.Event:
        """
        Verifica a assinatura do webhook vindo do Stripe.

        Args:
            payload: Corpo da requisição (bytes)
            sig_header: Header 'Stripe-Signature'

        Returns:
            Evento do Stripe validado

        Raises:
            ValueError: Se a assinatura for inválida
        """

        try:
            event = stripe.Webhook.construct_event(
                payload = payload,
                sig_header = sig_header,
                secret = self.webhook_secret
            )
            return event
        except stripe.error.SignatureVerificationError as error:
            raise ValueError(f"Assinatura inválida: {str(error)}")