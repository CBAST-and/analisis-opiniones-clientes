# Sistema de Análisis de Opiniones de Clientes

## 📋 Descripción del Proyecto
Pipeline ETL para el procesamiento y análisis de opiniones de clientes provenientes de múltiples fuentes (web, redes sociales, encuestas).

## 🏗️ Estructura del Proyecto

```
analisis_opiniones/
├── data/
│ ├── clients.csv
│ ├── products.csv
│ ├── fuente_datos.csv
│ ├── social_comments.csv
│ ├── surveys_part1.csv
│ └── web_reviews.csv
├── database.py
├── main.py
├── DB_Script.sql
├── requirements.txt
└── README.md
```

## Requisitos
- Python 3.8+
- SQL Server
- pandas, pyodbc, python-dotenv

## Instalación
```bash
pip install -r requirements.txt
```

## Uso
```python 
main.py
```

## Modelo de Datos
- Clientes (IdCliente) ← ComentariosSociales → Productos (IdProducto)
- Clientes (IdCliente) ← Encuestas → Productos (IdProducto)
- Clientes (IdCliente) ← ResenasWeb → Productos (IdProducto)
- Productos (IdProducto) → Categorias (IdCategoria)
- Fuentes (IdFuente) → TiposFuente (IdTipoFuente)

### Diagrama Entidad-Relacion

```mermaid
erDiagram
    Clientes {
        int IdCliente PK
        varchar Nombre
        varchar Email
    }
    
    Categorias {
        int IdCategoria PK
        varchar Categoria
    }
    
    Productos {
        int IdProducto PK
        varchar Nombre
        int IdCategoria FK
    }
    
    TiposFuente {
        int IdTipoFuente PK
        varchar TipoFuente
    }
    
    Fuentes {
        varchar IdFuente PK
        int IdTipoFuente FK
        date FechaCarga
    }
    
    FuentesSociales {
        int IdFuenteSocial PK
        varchar NombreFuente
    }
    
    Clasificaciones {
        int IdClasificacion PK
        varchar Clasificacion
    }
    
    ComentariosSociales {
        varchar IdComment PK
        int IdCliente FK
        int IdProducto FK
        int IdFuenteSocial FK
        date Fecha
        text Comentario
    }
    
    Encuestas {
        int IdOpinion PK
        int IdCliente FK
        int IdProducto FK
        date Fecha
        text Comentario
        int IdClasificacion FK
        int PuntajeSatisfaccion
    }
    
    ReseñasWeb {
        varchar IdReview PK
        int IdCliente FK
        int IdProducto FK
        date Fecha
        text Comentario
        int Rating
    }

    Productos ||--o{ Categorias : pertenece_a
    Fuentes ||--o{ TiposFuente : tiene_tipo
    ComentariosSociales }o--|| Clientes : realizado_por
    ComentariosSociales }o--|| Productos : sobre_producto
    ComentariosSociales }o--|| FuentesSociales : desde_fuente
    Encuestas }o--|| Clientes : realizada_por
    Encuestas }o--|| Productos : evalua_producto
    Encuestas }o--|| Clasificaciones : tiene_clasificacion
    ReseñasWeb }o--|| Clientes : escrita_por
    ReseñasWeb }o--|| Productos : reseña_producto
  
```

# Informe Técnico - Pipeline ETL

## 1. Diseño de Base de Datos
Modelo relacional normalizado con 10 tablas.

## 2. Pipeline ETL
### Extracción
6 archivos CSV - 1,700 registros

### Transformación
Limpieza y normalización de datos

### Carga
Inserción en SQL Server - 816 registros

## 3. Tecnologías
Python, SQL Server, pandas

## 4. Resultados
Proceso ejecutado exitosamente
