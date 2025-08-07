# Gestor de Fondos API - Backend

Este documento describe cómo configurar, ejecutar y probar el servidor de la API del Gestor de Fondos.

## Índice

- [Gestor de Fondos API - Backend](#gestor-de-fondos-api---backend)
  - [Índice](#índice)
  - [Descripción](#descripción)
  - [Prerequisitos](#prerequisitos)
  - [Configuración del entorno](#configuración-del-entorno)
  - [Ejecución local](#ejecución-local)
  - [Ejecución con Docker Compose](#ejecución-con-docker-compose)
  - [Uso de DynamoDB Local](#uso-de-dynamodb-local)
  - [Ejemplos de uso de los endpoints](#ejemplos-de-uso-de-los-endpoints)

---

## Descripción

La API de Gestor de Fondos permite a los usuarios suscribirse y cancelar suscripciones a fondos, así como consultar su estado y el historial de transacciones.

Está implementada con FastAPI, PynamoDB para interacción con DynamoDB y Docker para orquestar los servicios (API, frontend y DynamoDB Local).

---

## Prerequisitos

- Python 3.11+
- pip
- Docker
- Docker Compose
- (Opcional) Visual Studio Code u otro editor

---

## Configuración del entorno

1. Clona el repositorio y navega a la carpeta del proyecto:

   ```bash
   git clone <repo-url>
   cd punto_1
   ```

2. Copia el archivo de variables de entorno para el backend:

   ```bash
   cd backend
   cp .env.example .env
   ```

3. Verifica que en `.env` esté definida la URL de DynamoDB Local (ejemplo):

   ```dotenv
   DYNAMODB_URL=http://localhost:8001
   ```

---

## Ejecución local

Para correr la API de forma local sin Docker (requiere tener DynamoDB Local corriendo en contenedor o localmente):

1. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

2. Asegúrate de levantar DynamoDB Local (ver sección siguiente).

3. Ejecuta el servidor:

   - Desde VSCode: Ejecuta `main.py` con el depurador.
   - Desde terminal:

     ```bash
     python main.py
     ```

4. La API estará disponible en `http://127.0.0.1:8000`.

---

## Ejecución con Docker Compose

1. Desde la raíz del proyecto (`punto_1`), levanta todos los servicios:

   ```bash
   docker-compose up --build
   ```

2. Esto iniciará:

   - **api** en el puerto `8000`
   - **frontend** en el puerto `3000`
   - **dynamodb-local** en el puerto `8001`

3. Para detener los servicios:

   ```bash
   docker-compose down
   ```

---

## Uso de DynamoDB Local

La API requiere siempre un contenedor de DynamoDB Local activo, ya sea en local o mediante Docker Compose.

- URL por defecto para conectarse: `http://localhost:8001`
- Volumen persistente en `./dynamodb_data`

---

## Ejemplos de uso de los endpoints

> **Nota**: Reemplaza `127.0.0.1` por la IP/host donde esté corriendo la API.

1. **Verificar que la API esté levantada**

   ```bash
   curl http://127.0.0.1:8000/
   # { "message": "API del Gestor de Fondos funcionando." }
   ```

2. **Suscribirse a un fondo**

   ```bash
   curl -X POST http://127.0.0.1:8000/funds/subscribe \
     -H "Content-Type: application/json" \
     -d '{"fund_id": 1}'
   # { "message": "Suscripción exitosa al fondo FPV_EL CLIENTE_RECAUDADORA" }
   ```

3. **Cancelar suscripción a un fondo**

   ```bash
   curl -X POST http://127.0.0.1:8000/funds/cancel \
     -H "Content-Type: application/json" \
     -d '{"fund_id": 1}'
   # { "message": "Cancelación exitosa del fondo FPV_EL CLIENTE_RECAUDADORA" }
   ```

4. **Consultar estado y historial**

   ```bash
   curl http://127.0.0.1:8000/funds/status-history
   # { "status": { ... }, "history": [ ... ] }
   ```
