import pandas as pd
import sqlite3


def lectura_de_datos(csv):
    print("Leyendo datos...")
    dtype_dict = {
        "OpCo": str,
        "OpCo Name": str,
        "Subsidiary": str,
        "Subsidiary Name": str,
        "Departure Airport": str,
        "Departure Airport Name": str,
        "Departure Country": str,
        "Departure Country Name": str,
        "Departure Region": str,
        "Arrival Airport": str,
        "Arrival Airport Name": str,
        "Arrival Country": str,
        "Arrival Country Name": str,
        "Arrival Region": str,
        "Aircraft type": str,
        "Date": str,
        "Cabin": str,
        "Service": str,
        "# Passengers": int,
        "# Flights": int,
    }

    df = pd.read_csv(csv, dtype=dtype_dict)
    print("Datos leídos.")
    return df


def limpieza_df(df):
    print("Limpiando Datos...")
    df.columns = [
        "OpCo",
        "OpCoName",
        "Subsidiary",
        "SubsidiaryName",
        "DepartureAirport",
        "DepartureAirportName",
        "DepartureCountry",
        "DepartureCountryName",
        "DepartureRegion",
        "ArrivalAirport",
        "ArrivalAirportName",
        "ArrivalCountry",
        "ArrivalCountryName",
        "ArrivalRegion",
        "AircraftType",
        "Date",
        "Cabin",
        "Service",
        "NPassengers",
        "NFlights",
    ]

    # Definimos que tipo de variables queremos para cada una de nuestras columnas

    dtype_dict = {
        "OpCo": str,
        "OpCoName": str,
        "Subsidiary": str,
        "SubsidiaryName": str,
        "DepartureAirport": str,
        "DepartureAirportName": str,
        "DepartureCountry": str,
        "DepartureCountryName": str,
        "DepartureRegion": str,
        "ArrivalAirport": str,
        "ArrivalAirportName": str,
        "ArrivalCountry": str,
        "ArrivalCountryName": str,
        "ArrivalRegion": str,
        "AircraftType": str,
        "Date": str,
        "Cabin": str,
        "Service": str,
        "NPassengers": int,
        "NFlights": int,
    }

    # Eliminamos en el caso que haya filas repetidas
    df.drop_duplicates(inplace=True)

    # Me aseguro que no hay numeros enteros en las columnas de caracteres.
    # Nota: Pensaba que se habian colado valores sueltos como en Aircraft el valor "747" (mas tarde me he dado cuenta que era un tipo de Aircraft)
    # y pensaba que se tenian que limpiar. He creado la funcion "es_numero" que encuentra si a alguna valor se le puede aplicar la funcion int()
    # que significaria que es un valor entero que se ha colado en una columna de strings y entonces estos valores los substituia por
    # el valor None. Esta funcion ("elmina_valores_enteros") solo se aplica para las columnas no numericas (ni para el numero de pasajeros ni para el numero de vuelos)

    # df=elimina_valores_enteros(df)

    # Cambio los OpCo que tienen como OpCoName "Vueling+"
    df.loc[df["OpCoName"] == "Vueling+", "OpCo"] = "VY+"

    OpCo = df[
        [
            "OpCo",
            "OpCoName",
        ]
    ].drop_duplicates()

    Subsidiary = df[
        [
            "Subsidiary",
            "SubsidiaryName",
        ]
    ].drop_duplicates()

    Departure = df[
        [
            "DepartureAirport",
            "DepartureAirportName",
            "DepartureCountry",
            "DepartureCountryName",
            "DepartureRegion",
        ]
    ].drop_duplicates()

    Arrival = df[
        [
            "ArrivalAirport",
            "ArrivalAirportName",
            "ArrivalCountry",
            "ArrivalCountryName",
            "ArrivalRegion",
        ]
    ].drop_duplicates()

    Flights = df[
        [
            "OpCo",
            "Subsidiary",
            "DepartureAirport",
            "ArrivalAirport",
            "AircraftType",
            "Date",
            "Cabin",
            "Service",
            "NPassengers",
            "NFlights",
        ]
    ]

    print("Datos limpios.")
    return {
        "OpCo": OpCo,
        "Subsidiary": Subsidiary,
        "Departure": Departure,
        "Arrival": Arrival,
        "Flights": Flights,
    }


def crear_tablas_DB():
    print("Creando base de datos y tablas...")
    conn = sqlite3.connect("Sample_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS OpCo (
            OpCo TEXT PRIMARY KEY,
            OpCoName TEXT
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Subsidiary (
            Subsidiary varchar PRIMARY KEY,
            SubsidiaryName varchar
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Departure (
            DepartureAirport varchar PRIMARY KEY,
            DepartureAirportName varchar,
            DepartureCountry varchar,
            DepartureCountryName varchar,
            DepartureRegion varchar
        )
    """
    )

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS Arrival (
            ArrivalAirport varchar PRIMARY KEY,
            ArrivalAirportName varchar,
            ArrivalCountry varchar,
            ArrivalCountryName varchar,
            ArrivalRegion varchar
            )
    """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Flights (
            OpCo varchar,
            Subsidiary varchar,
            DepartureAirport varchar,
            ArrivalAirport varchar,
            AircraftType varchar,
            Date varchar,
            Cabin varchar,
            Service varchar,
            "NPassengers" int,
            "NFlights" int,
            FOREIGN KEY (OpCo) REFERENCES OpCo (OpCo),
            FOREIGN KEY (Subsidiary) REFERENCES Subsidiary (Subsidiary),
            FOREIGN KEY (DepartureAirport) REFERENCES Departure (DepartureAirport),
            FOREIGN KEY (ArrivalAirport) REFERENCES Arrival (ArrivalAirport)
            )
    """
    )
    conn.commit()
    conn.close()
    print("Base de datos y tablas Creadas.")


def llenar_tablas_DB(dict):
    print("Llenando tablas de la base de datos...")
    with sqlite3.connect("Sample_data.db") as conn:
        for key in dict.keys():
            dict[key].to_sql(key, conn, if_exists="append", index=False)
    print("Datos introducidos.")


def df_de_SQL_script(database, sql_script):
    print("Convirtiendo Query de SQL a Dataframe...")
    with open(sql_script, "r") as f:
        sql_script = f.read()
    with sqlite3.connect(database) as conn:
        df = pd.read_sql_query(sql_script, conn)
    print("Dataframe obtenido.")
    return df


def es_numero(valor):
    try:
        int(valor)
        return True
    except ValueError:
        return False


def elimina_valores_enteros(df):
    print("Eliminando valores enteros...")
    for columna in df.columns:
        if columna not in ["NPassengers", "NFlights"]:
            mask = df[columna].apply(es_numero)
            df.loc[mask, columna] = None
    print("Valores eliminados.")
    return df


if __name__ == "__main__":
    df = lectura_de_datos("Sample_Data.csv")
    df_dict = limpieza_df(df)
    crear_tablas_DB()
    llenar_tablas_DB(df_dict)
    df_query = df_de_SQL_script("Sample_data.db", "script.sql")
    print(df_query)
