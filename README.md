# Análisis de Machine Learning para Plataforma de Alojamiento Vacacional

## Descripción del Proyecto

Este proyecto forma parte de la asignatura de Ingeniería de Datos y se centra en el análisis de datos para una plataforma de alojamiento vacacional en España.

## Contexto de la Práctica

La plataforma de alojamiento vacacional actualiza los datos de los hoteles a través de 4 ficheros CSV que contienen:

1. **Información de los alojamientos**: Datos básicos de los hoteles incluyendo ubicación, estrellas, precios y puntuaciones
2. **Precios de habitaciones**: Información detallada sobre los diferentes tipos de habitación y sus precios
3. **Servicios de hoteles**: Catálogo de servicios y facilities disponibles a nivel de hotel
4. **Servicios de habitaciones**: Catálogo de servicios y facilities específicos de cada tipo de habitación

## Objetivos del Análisis

El proyecto implementa tres tipos principales de modelos de Machine Learning:

### 1. Modelos de Regresión
- **Objetivo**: Predecir el precio de las habitaciones
- **Algoritmos implementados**:
  - Regresión Lineal
  - Random Forest Regressor
  - Red Neuronal (MLP Regressor)
- **Características utilizadas**: Capacidad, tamaño de habitación, estrellas del hotel, puntuación y facilities de habitación

### 2. Modelo de Clustering
- **Objetivo**: Agrupar hoteles por características similares
- **Algoritmo**: K-Means
- **Características utilizadas**: Estrellas, precio y puntuación

### 3. Modelos de Clasificación
- **Objetivo**: Predecir la categoría de estrellas de los hoteles
- **Algoritmos implementados**:
  - Random Forest Classifier
  - Regresión Logística Multinomial
- **Características utilizadas**: Precio, puntuación, tipo de hotel y facilities del hotel

## Estructura de Archivos

```
proyecto/
├── datos/
│   ├── hoteles.csv                 # Información principal de hoteles
│   ├── precios_habitaciones.csv    # Precios y características de habitaciones
│   ├── servicios_hotel.csv         # Catálogo de servicios de hotel
│   └── servicios_habitacion.csv    # Catálogo de servicios de habitación
├── ml_analysis_hoteles.ipynb       # Notebook principal con el análisis
├── requirements.txt                # Dependencias del proyecto
├── data_processor.py              # Procesador de datos
├── docker-compose.yml             # Configuración Docker
├── mongo-init.js                  # Inicialización MongoDB
└── README.md                      # Este archivo
```

## Requisitos del Sistema

### Software necesario:
- Visual Studio Code
- Python
- Jupyter Notebook
- Git (opcional, para clonar el repositorio)
- Docker

### Dependencias de Python:
- En el requirements.txt

## Configuración del Entorno con Docker

El proyecto incluye una configuración de MongoDB usando Docker para almacenar y gestionar los datos.

### Requisitos para Docker:
- Docker

### Configuración de la Base de Datos:

1. **Iniciar MongoDB con Docker**:
```bash
docker-compose up -d
```

2. **Verificar que MongoDB esté funcionando**:
```bash
docker ps
```
Deberías ver un contenedor llamado `mongodb_hoteles` ejecutándose.

3. **Acceso a MongoDB (datos de ejemplo)**:
   - **URL de conexión**: `mongodb://admin:password123@localhost:27017/hoteles_db?authSource=admin`
   - **Usuario administrador**: `admin`
   - **Contraseña**: `password123`
   - **Base de datos**: `hoteles_db`

### Procesamiento y Carga de Datos:

El archivo `data_processor.py` se encarga de:
- Limpiar y estructurar los datos CSV
- Parsear las facilities de hoteles y habitaciones
- Cargar los datos en MongoDB con la estructura óptima
- Crear índices para consultas eficientes

**Ejecutar el procesador de datos**:
```bash
python data_processor.py
```

Este proceso:
1. Conecta a MongoDB
2. Carga los catálogos de servicios
3. Procesa y limpia los datos de hoteles
4. Procesa y limpia los datos de habitaciones
5. Inserta todo en la base de datos
6. Crea índices para optimizar consultas

### Detener el entorno Docker:
```bash
docker-compose down -v
```

## Instalación y Configuración

### 1. Clonar o descargar el proyecto
```bash
# Si usas Git
git clone https://github.com/didinaeg/trabajo-hoteles
cd trabajofinal

# O descargar y extraer el archivo ZIP
```

### 2. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Verificar estructura de datos
Asegúrate de que la carpeta `datos/` contenga los siguientes archivos CSV:
- `hoteles.csv`
- `precios_habitaciones.csv`
- `servicios_hotel.csv`
- `servicios_habitacion.csv`

## Ejecución del Proyecto

### Proceso de la Base de Datos

1. **Copiar el archivo `.env.example` a `.env`**:

2. **Iniciar el entorno Docker**:
```bash
docker-compose up -d
```

3. **Procesar y cargar datos en MongoDB**:
```bash
python data_processor.py
```

### Análisis de datos
1. Abrir Visual Studio Code
2. Instalar las extensiones de Python y Jupyter
3. Abrir el archivo `ml_analysis_hoteles.ipynb`
4. Seleccionar el intérprete de Python
5. Ejecutar las celdas (el notebook carga directamente desde los CSV)

## Estructura del Análisis

### Datos:
- **Archivos CSV**: Datos originales en formato crudo
- **MongoDB**: Base de datos NoSQL para almacenamiento estructurado
- **data_processor.py**: Transforma CSV a MongoDB

### Análisis:
El notebook está organizado en las siguientes secciones:

1. **Importación de librerías**: Carga de todas las dependencias necesarias
2. **Carga y exploración de datos**: Lectura de archivos CSV y análisis exploratorio
3. **Limpieza y preprocesamiento**: 
   - Tratamiento de valores nulos
   - Procesamiento de facilities de habitaciones y hoteles
   - Creación de variables binarias (one-hot encoding)
4. **Preparación de datos**: División en conjuntos de entrenamiento y prueba y preparacion de los datos para cada tipo de modelo
5. **Modelos de regresión**: Implementación y evaluación de modelos predictivos de precio
6. **Modelo de clustering**: Agrupación de hoteles por características
7. **Modelos de clasificación**: Predicción de categorías de estrellas

## Métricas de Evaluación

### Modelos de Regresión:
- **R² Score**: Coeficiente de determinación (0 = malo, 1 = perfecto)
- **MSE**: Error cuadrático medio
- **MAE**: Error absoluto medio

### Modelo de Clustering:
- **Silhouette Score**: Calidad de los clusters (-1 = malo, 1 = perfecto)
- **Método Elbow**: Para determinar número óptimo de clusters

### Modelos de Clasificación:
- **Accuracy**: Precisión general del modelo
- **Classification Report**: Precisión, recall y F1-score por clase
- **Confusion Matrix**: Matriz de confusión

## Créditos

**Autores**:
- Diana Murieva
- Irene Gómez Figueroa
- Juan José Velasquez Garces
- Lidia Lorenzo Alcedo
- Rodrigo Rafael Hernandez Ayala

**Profesor**:
- Hugo Fernandez Visiera

Proyecto desarrollado para la asignatura de Ingeniería de Datos.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.