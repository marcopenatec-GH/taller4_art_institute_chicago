# Taller 4 - API publica, MongoDB y EDA

Proyecto individual para desarrollar un flujo basico de Ciencia de Datos:

1. Consumir una API publica.
2. Guardar datos crudos en MongoDB.
3. Realizar un analisis exploratorio en Jupyter Notebook.

El proyecto sigue la logica de un pipeline simple: **extract -> raw -> transform -> EDA**.
No se incluye una carga a MySQL porque el instructivo de esta actividad pide conservar los
datos crudos en MongoDB y analizarlos desde un notebook.

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

## Pipeline del proyecto

| Etapa | Archivo o herramienta | Proposito |
| --- | --- | --- |
| Extract | `ingesta.py` | Consumir la API publica con paginacion. |
| Raw | MongoDB `taller4_db.raw_data` | Guardar el JSON crudo sin transformar para trazabilidad. |
| Transform | `analisis.ipynb` | Seleccionar columnas, limpiar nulos, tipificar variables y crear variables auxiliares. |
| EDA | `analisis.ipynb` | Calcular insights y generar graficos para interpretar los datos. |

## Principios aplicados

- **Reproducibilidad**: el proyecto usa `.env.example` y `requirements.txt` para repetir la ejecucion.
- **Observabilidad**: `ingesta.py` muestra logs con fuente, destino, paginas procesadas y conteo final.
- **Bajo acoplamiento**: la ingesta, la conexion y la validacion estan separadas en funciones pequenas.
- **Idempotencia**: si se ejecuta de nuevo, `replace_one(..., upsert=True)` actualiza por `id` y evita duplicados.
- **Trazabilidad**: MongoDB conserva el dato crudo de la API antes de cualquier transformacion.
- **Validacion post-carga**: el script comprueba que existan al menos 100 documentos en `raw_data`.

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

Al finalizar, el script muestra una validacion post-carga con:

- Total de documentos en la coleccion.
- Cantidad de `id` unicos.
- Muestra de campos disponibles en el documento RAW.

## Analisis exploratorio

Abrir el notebook:

```text
analisis.ipynb
```

El notebook se conecta a MongoDB, lee la coleccion `raw_data`, crea un DataFrame con variables relevantes y desarrolla:

- Validacion de que MongoDB tenga minimo 100 registros.
- Revision de duplicados por `id`.
- Diccionario de variables seleccionadas.
- Limpieza y transformacion minima para analisis.
- Inspeccion inicial con `head`, `info` y revision de nulos.
- Minimo 5 insights numericos o conteos.
- 3 graficos:
  - 1 grafico de torta.
  - 2 graficos libres.

Las transformaciones se hacen en el notebook para respetar el principio del taller:
MongoDB conserva el dato RAW y Pandas crea una vista curada para EDA.

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
