import pyodbc
import os
from dotenv import load_dotenv

load_dotenv()


class SQLServerManager:
    def __init__(self):
        self.connection = self._create_connection()

    def _create_connection(self):
        """Crear conexión a SQL Server con Windows Authentication"""
        try:
            connection_string = (
                f"DRIVER={os.getenv('DB_DRIVER', 'ODBC Driver 17 for SQL Server')};"
                f"SERVER={os.getenv('DB_SERVER', 'DESKTOP-JPRJFOK')};"
                f"DATABASE={os.getenv('DB_DATABASE', 'AnalisisOpiniones')};"
                "Trusted_Connection=yes;"
            )

            connection = pyodbc.connect(connection_string)
            print("Conexión a SQL Server exitosa (Windows Authentication)")
            return connection
        except Exception as e:
            print(f"Error conectando a SQL Server: {e}")
            return None

    def test_connection(self):
        """Probar la conexión"""
        if self.connection:
            try:
                cursor = self.connection.cursor()
                cursor.execute("SELECT DB_NAME() as CurrentDatabase")
                db_name = cursor.fetchone()[0]
                print(f"Conexión exitosa. Base de datos actual: {db_name}")
                return True
            except Exception as e:
                print(f"Error probando conexión: {e}")
                return False
        return False

    def execute_query(self, query, params=None):
        """Ejecutar consulta SQL"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Exception as e:
            print(f"Error ejecutando consulta: {e}")
            return None

    def create_tables(self):
        """Crear las tablas según nuestro diseño normalizado"""
        print("Creando tablas en SQL Server...")

        tables_sql = """
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Categorias' AND xtype='U')
        CREATE TABLE Categorias (
            IdCategoria INT IDENTITY(1,1) PRIMARY KEY,
            Categoria NVARCHAR(50) UNIQUE NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Clientes' AND xtype='U')
        CREATE TABLE Clientes (
            IdCliente INT PRIMARY KEY,
            Nombre NVARCHAR(100) NOT NULL,
            Email NVARCHAR(100)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Productos' AND xtype='U')
        CREATE TABLE Productos (
            IdProducto INT PRIMARY KEY,
            Nombre NVARCHAR(100) NOT NULL,
            IdCategoria INT,
            FOREIGN KEY (IdCategoria) REFERENCES Categorias(IdCategoria)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='TiposFuente' AND xtype='U')
        CREATE TABLE TiposFuente (
            IdTipoFuente INT IDENTITY(1,1) PRIMARY KEY,
            TipoFuente NVARCHAR(50) UNIQUE NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Fuentes' AND xtype='U')
        CREATE TABLE Fuentes (
            IdFuente NVARCHAR(10) PRIMARY KEY,
            IdTipoFuente INT,
            FechaCarga DATE,
            FOREIGN KEY (IdTipoFuente) REFERENCES TiposFuente(IdTipoFuente)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='FuentesSociales' AND xtype='U')
        CREATE TABLE FuentesSociales (
            IdFuenteSocial INT IDENTITY(1,1) PRIMARY KEY,
            NombreFuente NVARCHAR(50) UNIQUE NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Clasificaciones' AND xtype='U')
        CREATE TABLE Clasificaciones (
            IdClasificacion INT IDENTITY(1,1) PRIMARY KEY,
            Clasificacion NVARCHAR(20) UNIQUE NOT NULL
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ComentariosSociales' AND xtype='U')
        CREATE TABLE ComentariosSociales (
            IdComment NVARCHAR(10) PRIMARY KEY,
            IdCliente INT,
            IdProducto INT,
            IdFuenteSocial INT,
            Fecha DATE,
            Comentario TEXT,
            FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
            FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto),
            FOREIGN KEY (IdFuenteSocial) REFERENCES FuentesSociales(IdFuenteSocial)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Encuestas' AND xtype='U')
        CREATE TABLE Encuestas (
            IdOpinion INT PRIMARY KEY,
            IdCliente INT,
            IdProducto INT,
            Fecha DATE,
            Comentario TEXT,
            IdClasificacion INT,
            PuntajeSatisfaccion INT,
            FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
            FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto),
            FOREIGN KEY (IdClasificacion) REFERENCES Clasificaciones(IdClasificacion)
        );

        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ResenasWeb' AND xtype='U')
        CREATE TABLE ResenasWeb (
            IdReview NVARCHAR(10) PRIMARY KEY,
            IdCliente INT,
            IdProducto INT,
            Fecha DATE,
            Comentario TEXT,
            Rating INT,
            FOREIGN KEY (IdCliente) REFERENCES Clientes(IdCliente),
            FOREIGN KEY (IdProducto) REFERENCES Productos(IdProducto)
        );
        """

        try:
            self.execute_query(tables_sql)
            print("Tablas creadas exitosamente")
            return True
        except Exception as e:
            print(f"Error creando tablas: {e}")
            return False

    def insertar_datos_maestros(self):
        """Insertar datos en tablas maestras (categorías, tipos, etc.)"""
        print("Insertando datos maestros...")

        try:
            # Datos para tabla Categorias
            categorias = ['Juguetes', 'Electrónica', 'Ropa', 'Hogar', 'Deportes']
            for categoria in categorias:
                self.execute_query("INSERT INTO Categorias (Categoria) VALUES (?)", (categoria,))

            # Datos para tabla TiposFuente
            tipos_fuente = ['Web', 'CSV', 'Red Social']
            for tipo in tipos_fuente:
                self.execute_query("INSERT INTO TiposFuente (TipoFuente) VALUES (?)", (tipo,))

            # Datos para tabla FuentesSociales
            fuentes_sociales = ['Instagram', 'Twitter', 'Facebook']
            for fuente in fuentes_sociales:
                self.execute_query("INSERT INTO FuentesSociales (NombreFuente) VALUES (?)", (fuente,))

            # Datos para tabla Clasificaciones
            clasificaciones = ['Positiva', 'Neutra', 'Negativa']
            for clasif in clasificaciones:
                self.execute_query("INSERT INTO Clasificaciones (Clasificacion) VALUES (?)", (clasif,))

            print("Datos maestros insertados")
            return True
        except Exception as e:
            print(f"Error insertando datos maestros: {e}")
            return False

    def cargar_clientes(self, dataframe):
        """Cargar datos de clientes desde el DataFrame"""
        print("Cargando clientes...")

        try:
            for _, row in dataframe.iterrows():
                self.execute_query(
                    "INSERT INTO Clientes (IdCliente, Nombre, Email) VALUES (?, ?, ?)",
                    (int(row['IdCliente']), str(row['Nombre']), str(row['Email']))
                )

            print(f"Clientes cargados: {len(dataframe)} registros")
            return True
        except Exception as e:
            print(f"Error cargando clientes: {e}")
            return False

    def cargar_productos(self, dataframe):
        """Cargar datos de productos desde el DataFrame"""
        print("Cargando productos...")

        try:
            # Primero necesitamos mapear categorías a IDs
            cursor = self.connection.cursor()
            cursor.execute("SELECT IdCategoria, Categoria FROM Categorias")
            categorias_map = {row[1]: row[0] for row in cursor.fetchall()}

            for _, row in dataframe.iterrows():
                categoria_id = categorias_map.get(row['Categoría'])
                if categoria_id:
                    self.execute_query(
                        "INSERT INTO Productos (IdProducto, Nombre, IdCategoria) VALUES (?, ?, ?)",
                        (int(row['IdProducto']), str(row['Nombre']), categoria_id)
                    )

            print(f"Productos cargados: {len(dataframe)} registros")
            return True
        except Exception as e:
            print(f"Error cargando productos: {e}")
            return False

    def cargar_fuentes_datos(self, dataframe):
        """Cargar datos de fuentes desde el DataFrame"""
        print("Cargando fuentes de datos...")

        try:
            # Mapear tipos de fuente a IDs
            cursor = self.connection.cursor()
            cursor.execute("SELECT IdTipoFuente, TipoFuente FROM TiposFuente")
            tipos_map = {row[1]: row[0] for row in cursor.fetchall()}

            for _, row in dataframe.iterrows():
                tipo_id = tipos_map.get(row['TipoFuente'])
                if tipo_id:
                    self.execute_query(
                        "INSERT INTO Fuentes (IdFuente, IdTipoFuente, FechaCarga) VALUES (?, ?, ?)",
                        (str(row['IdFuente']), tipo_id, row['FechaCarga'])
                    )

            print(f"Fuentes cargadas: {len(dataframe)} registros")
            return True
        except Exception as e:
            print(f"Error cargando fuentes: {e}")
            return False

    def get_id_from_table(self, table_name, id_column, value_column, value):
        """Obtener ID de una tabla basado en un valor"""
        try:
            cursor = self.connection.cursor()
            query = f"SELECT {id_column} FROM {table_name} WHERE {value_column} = ?"
            cursor.execute(query, (value,))
            result = cursor.fetchone()
            return result[0] if result else None
        except Exception as e:
            print(f"Error obteniendo ID de {table_name}: {e}")
            return None

    def close_connection(self):
        """Cerrar conexión a la base de datos"""
        if self.connection:
            self.connection.close()
            print("Conexión cerrada")