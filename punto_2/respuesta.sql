SELECT DISTINCT c.nombre, c.apellidos
FROM Cliente c
JOIN Inscripcion i ON c.id = i.idCliente
WHERE
    -- La siguiente subconsulta verifica que NO EXISTA una sucursal
    -- donde el producto esté disponible y que el cliente NO haya visitado.
    NOT EXISTS (
        SELECT 1
        FROM Disponibilidad d
        WHERE
            d.idProducto = i.idProducto
            AND d.idSucursal NOT IN (
                SELECT v.idSucursal
                FROM Visitan v
                WHERE v.idCliente = c.id
            )
    )
    -- confirmar que el cliente haya visitado
    -- al menos una sucursal donde su producto está disponible.
    AND EXISTS (
        SELECT 1
        FROM Visitan v
        JOIN Disponibilidad d ON v.idSucursal = d.idSucursal
        WHERE v.idCliente = c.id AND d.idProducto = i.idProducto
    );