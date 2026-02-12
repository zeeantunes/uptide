from supabase import create_client, Client
from app.core.config import get_settings
from app.models.webhook import WebhookLogCreate, WebhookLogResponse


class SupabaseService:
    """
    Serviço para integrar com o Supabase
    """
    def __init__(self):
        settings = get_settings()
        self.client: Client = create_client(
            supabase_url = settings.supabase_url,
            supabase_key = settings.supabase_key
        )
    
    def webhook_log_insert(self, webhook_data: WebhookLogCreate) -> dict:
        """
        Insere um registro de webhook no banco de dados.

        Args:
            webhook_data: Dados do webhook validados pelo Pydantic

        Returns:
            Resposta do Supabase
        """

        response = self.client.table('webhook_log').insert(
            webhook_data.model_dump(mode='json')
        ).execute()

        return response.data

    def webhook_log_get_byID(self, log_id: str) -> WebhookLogResponse:
        """
        Busca um webhook log pelo ID da tabela no Supabase

        Args:
            log_if: UUID do registro no Supabase

        Returns:
            WebhookLogResponse com os dados
        """

        response = self.client.table('webhook_log').select('*').eq('id', log_id).execute()

        if not response.data:
            raise ValueError(f"Webhook log {log_id} não encontrado.")
        
        return WebhookLogResponse(**response.data[0])