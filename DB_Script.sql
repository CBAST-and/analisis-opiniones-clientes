-- =============================================
-- SCRIPT DE CREACIÓN DE BASE DE DATOS
-- Sistema de Análisis de Opiniones de Clientes
-- =============================================

-- Crear la base de datos
CREATE DATABASE AnalisisOpiniones;
GO

USE AnalisisOpiniones;
GO

-- =============================================
-- TABLAS MAESTRAS (LOOKUP TABLES)
-- =============================================

-- Tabla Categorias
CREATE TABLE Categorias (
    IdCategoria INT IDENTITY(1,1) PRIMARY KEY,
    Categoria NVARCHAR(50) UNIQUE NOT NULL
);
GO

-- Tabla TiposFuente
CREATE TABLE TiposFuente (
    IdTipoFuente INT IDENTITY(1,1) PRIMARY KEY,
    TipoFuente NVARCHAR(50) UNIQUE NOT NULL
);
GO

-- Tabla FuentesSociales
CREATE TABLE FuentesSociales (
    IdFuenteSocial INT IDENTITY(1,1) PRIMARY KEY,
    NombreFuente NVARCHAR(50) UNIQUE NOT NULL
);
GO

-- Tabla Clasificaciones
CREATE TABLE Clasificaciones (
    IdClasificacion INT IDENTITY(1,1) PRIMARY KEY,
    Clasificacion NVARCHAR(20) UNIQUE NOT NULL
);
GO

-- =============================================
-- TABLAS PRINCIPALES
-- =============================================

-- Tabla Clientes
CREATE TABLE Clientes (
    IdCliente INT PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    Email NVARCHAR(100)
);
GO

-- Tabla Productos
CREATE TABLE Productos (
    IdProducto INT PRIMARY KEY,
    Nombre NVARCHAR(100) NOT NULL,
    IdCategoria INT NOT NULL,
    FOREIGN KEY (IdCategoria) REFERENCES Categorias(IdCategoria)
);
GO

-- Tabla Fuentes
CREATE TABLE Fuentes (
    IdFuente NVARCHAR(10) PRIMARY KEY,
    IdTipoFuente INT NOT NULL,
    FechaCarga DATE NOT NULL,
    FOREIGN KEY (IdTipoFuente) REFERENCES TiposFuente(IdTipoFuente)
);
GO

-- =============================================
-- TABLAS DE HECHOS (FACT TABLES)
-- =============================================

-- Tabla ComentariosSociales
CREATE TABLE ComentariosSociales (
    IdComment NVARCHAR(10) PRIMARY KEY,
    IdCliente INT NULL, -- Puede ser anónimo
    IdProducto INT NOT NULL,
    IdFuenteSocial INT NOT NULL,
    Fecha DATE NOT NULL,
    Comentario TEXT NOT NULL,
    FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
    FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto),
    FOREIGN KEY (IdFuenteSocial) REFERENCES FuentesSociales(IdFuenteSocial)
);
GO

-- Tabla Encuestas
CREATE TABLE Encuestas (
    IdOpinion INT PRIMARY KEY,
    IdCliente INT NOT NULL,
    IdProducto INT NOT NULL,
    Fecha DATE NOT NULL,
    Comentario TEXT NOT NULL,
    IdClasificacion INT NOT NULL,
    PuntajeSatisfaccion INT NOT NULL CHECK (PuntajeSatisfaccion BETWEEN 1 AND 5),
    FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
    FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto),
    FOREIGN KEY (IdClasificacion) REFERENCES Clasificaciones(IdClasificacion)
);
GO

-- Tabla ResenasWeb
CREATE TABLE ResenasWeb (
    IdReview NVARCHAR(10) PRIMARY KEY,
    IdCliente INT NOT NULL,
    IdProducto INT NOT NULL,
    Fecha DATE NOT NULL,
    Comentario TEXT NOT NULL,
    Rating INT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
    FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto)
);
GO

-- =============================================
-- INSERCIÓN DE DATOS MAESTROS
-- =============================================

-- Insertar categorías de productos
INSERT INTO Categorias (Categoria) VALUES 
('Juguetes'),
('Electrónica'),
('Ropa'),
('Hogar'),
('Deportes');
GO

-- Insertar tipos de fuente
INSERT INTO TiposFuente (TipoFuente) VALUES 
('Web'),
('CSV'),
('Red Social');
GO

-- Insertar fuentes sociales
INSERT INTO FuentesSociales (NombreFuente) VALUES 
('Instagram'),
('Twitter'),
('Facebook');
GO

-- Insertar clasificaciones
INSERT INTO Clasificaciones (Clasificacion) VALUES 
('Positiva'),
('Neutra'),
('Negativa');
GO

-- =============================================
-- CONSULTAS DE VERIFICACIÓN
-- =============================================

-- Verificar creación de tablas
SELECT 
    TABLE_NAME as Tabla,
    TABLE_TYPE as Tipo
FROM INFORMATION_SCHEMA.TABLES 
WHERE TABLE_TYPE = 'BASE TABLE'
ORDER BY TABLE_NAME;
GO

-- Verificar datos maestros insertados
SELECT 'Categorias' as Tabla, COUNT(*) as Total FROM Categorias
UNION ALL SELECT 'TiposFuente', COUNT(*) FROM TiposFuente
UNION ALL SELECT 'FuentesSociales', COUNT(*) FROM FuentesSociales
UNION ALL SELECT 'Clasificaciones', COUNT(*) FROM Clasificaciones;
GO

-- =============================================
-- ÍNDICES PARA MEJORAR RENDIMIENTO
-- =============================================

-- Índices para búsquedas frecuentes
CREATE INDEX IX_Clientes_Nombre ON Clientes(Nombre);
CREATE INDEX IX_Productos_Categoria ON Productos(IdCategoria);
CREATE INDEX IX_ComentariosSociales_Fecha ON ComentariosSociales(Fecha);
CREATE INDEX IX_Encuestas_Fecha ON Encuestas(Fecha);
CREATE INDEX IX_ResenasWeb_Fecha ON ResenasWeb(Fecha);
GO

PRINT 'Base de datos creada exitosamente';
PRINT 'Tablas: 10';
PRINT 'Registros maestros: 14';
GO