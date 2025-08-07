-- DDL para crear las tablas en SQLite

-- Tabla para almacenar la información de los clientes
CREATE TABLE Cliente (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    apellidos VARCHAR(255) NOT NULL,
    ciudad VARCHAR(255) NOT NULL
);

-- Tabla para almacenar la información de las sucursales
CREATE TABLE Sucursal (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    ciudad VARCHAR(255) NOT NULL
);

-- Tabla para almacenar los productos ofrecidos
CREATE TABLE Producto (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR(255) NOT NULL,
    tipoProducto VARCHAR(255) NOT NULL
);

-- Tabla de relación para la inscripción de un cliente a un producto
CREATE TABLE Inscripcion (
    idProducto INTEGER,
    idCliente INTEGER,
    PRIMARY KEY (idProducto, idCliente),
    FOREIGN KEY (idProducto) REFERENCES Producto(id),
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)
);

-- Tabla de relación para la disponibilidad de un producto en una sucursal
CREATE TABLE Disponibilidad (
    idSucursal INTEGER,
    idProducto INTEGER,
    PRIMARY KEY (idSucursal, idProducto),
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (idProducto) REFERENCES Producto(id)
);

-- Tabla para registrar las visitas de los clientes a las sucursales
CREATE TABLE Visitan (
    idSucursal INTEGER,
    idCliente INTEGER,
    fechaVisita DATE NOT NULL,
    PRIMARY KEY (idSucursal, idCliente, fechaVisita),
    FOREIGN KEY (idSucursal) REFERENCES Sucursal(id),
    FOREIGN KEY (idCliente) REFERENCES Cliente(id)
);

-- DML para insertar datos de prueba

-- Clientes
INSERT INTO Cliente (id, nombre, apellidos, ciudad) VALUES
(1, 'Ana', 'Perez', 'Bogota'),
(2, 'Pedro', 'Gomez', 'Medellin'),
(3, 'Maria', 'Rodriguez', 'Cali');

-- Sucursales
INSERT INTO Sucursal (id, nombre, ciudad) VALUES
(101, 'Sucursal Norte', 'Bogota'),
(102, 'Sucursal Sur', 'Medellin'),
(103, 'Sucursal Centro', 'Bogota');

-- Productos
INSERT INTO Producto (id, nombre, tipoProducto) VALUES
(201, 'FPV Renta Alta', 'FPV'),
(202, 'FIC Global', 'FIC'),
(203, 'Seguro de Vida', 'Seguro');

-- Inscripciones de clientes a productos
INSERT INTO Inscripcion (idCliente, idProducto) VALUES
(1, 201), -- Ana se inscribe en 'FPV Renta Alta'
(2, 202), -- Pedro se inscribe en 'FIC Global'
(3, 203); -- Maria se inscribe en 'Seguro de Vida'

-- Disponibilidad de productos en sucursales
INSERT INTO Disponibilidad (idSucursal, idProducto) VALUES
(101, 201), -- 'FPV Renta Alta' está disponible SÓLO en Sucursal Norte
(102, 202), -- 'FIC Global' está disponible en Sucursal Sur...
(103, 202), -- ...y también en Sucursal Centro
(101, 203); -- 'Seguro de Vida' está disponible en Sucursal Norte

-- Visitas de clientes a sucursales
INSERT INTO Visitan (idCliente, idSucursal, fechaVisita) VALUES
(1, 101, '2025-08-01'), -- Ana visita la Sucursal Norte
(2, 102, '2025-08-02'), -- Pedro visita la Sucursal Sur (pero su producto también está en la Centro, que no visita)
(3, 103, '2025-08-03'); -- Maria visita la Sucursal Centro (pero su producto está en la Norte, que no visita)