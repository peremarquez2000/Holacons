# HOLACONS
El programa recibe un fichero "csv" el cual se encarga de limpiar los datos, crea un modelo de datos en la base de datos de SQLite y finalmente muestra por terminal la query pedida en el ejercicio.


## Requisitos
Tener instalado [Poetry](https://python-poetry.org/docs/) (disponible tanto para windows/mac/linux)
## Ejecución
Para ejecutar el codigo ejecuta los siguientes comandos
```bash
poetry install
poetry shell --no-root
python main.py
```

## Modelo ER 
![alt text](<ER model.png>)
## Recomendaciones 
Para poder visualizar la base de datos he usado la herramienta [DBeaver](https://dbeaver.io/download/).

## Advertencia
El codigo crea una base de datos y unas tablas durante el proceso. Como las tablas estan creadas con PRIMARY KEYS y la ingesta de datos a estas tablas si se hace más de una vez introduce valores repetidos, el programa se queja.

Por tanto, este script esta diseñado para ejecutarse una única vez.


<!-- # Analizemos primero cual es el proceso mental seguido para hacer este ejercicio.

Primero de todo fijemonos en que consiste el fichero excel. Si nos fijamos, el fichero excel tiene diversas columnas pero hay una que se mantiene contante que si que es fija para todas las lineas. Esta columna fija es "Date". 

Por tanto, se entiende que el fichero consiste en todos los vuelos que se han hecho en un mismo dia. -->

