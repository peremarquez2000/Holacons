import pandas as pd
import sqlite3


def valores_faltantes(df):
    print(df.isnull().sum() / len(df))


def limpieza_df(df):
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
    
    #Cambios el OpCo a Vueling+
    df.loc[df["OpCoName"]=="Vueling+", 'OpCo'] = "VY+"
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

    return {
        "OpCo": OpCo,
        "Subsidiary": Subsidiary,
        "Departure": Departure,
        "Arrival": Arrival,
        "Flights": Flights,
    }


def crear_tablas_DB():
    conn = sqlite3.connect("Sample_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE OpCo (
            OpCo TEXT PRIMARY KEY,
            OpCoName TEXT
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE Subsidiary (
            Subsidiary varchar PRIMARY KEY,
            SubsidiaryName varchar
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE Departure (
            DepartureAirport varchar PRIMARY KEY,
            DepartureAirportName varchar,
            DepartureCountry varchar,
            DepartureCountryName varchar,
            DepartureRegion varchar
        )
    """
    )

    cursor.execute(
        """CREATE TABLE Arrival (
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
        CREATE TABLE Flights (
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


def llenar_tablas_DB(dict):
    conn = sqlite3.connect("Sample_data.db")
    for key in dict.keys():
        dict[key].to_sql(key, conn, if_exists="append", index=False)
    #dict["OpCo"].to_sql("OpCo", conn, if_exists="append", index=False)
    conn.close()

def df_de_sql_script(database, sql_script):
    conn = sqlite3.connect(database)
    with open(sql_script, 'r') as f:
        sql_script = f.read()
    df = pd.read_sql_query(sql_script, conn)
    conn.close()
    return df
    


if __name__ == "__main__":
    df = pd.read_csv("Sample_Data.csv")
    df_dict = limpieza_df(df)
    #crear_tablas_DB()
    #llenar_tablas_DB(df_dict)
    df_query=df_de_sql_script("Sample_data.db", "script.sql")
    print(df_query.head())


# TODO

# Tendre que definir que tipo de variable es cada columna (int, strng,..)
