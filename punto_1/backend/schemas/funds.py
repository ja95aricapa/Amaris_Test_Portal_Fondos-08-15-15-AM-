from pydantic import BaseModel, Field
from typing import Literal, Dict, List


class FundSubscriptionRequest(BaseModel):
    """Esquema para la solicitud de suscripción o cancelación."""

    fund_id: int = Field(..., gt=0, description="ID del fondo, ej: 1, 2, 3...")


class Transaction(BaseModel):
    """Esquema para mostrar una transacción en el historial."""

    record_id: str
    transaction_type: str
    fund_name: str
    amount: float


class ClientStatus(BaseModel):
    """Esquema para mostrar el estado actual del cliente."""

    balance: float
    subscribed_funds: Dict[
        str, dict
    ]  # { "fund_id_str": {"name": "...", "amount": ...} }


class StatusHistoryResponse(BaseModel):
    """Esquema para la respuesta del endpoint de estado e historial."""

    status: ClientStatus
    history: List[Transaction]
