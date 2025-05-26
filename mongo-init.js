// Script de inicialización de MongoDB
db = db.getSiblingDB('hoteles_db');

// Crear usuario para la aplicación
db.createUser({
  user: 'app_user',
  pwd: 'app_password',
  roles: [
    {
      role: 'readWrite',
      db: 'hoteles_db'
    }
  ]
});

// Crear índices para optimizar consultas
db.hoteles.createIndex({ "id_hotel": 1 }, { unique: true });
db.hoteles.createIndex({ "ubicacion.coordinates": "2dsphere" });
db.hoteles.createIndex({ "estrellas": 1 });
db.hoteles.createIndex({ "precio": 1 });
db.hoteles.createIndex({ "pais": 1 });

db.habitaciones.createIndex({ "id": 1 }, { unique: true });
db.habitaciones.createIndex({ "id_hotel": 1 });
db.habitaciones.createIndex({ "precio": 1 });
db.habitaciones.createIndex({ "capacidad": 1 });
db.habitaciones.createIndex({ "fechas.inicio": 1, "fechas.fin": 1 });

db.servicios_habitacion.createIndex({ "id": 1 }, { unique: true });
db.servicios_hotel.createIndex({ "id": 1 }, { unique: true });

print('Base de datos inicializada correctamente');
