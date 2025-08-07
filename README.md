# Repositorio de soluciones prueba Amaris

Este repositorio agrupa dos proyectos independientes:

- **Punto 1: Portal de Fondos**
  Una aplicación full‑stack que permite a un cliente realizar suscripciones y cancelaciones en fondos de inversión, consultar su estado y ver el historial de transacciones.

- **Punto 2: Consulta SQL en SQLite**
  Un ejercicio de base de datos que identifica, mediante una consulta SQL, los clientes que han visitado todas las sucursales donde están disponibles los productos a los que están inscritos.

---

## Punto 1: Portal de Fondos

Ubicado en la carpeta `punto_1/`, contiene:

- **backend/**: API REST construida con **FastAPI**, **PynamoDB** y **DynamoDB Local**.
- **frontend/**: SPA en **React**, que consume la API para mostrar el catálogo de fondos, gestionar suscripciones y presentar el historial.
- **Dockerfile.api** y **Dockerfile.react**: Dockerfiles para cada servicio.
- **docker-compose.yml**: Orquesta los contenedores de API, frontend y DynamoDB Local.

### Características principales

1. Suscribirse a un fondo (monto mínimo según catálogo).
2. Cancelar suscripción y devolución del monto.
3. Consultar historial de aperturas y cancelaciones.
4. (Pendiente) Notificaciones por email/SMS tras suscripción.

### Cómo ejecutar

Desde la raíz del repositorio:

```bash
docker-compose up --build
```

- API en `http://localhost:8000`
- Frontend en `http://localhost:3000`
- DynamoDB Local en `http://localhost:8001`

---

## Punto 2: Consulta SQL en SQLite

Ubicado en la carpeta `punto_2/`, contiene:

- **EL_CLIENTE.db**: Base de datos SQLite con tablas y datos de ejemplo.
- **ddl.sql**: Script para crear tablas (`Cliente`, `Sucursal`, `Producto`, `Inscripcion`, `Disponibilidad`, `Visitan`) y poblar datos.
- **respuesta.sql**: Consulta que obtiene los nombres de los clientes que han visitado todas las sucursales donde su(s) producto(s) está(n) disponible(s).

### Cómo reproducir

1. Abre SQLite:

   ```bash
   sqlite3 punto_2/EL_CLIENTE.db
   ```

2. (Opcional) Ejecuta el DDL/DML:

   ```sql
   .read punto_2/ddl.sql
   ```

3. Ejecuta la consulta de solución:

   ```sql
   .read punto_2/respuesta.sql
   ```

Verás la lista de clientes que cumplen la condición de haber recorrido cada sucursal que ofrece sus productos.
