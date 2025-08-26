# Trabajo práctico de Operación de Aprendizaje de Maquina I (MLOps1)

## Equipo
El grupo nuestro se encuentra conformado por:
- Querales, Gabriel
- Rodríguez, Joaquín
- Martín, Matías

## Predicción de ventas de videojuegos en Steam
En este proyecto implementamos un flujo de trabajo y despliegue completo para predecir ventas de videojuegos en Steam. Dentro de este flujo se integro:

1. Orquestación de ETL y reentrenamiento con Apache Airflow para automatizar el procesamiento de datos y actualización del modelo.
2. Almacenamiento de datos y artefactos en MinIO como sistema de almacenamiento compatible con S3.
3. Seguimiento de experimentos y versionado de modelos en MLflow para mantener registro del entrenamiento.
4. API REST desarrollada con FastAPI con endpoints para acceder a predicciones y registro de ellas.
5. Swagger para documentar y validar la API con una interfaz dinamica.
6. Frontend implementado con Streamlit que permite realizar predicciones y visualizar registros históricos.
7. Despliegue containerizado mediante Docker Compose que facilita el lanzamiento de todos los servicios.

## Automatizacion del flujo de trabajo
Mediante el uso de las diversas herramientas del proyecto se logro gestionar y automatizar las siguientes tareas:
1. Limpieza, escalado y division de los datos.
2. Entrenar un modelo con Random Forest con búsqueda de hiperparámetros.
3. Contrastar cada vez que se forma un modelo nuevo con el actual de produccion, seleccionando el mejor y dejandolo en produccion.
5. Brindar un API para poder acceder al modelo de predicciones.
6. Presentar documentacion correspondiente para el uso y test de la API.
7. Visualizar resultados y métricas a través de un frontend..

## Tecnologías

- [Airflow](https://airflow.apache.org/): Orquestación de workflows.
- [MinIO](https://min.io/): Almacenamiento de datasets y artefactos (compatible con S3).
- [MLflow](https://mlflow.org/): Tracking de experimentos y gestión de modelos.
- [Docker Compose](https://docs.docker.com/compose/): Contenerización del entorno.
- [FastAPI](https://fastapi.tiangolo.com/): Creación de la API REST.
- [Swagger](https://swagger.io/): Documentacion de la API
- [Streamlit](https://streamlit.io/): Interfaz gráfica de usuario.

## Requisitos

- Docker y Docker Compose instalados.

## Entorno de desarrollo utilizado
- SO: Winfows 11
- Docker faclitado con Docker Desktop

## Forma de uso

### Instalación y setup
1. Clonar el repositorio y levantar los servicios necesarios utilizando Docker Compose:

```bash
git clone JoacoRP/oaa1-20Co2025-ml-models-smth-inc.git
cd oaa1-20Co2025-ml-models-smth-inc
docker compose up --build
```

Se inician los siguientes proocesos servicios y es un proceso que puede tomar unos minutos:

- Airflow (webserver, scheduler)
- MLflow Server: [http://localhost:5000](http://localhost:5000)
- MinIO: [http://localhost:9000](http://localhost:9000) (usuario: `minio`, contraseña: `minio123`)
- API REST con FastAPI: [http://localhost:8000](http://localhost:8000)
- Frontend con Streamlit: [http://localhost:8501](http://localhost:8501)

Para validarlos ingreso uno a uno corroborando que todo se haya levantado correctamente.

### Airflow y DAG de entrenamiento
1. Acceder a la interfaz de Airflow y loguearse con las siguientes credenciales:
- URL: [http://localhost:8080](http://localhost:8080)
- Usuario: `airflow`
- Contraseña: `airflow`

2. Dentro de la interfaz:
- Validar que se reconocen los dos DAGs necesarios
  - `etl_proceso_steam_sales`
  - `retrain_and_promote_sales_model`
- Verificar que el DAG `etl_proceso_steam_sales` esté activo y corrido con resultado `success`.
- Verificar que el DAG `retrain_and_promote_sales_model` esté activo pero sin correr.
- Ejecutar manualmente ese DAG para entrenar el modelo por primera vez y registrarlo en MLflow.

### Frontend
1. Acceder a la plataforma implementada con Streamlit en [http://localhost:8501](http://localhost:8501)
2. Por defecto el home es la pestaña de **Predicciones**
3. Para poder consultar una predicción, hay que seleccionar:
  - Día de la semana
  - Estación del año
  - Es feriado.
4. Por ultimo presionar `Obtener predicción`.
5. Se puede acceder a un **Registro** donde se pueden ver todas las consultas de predicciones realizadas con sus parametros y resultado.

_Nota: En caso de no haber realizado la corrida manual del DAG en Airflow, se generara un mensaje de error en el paso 4._

## Herramientas más detalladas

### Airflow & DAGs disponibles

#### 1. `etl_proceso_ventas`
- Este DAG se ejecuta automáticamente una única vez al iniciar el entorno.
- Realiza el procesamiento de los datos originales (`steam_selling_games.csv`), procesando los datos y diviendo entre `train.csv` y `test.csv` (70/30).
- Los datasets generados en la división se almacenan en MinIO (bucket `data`).

#### 2. `retrain_and_promote_sales_model`
- Reentrena el modelo de predicción de ventas utilizando los datasets obtenidos con el DAG anterior.
- Evalúa si el modelo nuevo supera al de producción en base al RMSE sobre el conjunto de test.
- Si el nuevo modelo es mejor, se lo pasa automáticamente a Production en MLflow Model Registry.

### MLflow
Esta herramienta la usamos para registrar el entrenamiento. Cada corrida registra:
  - Parámetros del modelo seleccionado por GridSearch (n_estimators, max_depth, etc.).
  - Métricas: `cv_mse`, `cv_rmse`, `test_mse`, `test_rmse`, `test_r2`.
  - Modelo entrenado como artefacto.
  - Registro de versiones en el Model Registry bajo el nombre `steam_sales_prediction_model_prod`.

## FastAPI
### Modelos y funcionalidades
- **Prediction**: Consultar un prediccion en tiempo real en base a multiples parametros.
- **Registry**: Consultar las predicciones previamente solicitadas y sus detalles.
- **Healthcheck**: Verifica el estado de la API.

### Documentación interactiva
Esta implementado con Swagger una documentación interactiva que se puede acceder en [http://localhost:8000/docs](http://localhost:8000/docs)

### Uso de health check
Este endpoint se utiliza mas para cuestiones de CI/CD pero ademas se puede acceder para validar que la API este corriendo correctamente [http://localhost:8000/health](http://localhost:8000/health)