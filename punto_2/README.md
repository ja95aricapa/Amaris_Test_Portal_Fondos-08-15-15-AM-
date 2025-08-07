# Punto 2: Base de Datos "EL_CLIENTE"

Este directorio contiene la definición y los datos de prueba de la base de datos **EL_CLIENTE**, junto con la consulta SQL solución.

## Archivos incluidos

- **EL_CLIENTE.db**
  Archivo SQLite con las tablas y datos cargados.

- **ddl.sql**
  Script DDL y DML para crear las tablas y poblar con datos de ejemplo.

  ```sql
  -- DDL para crear las tablas en SQLite
  CREATE TABLE Cliente (
      id INTEGER PRIMARY KEY,
      nombre VARCHAR(255) NOT NULL,
      apellidos VARCHAR(255) NOT NULL,
      ciudad VARCHAR(255) NOT NULL
  );
  CREATE TABLE Sucursal (
      id INTEGER PRIMARY KEY,
      nombre VARCHAR(255) NOT NULL,
      ciudad VARCHAR(255) NOT NULL
  );
  CREATE TABLE Producto (
      id INTEGER PRIMARY KEY,
      nombre VARCHAR(255) NOT NULL,
      tipoProducto VARCHAR(255) NOT NULL
  );
  CREATE TABLE Inscripcion (
      idProducto INTEGER,
      idCliente INTEGER,
      PRIMARY KEY (idProducto, idCliente),
      FOREIGN KEY (idProducto) REFERENCES Producto(id),
      FOREIGN KEY (idCliente) REFERENCES Cliente(id)
  );
  CREATE TABLE Disponibilidad (
      idSucursal INTEGER,
      idProducto INTEGER,
      PRIMARY KEY (idSucursal, idProducto),
      FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
      FOREIGN KEY (idProducto) REFERENCES Producto(id)
  );
  CREATE TABLE Visitan (
      idSucursal INTEGER,
      idCliente INTEGER,
      fechaVisita DATE NOT NULL,
      PRIMARY KEY (idSucursal, idCliente, fechaVisita),
      FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
      FOREIGN KEY (idCliente) REFERENCES Cliente(id)
  );
  -- DML de prueba...
  ```

- **respuesta.sql**
  Consulta que obtiene los nombres (_nombre_, _apellidos_) de los clientes que están inscritos en al menos un producto **y** han visitado **todas** las sucursales donde ese producto está disponible:

  ```sql
  SELECT DISTINCT c.nombre, c.apellidos
  FROM Cliente c
  JOIN Inscripcion i ON c.id = i.idCliente
  WHERE
      -- No existe sucursal con el producto que el cliente NO haya visitado
      NOT EXISTS (
          SELECT 1
          FROM Disponibilidad d
          WHERE d.idProducto = i.idProducto
            AND d.idSucursal NOT IN (
              SELECT v.idSucursal
              FROM Visitan v
              WHERE v.idCliente = c.id
            )
      )
      -- Y sí haya visitado al menos una sucursal que ofrezca el producto
      AND EXISTS (
          SELECT 1
          FROM Visitan v
          JOIN Disponibilidad d ON v.idSucursal = d.idSucursal
          WHERE v.idCliente = c.id
            AND d.idProducto = i.idProducto
      );
  ```

## Cómo usar

1. Abre la base SQLite:

   ```bash
   sqlite3 EL_CLIENTE.db
   ```

2. (Opcional) Carga el esquema y datos desde `ddl.sql`:

   ```sql
   .read ddl.sql
   ```

3. Ejecuta la consulta de `respuesta.sql` para ver los resultados:

   ```sql
   .read respuesta.sql
   ```

   Deberías obtener los clientes que cumplen la condición descrita.

## Explicación de la consulta

- **NOT EXISTS**: asegura que no quede ninguna sucursal donde el producto esté disponible y el cliente no la haya visitado (es decir, visitó todas).
- **EXISTS**: confirma que el cliente haya visitado al menos una de las sucursales que ofrecen su producto.
- **DISTINCT**: elimina duplicados si un cliente está inscrito en varios productos.
