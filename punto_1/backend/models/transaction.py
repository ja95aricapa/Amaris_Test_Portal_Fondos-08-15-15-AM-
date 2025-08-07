import os
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute
from dotenv import load_dotenv

if os.getenv("ENV", "development") == "development":
    load_dotenv()

# --- Configuración del Entorno de DynamoDB ---
# Usamos variables de entorno para que Docker Compose pueda inyectar la URL local.
DYNAMODB_URL = os.getenv("DYNAMODB_URL")


class TransactionModel(Model):
    """
    Modelo para la tabla DynamoDB usando un diseño de tabla única.
    - PK: 'USER#1' para el perfil del cliente. 'TX#{tx_id}' para transacciones.
    - SK: 'PROFILE' para el perfil. '#{timestamp}' para ordenar transacciones.
    """

    class Meta:
        table_name = "FondosCliente"
        # Si la variable de entorno existe, apunta al DynamoDB local (para Docker)
        if DYNAMODB_URL:
            host = DYNAMODB_URL
        # De lo contrario, usará las credenciales de AWS por defecto
        region = "us-east-1"
        write_capacity_units = 1
        read_capacity_units = 1

    # Atributos de la Clave
    user_id = UnicodeAttribute(hash_key=True)
    record_id = UnicodeAttribute(range_key=True)  # SK

    # Atributos de Datos
    balance = NumberAttribute(null=True)
    subscribed_funds = MapAttribute(null=True)  # Almacenará los fondos suscritos

    # Atributos específicos de la transacción
    transaction_type = UnicodeAttribute(null=True)
    amount = NumberAttribute(null=True)
    fund_name = UnicodeAttribute(null=True)


# --- Función para crear la tabla si no existe ---
def create_table_if_not_exists():
    """Verifica y crea la tabla de DynamoDB."""
    if not TransactionModel.exists():
        print("La tabla 'FondosCliente' no existe. Creando...")
        TransactionModel.create_table(wait=True)
        print("Tabla creada exitosamente.")
    else:
        print("La tabla 'FondosCliente' ya existe.")
