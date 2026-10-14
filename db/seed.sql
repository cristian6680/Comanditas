-- ===================================================
-- ARCHIVO: db/seed.sql
-- DESCRIPCIÓN: Datos iniciales de prueba para Comanditas
-- ===================================================

-- 1. Insertar Categorías principales
INSERT INTO categorias (nombre, descripcion) VALUES
('Pizzas a la Piedra', 'Pizzas artesanales al horno de barro'),
('Empanadas', 'Empanadas tradicionales'),
('Bebidas', 'Gaseosas, aguas y cervezas bien frías')
ON CONFLICT (nombre) DO NOTHING;

-- 2. Insertar Productos del menú
INSERT INTO productos (categoria_id, nombre, descripcion, precio, disponible) VALUES
(1, 'Muzzarella Familiar', 'Salsa de tomate, muzzarella y orégano', 8500.00, TRUE),
(1, 'Fugazzeta Especial', 'Muzzarella, cebolla y jamón', 9800.00, TRUE),
(2, 'Empanada Carne Cuchillo', 'Carne cortada a cuchillo, suave', 1200.00, TRUE),
(2, 'Empanada Jamón y Queso', 'Jamón cocido y muzzarella', 1100.00, TRUE),
(3, 'Coca-Cola 1.5L', 'Gaseosa botella 1.5 Litros', 3200.00, TRUE);

-- 3. Insertar Usuario de prueba
INSERT INTO usuarios (nombre, email, password_hash, rol) VALUES
('Carlos Mozo', 'carlos@comanditas.local', 'hash_simulado_12345', 'mozo')
ON CONFLICT (email) DO NOTHING;
