# Trabajo Fin de Master
Este proyecto se corresponde con el Trabajo Fin de Máster de Business Analytics and Big Data.

## Resumen

El proyecto consiste en evaluar la búsqueda de imágenes similares en una colección de imágenes de Pokémon a partir de una imagen introducida.

Los datos se han obtenido de [pokedex.py](https://pypi.org/project/pokedex.py/).

# Puesta en marcha

Es necesario tener instalado [Docker](https://www.docker.com/) y [Docker-Compose](https://docs.docker.com/compose/).

Para descargar las imágenes y construirlas:

```
docker-compose build
``` 

> **Atención**: la descarga de las imágenes y la instalación de las dependencias puede tardar varios minutos

Para lanzar los contenedores

```
docker-compose up
```

# Dashboard

Para acceder al dashboard: `localhost:8000`

Es necesario cargar los datos en la base de datos a partir del dump `pokemon.json` con el botón `Populate db`.

A continuación, empezar el proceso de indexación del catálogo completo de imágenes.

> **Atención**: la indexación del catálogo completo de imágenes puede tardar más de una hora

# Otros servicios

* MondoDB: `localhost:27017`
* ElasticSearch: `localhost:9200`
