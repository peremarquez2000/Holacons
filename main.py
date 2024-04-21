import pandas as pd
import sqlite3


def valores_faltantes(df):
    print(df.isnull().sum() / len(df))


if __name__ == "__main__":
    df = pd.read_csv("Sample_Data.csv")

    # valores_faltantes(df)

    conn = sqlite3.connect("Sample_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE OpCo (
            OpCo varchar PRIMARY KEY,
            OpCo_Name varchar
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE Subsidiary (
            Subsidiary varchar PRIMARY KEY,
            Subsidiary_Name varchar
        ) 
        """
    )
    cursor.execute(
        """CREATE TABLE Departure (
        Departure_Airport varchar PRIMARY KEY,
        Departure_Airport_Name varchar,
        Departure_Country varchar,
        Departure_Region varchar
        )
    """
    )

    cursor.execute(
        """CREATE TABLE Arrival (
            Arrival_Airport varchar PRIMARY KEY,
            Arrival_Airport_Name varchar,
            Arrival_Country varchar,
            Arrival_Region varchar
            )
    """
    )

    cursor.execute(
        """
        CREATE TABLE Flights (
            OpCo varchar,
            Subsidiary varchar,
            Departure varchar,
            Arrival varchar,
            Aircraft_Type varchar,
            Date varchar,
            Cabin varchar,
            Service varchar,
            NPassengers int,
            NFlights int,
            FOREIGN KEY (Opco) REFERENCES OpCo (OpCo),
            FOREIGN KEY (Subsidiary) REFERENCES Subsidiary (Subsidiary),
            FOREIGN KEY (Departure) REFERENCES Departure (Departure_Airport),
            FOREIGN KEY (Arrival) REFERENCES Arrival (Arrival_Airport)
            )
    """
    )    

    df.to_sql("Sample_data", conn, index=False, if_exists="replace")
    conn.close()


# TODO

# Tendre que definir que tipo de variable es cada columna (int, strng,..)
# Coge de la base de datos el aricraft, #passengers, #flights para saber si en realidad los datos son de vuelo unico o no
