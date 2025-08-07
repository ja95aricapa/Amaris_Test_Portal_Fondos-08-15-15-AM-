from fastapi import APIRouter, HTTPException, status
from services import funds_service
from schemas.funds import (
    FundSubscriptionRequest,
    Transaction,
    ClientStatus,
    StatusHistoryResponse,
)

router = APIRouter(prefix="/funds", tags=["Funds"])


@router.get("/catalog")
def get_catalog():
    """Devuelve la lista de todos los fondos disponibles."""
    return funds_service.get_fund_catalog()


@router.get(
    "/status-history",
    status_code=status.HTTP_200_OK,
    response_model=StatusHistoryResponse,
)
def get_status_and_history():
    """Endpoint para ver el estado actual y el historial de transacciones."""
    return funds_service.get_client_status_and_history()


@router.post("/subscribe", status_code=status.HTTP_200_OK)
def subscribe(request: FundSubscriptionRequest):
    """Endpoint para suscribirse a un nuevo fondo[cite: 9]."""
    try:
        return funds_service.subscribe_to_fund(request.fund_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/cancel", status_code=status.HTTP_200_OK)
def cancel(request: FundSubscriptionRequest):
    """Endpoint para salirse de un fondo actual[cite: 10]."""
    try:
        return funds_service.cancel_fund_subscription(request.fund_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
