# Taller 4 - API publica, MongoDB y EDA

Proyecto individual para desarrollar un flujo basico de Ciencia de Datos:

1. Consumir una API publica.
2. Guardar datos crudos en MongoDB.
3. Realizar un analisis exploratorio en Jupyter Notebook.

## API seleccionada

Se utiliza la API publica del **Art Institute of Chicago**:

- Sitio de documentacion: https://api.artic.edu/docs/
- Endpoint usado: `https://api.artic.edu/api/v1/artworks`
- Tema de los datos: obras de arte, artistas, fechas, departamentos, tipos de obra y lugares de origen.

Esta API no requiere token y permite obtener mas de 100 registros mediante paginacion.

## Estructura del proyecto

```text
taller4_art_institute/
  .env.example
  .gitignore
  README.md
  requirements.txt
  ingesta.py
  analisis.ipynb
  data/
    .gitkeep
```

## Requisitos

- Python 3.10 o superior
- MongoDB local en ejecucion
- VS Code
- Extension de Python y Jupyter en VS Code

## Configuracion del entorno

Desde la carpeta del proyecto:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

El archivo `.env.example` ya trae los valores solicitados por el taller:

```text
MONGO_DB=taller4_db
MONGO_COLLECTION=raw_data
```

## Ejecucion de la ingesta

Con MongoDB abierto o ejecutandose en local:

```powershell
python ingesta.py
```

El script descarga minimo 100 obras desde la API y guarda cada documento JSON crudo en:

- Base de datos: `taller4_db`
- Coleccion: `raw_data`

## Analisis exploratorio

Abrir el notebook:

```text
analisis.ipynb
```

El notebook se conecta a MongoDB, lee la coleccion `raw_data`, crea un DataFrame con variables relevantes y desarrolla:

- Inspeccion inicial con `head`, `info` y revision de nulos.
- Minimo 5 insights numericos o conteos.
- 3 graficos:
  - 1 grafico de torta.
  - 2 graficos libres.

## Checklist de entrega

- [ ] Repositorio publico en GitHub.
- [ ] `README.md` completo.
- [ ] `requirements.txt` funcional.
- [ ] `ingesta.py` con minimo 100 registros.
- [ ] Base de datos `taller4_db`.
- [ ] Coleccion `raw_data`.
- [ ] `analisis.ipynb` documentado.
- [ ] 5 insights.
- [ ] 3 graficos.
- [ ] Minimo 5 commits.
- [ ] PDF con enlace al repositorio y evidencias.
