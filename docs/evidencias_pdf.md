# Evidencias PDF: Entrega

Este archivo resume las capturas y textos que deben incluirse en el PDF final del taller.

## Datos generales

- Repositorio: agregar aqui el enlace publico de GitHub.
- API usada: Art Institute of Chicago API.
- Endpoint principal: https://api.artic.edu/api/v1/artworks
- Base de datos: `taller4_db`
- Coleccion: `raw_data`
- Registros cargados: 100 documentos.

## Capturas obligatorias

1. MongoDB conectado en VS Code o Compass.
2. Base de datos `taller4_db` visible.
3. Coleccion `raw_data` visible.
4. Conteo de documentos igual o superior a 100.
5. Documento RAW abierto, mostrando campos como `id`, `title`, `artist_title`, `date_start`, `department_title` y `artwork_type_title`.
6. Notebook `analisis.ipynb` ejecutado desde el inicio.
7. Validacion de 100 documentos y 100 ids unicos.
8. DataFrame con minimo 5 variables seleccionadas.
9. Tabla o salida de nulos y tipos de datos.
10. Lista de insights.
11. Grafico de torta.
12. Grafico de barras.
13. Histograma de fechas.

## Insights para redactar en el PDF

1. El conjunto analizado contiene 100 obras de arte.
2. Hay 61 artistas o autores distintos en los registros seleccionados.
3. El 79.0% de las obras tiene artista identificado.
4. El departamento con mas obras es `Applied Arts of Europe`, con 19 registros.
5. El tipo de obra mas frecuente es `Glass`, con 15 registros.
6. El lugar de origen mas frecuente es `United States`, con 19 registros.
7. El siglo mas frecuente es `Siglo 20`, con 48 obras.
8. Las fechas de inicio de las obras van desde -2055 hasta 2024.
