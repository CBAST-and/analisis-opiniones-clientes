import pandas as pd
import os
from datetime import datetime
from database import SQLServerManager


def limpiar_dataframe(df, nombre_df):
    """Limpieza general de cualquier dataframe"""
    print("Limpiando " + nombre_df + "...")

    # Eliminar duplicados
    original_count = len(df)
    df = df.drop_duplicates()
    duplicados = original_count - len(df)
    if duplicados > 0:
        print("Eliminados " + str(duplicados) + " duplicados")

    # Verificar y contar nulos en columnas clave
    columnas_con_nulos = df.columns[df.isnull().any()].tolist()
    if columnas_con_nulos:
        print("Columnas con valores nulos: " + ", ".join(columnas_con_nulos))

    return df


def limpiar_clientes(df):
    """Limpieza específica para clientes"""
    df = limpiar_dataframe(df, "clientes")

    # Asegurar tipo de dato
    df['IdCliente'] = df['IdCliente'].astype(int)

    print("Clientes limpios: " + str(len(df)) + " registros")
    return df


def limpiar_productos(df):
    """Limpieza específica para productos"""
    df = limpiar_dataframe(df, "productos")

    # Asegurar tipo de dato
    df['IdProducto'] = df['IdProducto'].astype(int)

    print("Productos limpios: " + str(len(df)) + " registros")
    return df


def limpiar_fuente_datos(df):
    """Limpieza específica para fuente_datos"""
    df = limpiar_dataframe(df, "fuente_datos")

    # Asegurar tipo de dato
    df['IdFuente'] = df['IdFuente'].astype(str)

    print("Fuente datos limpios: " + str(len(df)) + " registros")
    return df


def limpiar_comentarios_sociales(df):
    """Limpieza específica para comentarios sociales"""
    df = limpiar_dataframe(df, "comentarios sociales")

    # Manejar clientes nulos (pueden ser comentarios anónimos)
    if df['IdCliente'].isnull().any():
        nulos = df['IdCliente'].isnull().sum()
        print("Comentarios sociales sin cliente: " + str(nulos))

    print("Comentarios sociales limpios: " + str(len(df)) + " registros")
    return df


def limpiar_encuestas(df):
    """Limpieza específica para encuestas"""
    df = limpiar_dataframe(df, "encuestas")

    # Asegurar tipos de datos
    df['IdOpinion'] = df['IdOpinion'].astype(int)
    df['IdCliente'] = df['IdCliente'].astype(int)
    df['IdProducto'] = df['IdProducto'].astype(int)
    df['PuntajeSatisfacción'] = df['PuntajeSatisfacción'].astype(int)

    print("Encuestas limpias: " + str(len(df)) + " registros")
    return df


def limpiar_resenas_web(df):
    """Limpieza específica para reseñas web"""
    df = limpiar_dataframe(df, "reseñas web")

    # Asegurar tipos de datos
    df['IdReview'] = df['IdReview'].astype(str)
    df['IdCliente'] = df['IdCliente'].astype(str)
    df['IdProducto'] = df['IdProducto'].astype(str)
    df['Rating'] = df['Rating'].astype(int)

    print("Reseñas web limpias: " + str(len(df)) + " registros")
    return df


def limpiar_fechas(df, columna_fecha):
    """Normalizar formato de fechas"""
    if columna_fecha in df.columns:
        df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
        # Contar fechas inválidas
        fechas_invalidas = df[columna_fecha].isnull().sum()
        if fechas_invalidas > 0:
            print("Fechas invalidas en " + columna_fecha + ": " + str(fechas_invalidas))
    return df


def main():
    print("Iniciando proyecto de analisis de opiniones")
    print("==========================================")

    # FASE 1: EXTRACCION
    print("FASE 1 - EXTRACCION")
    print("Verificando archivos CSV...")

    archivos = {
        'clients': 'data/clients.csv',
        'products': 'data/products.csv',
        'fuente_datos': 'data/fuente_datos.csv',
        'social_comments': 'data/social_comments.csv',
        'surveys_part1': 'data/surveys_part1.csv',
        'web_reviews': 'data/web_reviews.csv'
    }

    dataframes = {}

    for nombre, archivo in archivos.items():
        if os.path.exists(archivo):
            dataframes[nombre] = pd.read_csv(archivo)
            print("Leido: " + archivo + " - " + str(len(dataframes[nombre])) + " registros")
        else:
            print("No encontrado: " + archivo)
            return

    print("==========================================")

    # FASE 2: TRANSFORMACION
    print("FASE 2 - TRANSFORMACION")

    # Aplicar limpieza específica para cada tipo de dato
    if 'clients' in dataframes:
        dataframes['clients'] = limpiar_clientes(dataframes['clients'])

    if 'products' in dataframes:
        dataframes['products'] = limpiar_productos(dataframes['products'])

    if 'fuente_datos' in dataframes:
        dataframes['fuente_datos'] = limpiar_fuente_datos(dataframes['fuente_datos'])

    if 'social_comments' in dataframes:
        dataframes['social_comments'] = limpiar_comentarios_sociales(dataframes['social_comments'])

    if 'surveys_part1' in dataframes:
        dataframes['surveys_part1'] = limpiar_encuestas(dataframes['surveys_part1'])

    if 'web_reviews' in dataframes:
        dataframes['web_reviews'] = limpiar_resenas_web(dataframes['web_reviews'])

    # Limpiar fechas en todos los dataframes
    for nombre, df in dataframes.items():
        for columna_fecha in ['Fecha', 'FechaCarga']:
            if columna_fecha in df.columns:
                dataframes[nombre] = limpiar_fechas(df, columna_fecha)

    print("==========================================")

    # Resumen final de transformación
    print("RESUMEN FINAL - DATOS TRANSFORMADOS:")
    for nombre, df in dataframes.items():
        print(nombre.upper() + ": " + str(len(df)) + " registros")

    print("==========================================")

    # FASE 3: CARGA
    print("FASE 3 - CARGA EN SQL SERVER")

    # Conectar a SQL Server
    db_manager = SQLServerManager()

    if db_manager.test_connection():
        print("Iniciando carga de datos...")

        # 1. Insertar datos maestros (categorías, tipos, etc.)
        if db_manager.insertar_datos_maestros():
            print("Datos maestros insertados correctamente")
        else:
            print("Error insertando datos maestros")
            return

        # 2. Cargar clientes
        if db_manager.cargar_clientes(dataframes['clients']):
            print("Clientes cargados correctamente")
        else:
            print("Error cargando clientes")
            return

        # 3. Cargar productos
        if db_manager.cargar_productos(dataframes['products']):
            print("Productos cargados correctamente")
        else:
            print("Error cargando productos")
            return

        # 4. Cargar fuentes de datos
        if db_manager.cargar_fuentes_datos(dataframes['fuente_datos']):
            print("Fuentes de datos cargadas correctamente")
        else:
            print("Error cargando fuentes de datos")
            return

        print("==========================================")
        print("CARGA DE DATOS COMPLETADA EXITOSAMENTE")
        print("Resumen de tablas cargadas:")
        print("- Categorias: 5 registros")
        print("- TiposFuente: 3 registros")
        print("- FuentesSociales: 3 registros")
        print("- Clasificaciones: 3 registros")
        print("- Clientes: " + str(len(dataframes['clients'])) + " registros")
        print("- Productos: " + str(len(dataframes['products'])) + " registros")
        print("- Fuentes: " + str(len(dataframes['fuente_datos'])) + " registros")

        # Cerrar conexión
        db_manager.close_connection()

    else:
        print("No se pudo conectar a la base de datos")
        return

    print("==========================================")
    print("PROCESO ETL COMPLETADO EXITOSAMENTE")
    print("Total de fases completadas: 3/3")
    print("Extracción: Completado "
          "Transformación: Completado "
          "Carga: Completado")


if __name__ == "__main__":
    main()