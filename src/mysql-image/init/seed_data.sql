INSERT INTO Cuadrante (nombre) VALUES
('Cuadrante Superior Izquierdo'),
('Cuadrante Superior Derecho'),
('Cuadrante Inferior Izquierdo'),
('Cuadrante Inferior Derecho'),
('Cuadrante Central');

INSERT INTO FormaGeometrica (nombre) VALUES
('Círculo'), ('Rombo'), ('Pirámide'), ('Texto'), ('Logo'), ('Triángulo'), ('Rectángulo');

INSERT INTO Calzado (categoria, marca, modelo, talle, ancho, alto, colores, tipo_registro) VALUES
('deportivo', 'Nike', 'Air Zoom', '42', 10.5, 28.0, 'negro/blanco', 'indubitada_proveedor'),
('urbano', 'Adidas', 'Superstar', '41', 10.0, 27.5, 'blanco/negro', 'indubitada_comisaria'),
('trabajo', 'Caterpillar', 'SteelToe', '43', 11.0, 29.0, 'amarillo/negro', 'dubitada');

INSERT INTO Suela (id_calzado, descripcion_general) VALUES
(1, 'Suela con dibujo estándar para pruebas'),
(2, 'Suela con dibujo estándar para pruebas'),
(3, 'Suela con dibujo estándar para pruebas');

INSERT INTO DetalleSuela (id_suela, id_cuadrante, id_forma, detalle_adicional) VALUES
(1, 1, 1, 'Test'), (1, 2, 2, 'Test'), (1, 3, 3, 'Test'),
(2, 1, 1, 'Test'), (2, 2, 2, 'Test'), (2, 3, 3, 'Test'),
(3, 1, 1, 'Test'), (3, 2, 2, 'Test'), (3, 3, 3, 'Test');
