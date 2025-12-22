#!/usr/bin/env python3
"""
Script para generar datos sintéticos de tráfico urbano
"""
import pandas as pd
import random
from datetime import datetime, timedelta
from pathlib import Path
def generar_datos_sensores_tiempo_real(fecha, num_sensores=50):
    """Genera datos de sensores de tráfico para una fecha específica"""
    # Ubicaciones de sensores
    ubicaciones = [
        "Plaza Mayor - Norte", "Plaza Mayor - Sur", "Gran Vía - Este", "Gran Vía - Oeste",
        "Calle Alcalá - Norte", "Calle Alcalá - Sur", "Paseo de la Castellana - Norte",
        "Paseo de la Castellana - Sur", "Calle Serrano - Este", "Calle Serrano - Oeste",
        "Plaza de España - Norte", "Plaza de España - Sur", "Calle Princesa - Este",
        "Calle Princesa - Oeste", "Plaza de Cibeles - Norte", "Plaza de Cibeles - Sur",
        "Calle Montera - Norte", "Calle Montera - Sur", "Plaza de Callao - Norte",
        "Plaza de Callao - Sur", "Calle Preciados - Este", "Calle Preciados - Oeste",
        "Plaza de Ópera - Norte", "Plaza de Ópera - Sur", "Calle Arenal - Este",
        "Calle Arenal - Oeste", "Plaza de Oriente - Norte", "Plaza de Oriente - Sur",
        "Calle Mayor - Este", "Calle Mayor - Oeste", "Plaza de la Villa - Norte",
        "Plaza de la Villa - Sur", "Calle Segovia - Este", "Calle Segovia - Oeste",
        "Plaza de la Paja - Norte", "Plaza de la Paja - Sur", "Calle Toledo - Este",
        "Calle Toledo - Oeste", "Plaza de Cascorro - Norte", "Plaza de Cascorro - Sur",
        "Calle Embajadores - Este", "Calle Embajadores - Oeste", "Plaza de Lavapiés - Norte",
        "Plaza de Lavapiés - Sur", "Calle Atocha - Este", "Calle Atocha - Oeste",
        "Plaza de Antón Martín - Norte", "Plaza de Antón Martín - Sur", "Calle Huertas - Este",
        "Calle Huertas - Oeste"
    ]
    datos_sensores = []
    for i in range(num_sensores):
        sensor_id = f"S{i + 1:03d}"
        ubicacion = ubicaciones[i] if i < len(ubicaciones) else f"Ubicación {i + 1}"
        # Generar datos cada 15 minutos durante el día
        for hora in range(24):
            for minuto in range(0, 60, 15):
                timestamp = datetime.combine(fecha, datetime.min.time()) + timedelta(hours=hora, minutes=minuto)
                # Velocidad promedio basada en la hora del día
                if 7 <= hora <= 9 or 18 <= hora <= 20:  # Horas pico
                    velocidad_base = random.uniform(15, 25)
                elif 22 <= hora or hora <= 6:  # Noche
                    velocidad_base = random.uniform(35, 50)
                else:  # Día normal
                    velocidad_base = random.uniform(25, 40)
                # Fluctuación aleatoria
                velocidad_promedio = max(5, velocidad_base + random.uniform(-10, 10))
                # Ocupación basada en la velocidad (inversamente proporcional)
                ocupacion_porcentaje = max(10, min(95, 100 - (velocidad_promedio * 2)))
                # Vehículos por hora estimados
                vehiculos_por_hora = int(velocidad_promedio * 15 + random.uniform(-50, 50))
                vehiculos_por_hora = max(0, vehiculos_por_hora)
                datos_sensores.append({
                    'sensor_id': sensor_id,
                    'ubicacion': ubicacion,
                    'timestamp': timestamp,
                    'velocidad_promedio': round(velocidad_promedio, 2),
                    'ocupacion_porcentaje': round(ocupacion_porcentaje, 2),
                    'vehiculos_por_hora': vehiculos_por_hora
                })
    return pd.DataFrame(datos_sensores)
def generar_datos_semaforos_tiempo_real(fecha, num_semaforos=50):
    """Genera datos de semáforos para una fecha específica"""
    ubicaciones = [
        "Plaza Mayor - Norte", "Plaza Mayor - Sur", "Gran Vía - Este", "Gran Vía - Oeste",
        "Calle Alcalá - Norte", "Calle Alcalá - Sur", "Paseo de la Castellana - Norte",
        "Paseo de la Castellana - Sur", "Calle Serrano - Este", "Calle Serrano - Oeste",
        "Plaza de España - Norte", "Plaza de España - Sur", "Calle Princesa - Este",
        "Calle Princesa - Oeste", "Plaza de Cibeles - Norte", "Plaza de Cibeles - Sur",
        "Calle Montera - Norte", "Calle Montera - Sur", "Plaza de Callao - Norte",
        "Plaza de Callao - Sur", "Calle Preciados - Este", "Calle Preciados - Oeste",
        "Plaza de Ópera - Norte", "Plaza de Ópera - Sur", "Calle Arenal - Este",
        "Calle Arenal - Oeste", "Plaza de Oriente - Norte", "Plaza de Oriente - Sur",
        "Calle Mayor - Este", "Calle Mayor - Oeste", "Plaza de la Villa - Norte",
        "Plaza de la Villa - Sur", "Calle Segovia - Este", "Calle Segovia - Oeste",
        "Plaza de la Paja - Norte", "Plaza de la Paja - Sur", "Calle Toledo - Este",
        "Calle Toledo - Oeste", "Plaza de Cascorro - Norte", "Plaza de Cascorro - Sur",
        "Calle Embajadores - Este", "Calle Embajadores - Oeste", "Plaza de Lavapiés - Norte",
        "Plaza de Lavapiés - Sur", "Calle Atocha - Este", "Calle Atocha - Oeste",
        "Plaza de Antón Martín - Norte", "Plaza de Antón Martín - Sur", "Calle Huertas - Este",
        "Calle Huertas - Oeste"
    ]
    datos_semaforos = []
    for i in range(num_semaforos):
        semaforo_id = f"SEM{i + 1:03d}"
        ubicacion = ubicaciones[i] if i < len(ubicaciones) else f"Ubicación {i + 1}"
        # Generar datos cada 5 minutos durante el día
        for hora in range(24):
            for minuto in range(0, 60, 5):
                timestamp = datetime.combine(fecha, datetime.min.time()) + timedelta(hours=hora, minutes=minuto)
                # Estado del semáforo (Verde, Amarillo, Rojo)
                estados = ['Verde', 'Amarillo', 'Rojo']
                estado_actual = random.choice(estados)
                # Tiempo de espera basado en el estado
                if estado_actual == 'Verde':
                    tiempo_espera = 0
                elif estado_actual == 'Amarillo':
                    tiempo_espera = random.uniform(1, 3)
                else:  # Rojo
                    tiempo_espera = random.uniform(10, 60)
                # Intensidad del tráfico
                if 7 <= hora <= 9 or 18 <= hora <= 20:  # Horas pico
                    intensidad_trafico = random.uniform(0.7, 1.0)
                elif 22 <= hora or hora <= 6:  # Noche
                    intensidad_trafico = random.uniform(0.1, 0.3)
                else:  # Día normal
                    intensidad_trafico = random.uniform(0.4, 0.8)
                datos_semaforos.append({
                    'semaforo_id': semaforo_id,
                    'ubicacion': ubicacion,
                    'timestamp': timestamp,
                    'estado_actual': estado_actual,
                    'tiempo_espera': round(tiempo_espera, 2),
                    'intensidad_trafico': round(intensidad_trafico, 2)
                })
    return pd.DataFrame(datos_semaforos)
def generar_datos_incidentes_tiempo_real(fecha, num_incidentes=20):
    """Genera datos de incidentes de tráfico para una fecha específica"""
    tipos_incidente = ['Accidente', 'Atasco', 'Avería', 'Obras', 'Manifestación']
    severidades = ['Baja', 'Media', 'Alta']
    datos_incidentes = []
    for i in range(num_incidentes):
        # Generar incidente en hora aleatoria del día
        hora_incidente = random.randint(0, 23)
        minuto_incidente = random.randint(0, 59)
        timestamp = datetime.combine(fecha, datetime.min.time()) + timedelta(hours=hora_incidente, minutes=minuto_incidente)
        tipo_incidente = random.choice(tipos_incidente)
        severidad = random.choice(severidades)
        # Ubicación aleatoria
        ubicaciones = [
            "Plaza Mayor", "Gran Vía", "Calle Alcalá", "Paseo de la Castellana",
            "Calle Serrano", "Plaza de España", "Calle Princesa", "Plaza de Cibeles",
            "Calle Montera", "Plaza de Callao", "Calle Preciados", "Plaza de Ópera",
            "Calle Arenal", "Plaza de Oriente", "Calle Mayor", "Plaza de la Villa",
            "Calle Segovia", "Plaza de la Paja", "Calle Toledo", "Plaza de Cascorro",
            "Calle Embajadores", "Plaza de Lavapiés", "Calle Atocha", "Plaza de Antón Martín",
            "Calle Huertas"
        ]
        ubicacion = random.choice(ubicaciones)
        # Tiempo de resolución basado en severidad
        if severidad == 'Baja':
            tiempo_resolucion = random.randint(15, 60)
        elif severidad == 'Media':
            tiempo_resolucion = random.randint(60, 180)
        else:  # Alta
            tiempo_resolucion = random.randint(180, 480)
        # Si es muy tarde en la noche, puede no tener tiempo de resolución
        if hora_incidente >= 22:
            tiempo_resolucion_str = None
        else:
            tiempo_resolucion_str = timestamp + timedelta(minutes=tiempo_resolucion)
        vehiculos_afectados = random.randint(1, 10)
        # Descripciones basadas en el tipo de incidente
        descripciones = {
            'Accidente': ['Colisión lateral entre vehículos', 'Accidente con heridos leves', 'Golpe en retroceso'],
            'Atasco': ['Congestión por obras en la calzada', 'Congestión por semáforo averiado', 'Congestión por cierre de carril'],
            'Avería': ['Vehículo averiado en la calzada', 'Motor averiado', 'Neumático reventado'],
            'Obras': ['Obras en la calzada', 'Cierre temporal por obras', 'Obras menores'],
            'Manifestación': ['Manifestación en la zona', 'Corte de tráfico por manifestación', 'Protesta ciudadana']
        }
        descripcion = random.choice(descripciones[tipo_incidente])
        datos_incidentes.append({
            'incidente_id': f"INC{i + 1:03d}",
            'ubicacion': ubicacion,
            'timestamp': timestamp,
            'tipo_incidente': tipo_incidente,
            'severidad': severidad,
            'descripcion': descripcion,
            'vehiculos_afectados': vehiculos_afectados,
            'tiempo_resolucion': tiempo_resolucion_str
        })
    return pd.DataFrame(datos_incidentes)
def generar_datos_vehiculos_tiempo_real(fecha, num_vehiculos=100):
    """Genera datos de vehículos detectados para una fecha específica"""
    tipos_vehiculo = ['Coche', 'Motocicleta', 'Autobús', 'Camión', 'Furgoneta']
    colores = ['Blanco', 'Negro', 'Gris', 'Azul', 'Rojo', 'Verde', 'Amarillo']
    datos_vehiculos = []
    for i in range(num_vehiculos):
        # Generar detección en hora aleatoria del día
        hora_deteccion = random.randint(0, 23)
        minuto_deteccion = random.randint(0, 59)
        timestamp = datetime.combine(fecha, datetime.min.time()) + timedelta(hours=hora_deteccion, minutes=minuto_deteccion)
        tipo_vehiculo = random.choice(tipos_vehiculo)
        color = random.choice(colores)
        # Ubicación aleatoria
        ubicaciones = [
            "Plaza Mayor", "Gran Vía", "Calle Alcalá", "Paseo de la Castellana",
            "Calle Serrano", "Plaza de España", "Calle Princesa", "Plaza de Cibeles",
            "Calle Montera", "Plaza de Callao", "Calle Preciados", "Plaza de Ópera",
            "Calle Arenal", "Plaza de Oriente", "Calle Mayor", "Plaza de la Villa",
            "Calle Segovia", "Plaza de la Paja", "Calle Toledo", "Plaza de Cascorro",
            "Calle Embajadores", "Plaza de Lavapiés", "Calle Atocha", "Plaza de Antón Martín",
            "Calle Huertas"
        ]
        ubicacion = random.choice(ubicaciones)
        # Velocidad basada en el tipo de vehículo y hora
        if tipo_vehiculo in ['Autobús', 'Camión']:
            velocidad_base = random.uniform(20, 40)
        elif tipo_vehiculo == 'Motocicleta':
            velocidad_base = random.uniform(30, 60)
        else:  # Coche, Furgoneta
            velocidad_base = random.uniform(25, 50)
        # Ajustar velocidad según la hora
        if 7 <= hora_deteccion <= 9 or 18 <= hora_deteccion <= 20:  # Horas pico
            velocidad_base *= 0.6
        elif 22 <= hora_deteccion or hora_deteccion <= 6:  # Noche
            velocidad_base *= 1.2
        velocidad = max(5, min(80, velocidad_base + random.uniform(-10, 10)))
        datos_vehiculos.append({
            'vehiculo_id': f"VEH{i + 1:03d}",
            'tipo_vehiculo': tipo_vehiculo,
            'color': color,
            'ubicacion': ubicacion,
            'timestamp': timestamp,
            'velocidad': round(velocidad, 2)
        })
    return pd.DataFrame(datos_vehiculos)
def generar_datos_camaras_tiempo_real(fecha, num_camaras=20):
    """Genera datos de cámaras de seguridad para una fecha específica"""
    datos_camaras = []
    for i in range(num_camaras):
        datos_camaras.append({
            'camara_id': f"CAM{i + 1:03d}",
            'ubicacion': f"Ubicación {i + 1}",
            'estado': 'Operativa',
            'timestamp': datetime.combine(fecha, datetime.min.time())
        })
    return pd.DataFrame(datos_camaras)
def main():
    """Función principal para generar todos los datos"""
    print("🚗 Generando datos sintéticos de tráfico urbano...")
    # Fecha base (hoy)
    fecha_base = datetime.now().date()
    
    # Directorio de salida compatible con Airflow (Bronze Bucket)
    output_dir = Path("buckets/bronze-bucket/raw_data")
    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"📂 Directorio de salida: {output_dir}")

    # Generamos datos solo para hoy para la prueba inmediata
    fecha = fecha_base
    print(f"📅 Generando datos para {fecha}...")
    
    # Generar datos de sensores
    sensores_df = generar_datos_sensores_tiempo_real(fecha)
    sensores_df.to_csv(output_dir / 'sensores_trafico.csv', index=False)
    print(f"  ✅ Sensores: {len(sensores_df)} registros")
    
    # Generar datos de semáforos
    semaforos_df = generar_datos_semaforos_tiempo_real(fecha)
    semaforos_df.to_csv(output_dir / 'semaforos.csv', index=False)
    print(f"  ✅ Semáforos: {len(semaforos_df)} registros")
    
    # Generar datos de incidentes
    incidentes_df = generar_datos_incidentes_tiempo_real(fecha)
    incidentes_df.to_csv(output_dir / 'incidentes_trafico.csv', index=False)
    print(f"  ✅ Incidentes: {len(incidentes_df)} registros")
    
    # Generar datos de vehículos
    vehiculos_df = generar_datos_vehiculos_tiempo_real(fecha)
    vehiculos_df.to_csv(output_dir / 'vehiculos.csv', index=False)
    print(f"  ✅ Vehículos: {len(vehiculos_df)} registros")

    # Generar datos de cámaras (Nuevo)
    camaras_df = generar_datos_camaras_tiempo_real(fecha)
    camaras_df.to_csv(output_dir / 'camaras_seguridad.csv', index=False)
    print(f"  ✅ Cámaras: {len(camaras_df)} registros")

    print("🎉 ¡Datos generados exitosamente!")
if __name__ == "__main__":
    main()
