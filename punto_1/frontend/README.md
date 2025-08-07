# Portal de Fondos - Frontend

Este proyecto es la aplicación React para el **Portal de Fondos**, que consume el API desarrollada en el backend para mostrar el catálogo de fondos, gestionar suscripciones y mostrar el historial de transacciones.

## Índice

- [Portal de Fondos - Frontend](#portal-de-fondos---frontend)
  - [Índice](#índice)
  - [Descripción](#descripción)
  - [Prerequisitos](#prerequisitos)
  - [Estructura del proyecto](#estructura-del-proyecto)
  - [Configuración de variables de entorno](#configuración-de-variables-de-entorno)
  - [Ejecución local (solo frontend)](#ejecución-local-solo-frontend)
  - [Ejecución completa con Docker Compose](#ejecución-completa-con-docker-compose)
  - [Scripts disponibles](#scripts-disponibles)
  - [Notas](#notas)

---

## Descripción

La aplicación permite a los usuarios:

- Visualizar su saldo y fondos a los que están suscritos.
- Suscribirse a nuevos fondos.
- Cancelar suscripciones existentes.
- Consultar el historial de transacciones.

Se basa en [Create React App](https://create-react-app.dev/) y está preparada para funcionar:

- **De forma aislada** (sin conexión a la API) en modo desarrollo.
- **En conjunto** con el backend y DynamoDB Local usando Docker Compose.

---

## Prerequisitos

- Node.js v16+ y npm.
- (Opcional) Docker y Docker Compose, para ejecutar la aplicación completa.

---

## Estructura del proyecto

```
frontend/
├── public/           # Archivos estáticos (HTML, favicon)
├── src/              # Código fuente React
│   ├── App.js        # Componente principal
│   ├── App.css       # Estilos globales
│   └── index.js      # Punto de entrada
├── Dockerfile.react  # Dockerfile para producción
├── package.json      # Dependencias y scripts
└── README.md         # Este documento
```

---

## Configuración de variables de entorno

Puedes definir la URL de la API que consume el frontend mediante la variable:

```
REACT_APP_API_URL=http://localhost:8000
```

- **Modo desarrollo local**: no es obligatoria, ya que por defecto apuntará a `http://localhost:8000`.

---

## Ejecución local (solo frontend)

1. Instala las dependencias:

   ```bash
   npm install
   ```

2. Inicia el servidor de desarrollo:

   ```bash
   npm start
   ```

3. Abre tu navegador en [http://localhost:3000](http://localhost:3000).

> Esta forma levanta únicamente la UI de React. No se mostrarán datos reales de fondos a menos que exista la API corriendo en `REACT_APP_API_URL`.

---

## Ejecución completa con Docker Compose

Desde la raíz del proyecto (donde está `docker-compose.yml`):

```bash
docker-compose up --build
```

Esto levantará tres servicios:

- **api**: Backend de FastAPI en el puerto 8000.
- **frontend**: UI de React compilada servida por Nginx en el puerto 3000.
- **dynamodb-local**: DynamoDB Local en el puerto 8001.

Abre [http://localhost:3000](http://localhost:3000) para usar la app completa.

Para detenerlos:

```bash
docker-compose down
```

---

## Scripts disponibles

En `package.json`:

- `npm start`: Modo desarrollo (hot reload).
- `npm run build`: Genera la versión de producción en la carpeta `build/`.
- `npm test`: Ejecuta tests (si los hubiera).

---

## Notas

- Si quieres personalizar el `service worker` o convertirla en PWA, deberás agregar el archivo `custom-service-worker.js` en `public/`.
- Asegúrate de que la API esté corriendo en la URL correcta para evitar errores de red (`Failed to fetch`).
