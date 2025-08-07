# Punto 1: Portal de Fondos

Este repositorio contiene el **backend** (FastAPI + PynamoDB + DynamoDB Local) y el **frontend** (React) del Portal de Fondos de EL CLIENTE.

## Contenido

```
./Dockerfile.api         # Dockerfile de la API (backend)
./Dockerfile.react       # Dockerfile de la app React (frontend)
./docker-compose.yml     # Orquestación de servicios Docker
./backend/               # Código fuente del backend
  └── README.md          # Instrucciones específicas del backend
./frontend/              # Código fuente del frontend
  └── README.md          # Instrucciones específicas del frontend
```

---

## Ejecución con Docker Compose

Toda la aplicación (API, frontend y DynamoDB Local) puede levantarse con un único comando:

```bash
docker-compose up --build
```

- **API** (FastAPI) disponible en `http://localhost:8000`
- **Frontend** (React) servido por Nginx en `http://localhost:3000`
- **DynamoDB Local** en `http://localhost:8001`

Para detener y eliminar contenedores:

```bash
docker-compose down
```

> **Nota**: Asegúrate de no tener otros servicios usando los puertos 8000, 3000 o 8001.

---

## 1. Requerimientos de Negocio

EL CLIENTE necesita un sistema que permita a sus clientes realizar:

1. Suscribirse a un nuevo fondo (aperturas).
2. Salirse de un fondo actual (cancelaciones).
3. Ver el historial de últimas transacciones.
4. Enviar notificaciones por email o SMS tras suscripción.

**Reglas de negocio**:

- Monto inicial disponible: COP \$500.000.
- Cada transacción genera un identificador único.
- Cada fondo tiene un monto mínimo de vinculación.
- Al cancelar, el valor vinculado se retorna al cliente.
- Si no hay saldo suficiente, se muestra:
  “No tiene saldo disponible para vincularse al fondo <NombreFondo>”.
- Sin autenticación: único usuario.
- Catálogo de fondos:

  | ID  | Nombre                     | Mínimo  | Categoría |
  | --- | -------------------------- | ------- | --------- |
  | 1   | FPV_EL CLIENTE_RECAUDADORA | 75.000  | FPV       |
  | 2   | FPV_EL CLIENTE_ECOPETROL   | 125.000 | FPV       |
  | 3   | DEUDAPRIVADA               | 50.000  | FIC       |
  | 4   | FDO-ACCIONES               | 250.000 | FIC       |
  | 5   | FPV_EL CLIENTE_DINAMICA    | 100.000 | FPV       |

---

## 2. Diseño de la Solución

### a) Tecnologías Utilizadas

- **Python + FastAPI**: Permite desarrollar una API REST rápida, con validación automática de esquemas y buena documentación.
- **PynamoDB + DynamoDB Local**: Base de datos NoSQL escalable y sin servidor, ideal para un modelo de tabla única con transacciones y perfil de usuario.
- **React**: Construcción de SPA con recarga en caliente y componentes reactivos.
- **Docker & Docker Compose**: Aislamiento de servicios y facilidad de despliegue.
- **python-dotenv**: Carga de variables de entorno para configuración dinámica.

> **Justificación**: Estas tecnologías permiten iterar rápido, escalar en AWS, y garantizan mantenibilidad y pruebas automatizadas.

### b) Modelo de Datos NoSQL (DynamoDB)

**Tabla**: `FondosCliente` (diseño de tabla única)

- **PK (hash key)**: `user_id` (ej: `USER#1`)
- **SK (range key)**:

  - Perfil: `PROFILE`
  - Transacciones: `TX#<timestamp_ISO>`

**Atributos**:

- `balance` (Number): saldo actual.
- `subscribed_funds` (Map): mapa de `{ fund_id: { name, amount } }`.
- **Transacción**:

  - `transaction_type` (String): `SUSCRIPCION` o `CANCELACION`.
  - `amount` (Number): monto de la operación.
  - `fund_name` (String).

Este diseño facilita:

- Lectura rápida del perfil y transacciones ordenadas.
- Operaciones atómicas de actualización con PynamoDB.

### c) Componentes de la Aplicación

1. **Backend (FastAPI)**

   - **Routers**: `/funds/catalog`, `/funds/subscribe`, `/funds/cancel`, `/funds/status-history`.
   - **Servicios**: Lógica de negocio, validaciones y acceso a DynamoDB.
   - **Schemas**: Pydantic para validar solicitudes y respuestas.
   - **Tests Unitarios**: (Opcional) pytest para lógica de servicio y validación de endpoints.
   - **Manejo de excepciones**: Errores de negocio devuelven 400 con mensaje claro.

2. **Frontend (React)**

   - **App.js**: Llama a la API, muestra estado, lista de fondos y historial.
   - **Componentes**: Formularios de suscripción y cancelación, tabla de historial.
   - **Estilos**: CSS modular en `App.css`.
   - **Errores de red**: Muestra mensajes de éxito/error.

3. **Notificaciones**

   - Funcionalidad pendiente de integrar servicio de email/SMS tras suscripción.
   - Puede usarse AWS SNS o servicio externo (Twilio, SendGrid).

---

## 3. Paso a Paso para Ejecutar

1. **Clonar repositorio**:

   ```bash
   git clone <[repo-url](https://github.com/ja95aricapa/Amaris_Test_Portal_Fondos/tree/main)> && cd punto\_1
   ```

2. **Levantar todo con Docker Compose**:

   ```bash
   docker-compose up --build
   ```

3. **Acceder a la aplicación**:

   - Frontend: [http://localhost:3000](http://localhost:3000)
   - API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

4. **Probar endpoints**:

   - Suscripción: `POST /funds/subscribe { "fund_id": 1 }`
   - Cancelación: `POST /funds/cancel { "fund_id": 1 }`
   - Estado e historial: `GET /funds/status-history`
   - Catálogo: `GET /funds/catalog`
