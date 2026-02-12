from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# ============================================
# WEBHOOK LOG MODELS
# ============================================


# Classes para INSERIR itens no banco de dados
class WebhookLogCreate(BaseModel):
    """
    Modelopara criar uma nova charge no Supabase
    """

    created_at: datetime = Field(default_factory=datetime.now, description="Data de criação do item no banco")
    charge_id: str = Field(..., description="ID da charge no Stripe")
    currency: str = Field(default="brl", description="Moeda utilizada na cobrança")
    amount: float = Field(..., gt=0, description="Valor da cobrança")
    event_type: str = Field(..., description="Tipo do evento recebido no Webhook")
    customer_id: Optional[str] = Field(None, description="Customer ID no Stripe")
    customer_email: Optional[str] = Field(None, description="Email do customer")


# Classes para BUSCAR itens no banco de dados
class WebhookLogResponse(BaseModel):
    """
    Modelo de resposta ao buscar uma charge do Supabase
    """

    id: str
    created_at: datetime
    charge_id: str
    amount: float
    currency: str
    event_type: str
    customer_id: str
    customer_email: str

    class Config:
        from_attributes = True #Permite criar de ORM results