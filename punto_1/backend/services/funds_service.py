import uuid
from datetime import datetime
from models.transaction import TransactionModel
from services.fund_data import FUNDS_CATALOG

USER_ID = "USER#1"


def get_fund_catalog():
    """Devuelve el catálogo completo de fondos disponibles."""
    return FUNDS_CATALOG


def _get_or_create_user_profile():
    """Obtiene el perfil del usuario o lo crea con el saldo inicial."""
    try:
        # Obtener el registro del perfil del usuario mediante su clave primaria.
        user_profile = TransactionModel.get(USER_ID, "PROFILE")
    except TransactionModel.DoesNotExist:
        # Si no existe, instanciar un nuevo modelo de perfil con valores iniciales.
        user_profile = TransactionModel(
            user_id=USER_ID,
            record_id="PROFILE",
            balance=500000,
            subscribed_funds={},
        )
        # Guardar el nuevo registro de perfil en la base de datos.
        user_profile.save()
    # Retornar el objeto del perfil del usuario, ya sea existente o recién creado.
    return user_profile


def subscribe_to_fund(fund_id: int):
    """Lógica para suscribir un usuario a un fondo usando acciones de actualización."""
    # Obtener los datos del fondo desde el catálogo.
    fund = FUNDS_CATALOG.get(fund_id)
    # Validar la existencia del fondo.
    if not fund:
        raise ValueError("El fondo no existe.")

    # Obtener o crear el perfil del usuario.
    user = _get_or_create_user_profile()

    # Verificar que el usuario no esté ya suscrito al fondo.
    if str(fund_id) in user.subscribed_funds.attribute_values:
        raise ValueError(f"Ya está suscrito al fondo {fund['name']}.")

    # Validar que el usuario posea saldo suficiente para la suscripción.
    if user.balance < fund["min_amount"]:
        raise ValueError(
            f"No tiene saldo disponible para vincularse al fondo {fund['name']}."
        )

    # Preparar el mapa de datos para el nuevo fondo a suscribir.
    new_fund_map = {"name": fund["name"], "amount": fund["min_amount"]}

    # Ejecutar una actualización atómica sobre el perfil del usuario.
    user.update(
        actions=[
            # 1. Restar el monto de la inversión del saldo actual.
            TransactionModel.balance.set(user.balance - fund["min_amount"]),
            # 2. Añadir el nuevo fondo al mapa de suscripciones.
            TransactionModel.subscribed_funds[str(fund_id)].set(new_fund_map),
        ]
    )

    # Crear un registro de transacción para auditoría.
    transaction_record = TransactionModel(
        user_id=USER_ID,
        record_id=f"TX#{datetime.utcnow().isoformat()}",
        transaction_type="SUSCRIPCION",
        amount=fund["min_amount"],
        fund_name=fund["name"],
    )
    # Guardar el registro de la transacción.
    transaction_record.save()

    # Retornar un mensaje de confirmación.
    return {"message": f"Suscripción exitosa al fondo {fund['name']}"}


def cancel_fund_subscription(fund_id: int):
    """Lógica para cancelar la suscripción a un fondo usando acciones de actualización."""
    # Obtener los datos del fondo desde el catálogo.
    fund = FUNDS_CATALOG.get(fund_id)
    # Validar la existencia del fondo.
    if not fund:
        raise ValueError("El fondo no existe.")

    # Obtener el perfil del usuario.
    user = _get_or_create_user_profile()

    # Extraer el mapa de suscripciones como un diccionario Python.
    raw_subscribed = user.subscribed_funds.attribute_values or {}
    # Verificar que el usuario esté suscrito al fondo que desea cancelar.
    if str(fund_id) not in raw_subscribed:
        raise ValueError(f"No está suscrito al fondo {fund['name']}.")

    # Extraer el monto invertido en el fondo para devolverlo al saldo.
    amount_to_return = float(raw_subscribed[str(fund_id)]["amount"])

    # Crear una copia del mapa de suscripciones para modificarlo.
    updated_map = raw_subscribed.copy()
    # Eliminar el fondo a cancelar del mapa copiado.
    del updated_map[str(fund_id)]

    # Ejecutar una actualización atómica sobre el perfil del usuario.
    user.update(
        actions=[
            # 1. Sumar el monto devuelto al saldo actual.
            TransactionModel.balance.set(user.balance + amount_to_return),
            # 2. Reemplazar el mapa de suscripciones completo con la versión actualizada.
            TransactionModel.subscribed_funds.set(updated_map),
        ]
    )

    # Crear un registro de transacción para la cancelación.
    transaction_record = TransactionModel(
        user_id=USER_ID,
        record_id=f"TX#{datetime.utcnow().isoformat()}",
        transaction_type="CANCELACION",
        amount=amount_to_return,
        fund_name=fund["name"],
    )
    # Guardar el registro de la transacción.
    transaction_record.save()

    # Retornar un mensaje de confirmación.
    return {"message": f"Cancelación exitosa del fondo {fund['name']}"}


def get_client_status_and_history():
    """Obtiene el estado actual y el historial de transacciones."""
    # Obtener el perfil del usuario para acceder a su estado actual.
    user = _get_or_create_user_profile()

    # --- Sección 1: Construir el historial de transacciones ---

    # Consultar todos los registros de transacciones (record_id prefijo "TX#").
    # Ordenar los resultados de más reciente a más antiguo.
    transactions_query = TransactionModel.query(
        USER_ID,
        TransactionModel.record_id.startswith("TX#"),
        scan_index_forward=False,
    )
    # Formatear los resultados de la consulta en una lista de diccionarios.
    history = [
        {
            "record_id": tx.record_id,
            "transaction_type": tx.transaction_type,
            "fund_name": tx.fund_name,
            "amount": float(tx.amount),
        }
        for tx in transactions_query
    ]

    # --- Sección 2: Construir el estado actual del cliente ---

    # Extraer el diccionario Python nativo del atributo de mapa de suscripciones.
    raw_subscribed = user.subscribed_funds.attribute_values or {}
    # Procesar el mapa para asegurar que los montos sean de tipo float.
    subscribed = {
        fund_id: {
            "name": info["name"],
            "amount": float(info["amount"]),
        }
        for fund_id, info in raw_subscribed.items()
    }

    # Ensamblar el objeto de estado actual del cliente.
    status = {
        "balance": float(user.balance),
        "subscribed_funds": subscribed,
    }

    # Retornar una estructura que contiene tanto el estado actual como el historial.
    return {"status": status, "history": history}
