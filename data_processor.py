import pandas as pd
import numpy as np
import pymongo
from pymongo import MongoClient
import json
import re
from datetime import datetime
import logging
from tqdm import tqdm
import os
from os import path
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Configurar logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class HotelesDataProcessor:
    def __init__(self, datos_folder, mongodb_url="mongodb://admin:password123@localhost:27017/hoteles_db?authSource=admin"):
        """Inicializar el procesador de datos"""
        self.mongodb_url = mongodb_url
        self.client = None
        self.db = None
        self.servicios_habitacion = {}
        self.servicios_hotel = {}
        self.datos_folder = datos_folder
        
    def conectar_mongodb(self):
        """Conectar a MongoDB"""
        try:
            self.client = MongoClient(self.mongodb_url)
            self.db = self.client['hoteles_db']
            # Verificar conexión
            self.client.admin.command('ping')
            logger.info("Conexión exitosa a MongoDB")
            return True
        except Exception as e:
            logger.error(f"Error conectando a MongoDB: {e}")
            return False
    
    def limpiar_texto(self, texto):
        """Limpiar texto eliminando caracteres especiales"""
        if pd.isna(texto) or texto is None:
            return None
        texto = str(texto)
        # Eliminar los espacios en blanco al inicio y al final
        return texto.strip()
    
    def parsear_facilities(self, facilities_str):
        """Convertir string de facilities a lista de enteros"""
        if pd.isna(facilities_str) or facilities_str == '[]':
            return []
        try:
            # Remover corchetes y dividir por comas
            facilities_str = str(facilities_str).strip('[]')
            if not facilities_str:
                return []
            return [int(x.strip()) for x in facilities_str.split(',') if x.strip().isdigit()]
        except:
            return []
    
    def cargar_servicios(self):
        """Cargar catálogos de servicios"""
        logger.info("Cargando catálogos de servicios...")
        
        # Servicios de habitación
        try:
            df_serv_hab = pd.read_csv(path.join(self.datos_folder, 'servicios_habitacion.csv'))
            for _, row in df_serv_hab.iterrows():
                self.servicios_habitacion[row['id']] = self.limpiar_texto(row['name'])
            logger.info(f"Cargados {len(self.servicios_habitacion)} servicios de habitación")
        except Exception as e:
            logger.error(f"Error cargando servicios de habitación: {e}")
        
        # Servicios de hotel
        try:
            df_serv_hotel = pd.read_csv(path.join(self.datos_folder, 'servicios_hotel.csv'))
            for _, row in df_serv_hotel.iterrows():
                self.servicios_hotel[row['id']] = self.limpiar_texto(row['name'])
            logger.info(f"Cargados {len(self.servicios_hotel)} servicios de hotel")
        except Exception as e:
            logger.error(f"Error cargando servicios de hotel: {e}")
    
    def procesar_hoteles(self):
        """Procesar y limpiar datos de hoteles"""
        logger.info("Procesando datos de hoteles...")
        
        try:
            df = pd.read_csv(path.join(self.datos_folder, 'hoteles.csv'))
            logger.info(f"Datos originales: {len(df)} hoteles")
            
            hoteles_procesados = []
            
            for _, row in tqdm(df.iterrows(), total=len(df), desc="Procesando hoteles"):
                # Saltar hoteles sin información básica
                if pd.isna(row['hotel_name']) or pd.isna(row['lat']) or pd.isna(row['lon']):
                    continue
                
                # Parsear facilities
                facilities_ids = self.parsear_facilities(row['facilities'])
                facilities_nombres = [self.servicios_hotel.get(fid, f"Servicio {fid}") 
                                    for fid in facilities_ids if fid in self.servicios_hotel]
                
                hotel = {
                    'id_hotel': int(row['id_hotel']),
                    'nombre': self.limpiar_texto(row['hotel_name']),
                    'estrellas': int(row['stars']) if not pd.isna(row['stars']) else 0,
                    'precio_base': float(row['price']) if not pd.isna(row['price']) else None,
                    'direccion': self.limpiar_texto(row['address']),
                    'ubicacion': {
                        'tipo': 'Point',
                        'coordinates': [float(row['lon']), float(row['lat'])]
                    },
                    'puntuacion_booking': float(row['vote_booking']) if not pd.isna(row['vote_booking']) else None,
                    'tipo_hotel': int(row['type']) if not pd.isna(row['type']) else 0,
                    'descripcion': self.limpiar_texto(row['description']),
                    'pais': int(row['id_country']),
                    'horarios': {
                        'checkin': {
                            'min': self.limpiar_texto(row['checkin_min']),
                            'max': self.limpiar_texto(row['checkin_max'])
                        },
                        'checkout': {
                            'min': self.limpiar_texto(row['checkout_min']),
                            'max': self.limpiar_texto(row['checkout_max'])
                        }
                    },
                    'servicios': {
                        'ids': facilities_ids,
                        'nombres': facilities_nombres
                    },
                    'fecha_procesamiento': datetime.now()
                }
                
                hoteles_procesados.append(hotel)
            
            logger.info(f"Procesados {len(hoteles_procesados)} hoteles válidos")
            return hoteles_procesados
            
        except Exception as e:
            logger.error(f"Error procesando hoteles: {e}")
            return []
    
    def procesar_habitaciones(self):
        """Procesar y limpiar datos de habitaciones"""
        logger.info("Procesando datos de habitaciones...")
        
        try:
            df = pd.read_csv(path.join(self.datos_folder, 'precios_habitaciones.csv'))
            logger.info(f"Datos originales: {len(df)} habitaciones")
            
            habitaciones_procesadas = []
            
            for _, row in tqdm(df.iterrows(), total=len(df), desc="Procesando habitaciones"):
                # Parsear facilities
                facilities_ids = self.parsear_facilities(row['facilities'])
                facilities_nombres = [self.servicios_habitacion.get(fid, f"Servicio {fid}") 
                                    for fid in facilities_ids if fid in self.servicios_habitacion]
                
                # Convertir fechas
                try:
                    fecha_inicio = datetime.strptime(row['start_date'], '%Y-%m-%d')
                    fecha_fin = datetime.strptime(row['end_date'], '%Y-%m-%d')
                except:
                    fecha_inicio = None
                    fecha_fin = None
                
                habitacion = {
                    'id': int(row['id']),
                    'id_hotel': int(row['id_hotel']),
                    'titulo': self.limpiar_texto(row['title']),
                    'fechas': {
                        'inicio': fecha_inicio,
                        'fin': fecha_fin,
                        'inicio_str': row['start_date'],
                        'fin_str': row['end_date']
                    },
                    'capacidad': int(row['capacity']),
                    'tamaño_habitacion': int(row['room_size']) if row['room_size'] > 0 else None,
                    'precio': int(row['price']),
                    'servicios': {
                        'ids': facilities_ids,
                        'nombres': facilities_nombres
                    },
                    'fecha_procesamiento': datetime.now()
                }
                
                habitaciones_procesadas.append(habitacion)
            
            logger.info(f"Procesadas {len(habitaciones_procesadas)} habitaciones")
            return habitaciones_procesadas
            
        except Exception as e:
            logger.error(f"Error procesando habitaciones: {e}")
            return []
    
    def insertar_datos(self, coleccion, datos, batch_size=1000):
        """Insertar datos en MongoDB por lotes"""
        if not datos:
            logger.warning(f"No hay datos para insertar en {coleccion}")
            return
        
        try:
            # Limpiar colección existente
            self.db[coleccion].drop()
            logger.info(f"Colección {coleccion} limpia")
            
            # Insertar por lotes
            total_batches = (len(datos) + batch_size - 1) // batch_size
            insertados = 0
            
            for i in tqdm(range(0, len(datos), batch_size), 
                         total=total_batches, 
                         desc=f"Insertando en {coleccion}"):
                
                batch = datos[i:i + batch_size]
                try:
                    result = self.db[coleccion].insert_many(batch, ordered=False)
                    insertados += len(result.inserted_ids)
                except Exception as e:
                    logger.error(f"Error insertando batch: {e}")
            
            logger.info(f"Insertados {insertados} documentos en {coleccion}")
            
        except Exception as e:
            logger.error(f"Error insertando datos en {coleccion}: {e}")
    
    def insertar_servicios(self):
        """Insertar catálogos de servicios"""
        logger.info("Insertando catálogos de servicios...")
        
        # Servicios de habitación
        servicios_hab = [
            {'id': id_serv, 'nombre': nombre, 'tipo': 'habitacion'}
            for id_serv, nombre in self.servicios_habitacion.items()
        ]
        self.insertar_datos('servicios_habitacion', servicios_hab)
        
        # Servicios de hotel
        servicios_hot = [
            {'id': id_serv, 'nombre': nombre, 'tipo': 'hotel'}
            for id_serv, nombre in self.servicios_hotel.items()
        ]
        self.insertar_datos('servicios_hotel', servicios_hot)
    
    def crear_indices(self):
        """Crear índices para optimizar consultas"""
        logger.info("Creando índices...")
        
        try:
            # Índices para hoteles
            self.db.hoteles.create_index([("id_hotel", 1)], unique=True)
            self.db.hoteles.create_index([("ubicacion", "2dsphere")])
            self.db.hoteles.create_index([("estrellas", 1)])
            self.db.hoteles.create_index([("precio_base", 1)])
            self.db.hoteles.create_index([("pais", 1)])
            
            # Índices para habitaciones
            self.db.habitaciones.create_index([("id", 1)], unique=True)
            self.db.habitaciones.create_index([("id_hotel", 1)])
            self.db.habitaciones.create_index([("precio", 1)])
            self.db.habitaciones.create_index([("capacidad", 1)])
            self.db.habitaciones.create_index([("fechas.inicio", 1), ("fechas.fin", 1)])
            
            logger.info("Índices creados correctamente")
            
        except Exception as e:
            logger.error(f"Error creando índices: {e}")
  
    def procesar_todo(self):
        """Ejecutar todo el proceso de limpieza e inserción"""
        logger.info("Iniciando procesamiento completo de datos...")
        
        # Conectar a MongoDB
        if not self.conectar_mongodb():
            return False
        
        # Cargar servicios
        self.cargar_servicios()
        
        # Insertar servicios
        self.insertar_servicios()
        
        # Procesar e insertar hoteles
        hoteles = self.procesar_hoteles()
        self.insertar_datos('hoteles', hoteles)
        
        # Procesar e insertar habitaciones
        habitaciones = self.procesar_habitaciones()
        self.insertar_datos('habitaciones', habitaciones)
        
        # Crear índices
        self.crear_indices()
        
        
        logger.info("Procesamiento completado exitosamente!")
        return True

def main():
    """Función principal"""
    # Obtener URL de MongoDB desde variable de entorno
    mongodb_url = os.getenv('MONGODB_URL', 'mongodb://admin:password123@localhost:27017/hoteles_db?authSource=admin')
    datos_folder = './datos'
    # Crear y ejecutar procesador
    processor = HotelesDataProcessor(datos_folder, mongodb_url)
    processor.procesar_todo()

if __name__ == "__main__":
    main()
