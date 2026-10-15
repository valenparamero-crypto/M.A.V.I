from smbus2 import SMBus
import time
from enum import Enum

# --- 1. CONFIGURACIÓN I2C ---
DIRECCION_ESP32 = 0x08
NUMERO_BUS = 1

# Diccionario de direcciones (Para que sea fácil de leer)
DIR_QUIETO = 0
DIR_ADELANTE = 1
DIR_ATRAS = 2
DIR_IZQUIERDA = 3
DIR_DERECHA = 4

# --- 2. FUNCIONES I2C (Las que ya probamos y funcionan) ---
def enviar_orden_segura(registro, valor, max_reintentos=3):
    trama = [registro, valor, registro + valor]
    for intento in range(max_reintentos):
        try:
            with SMBus(NUMERO_BUS) as bus:
                bus.write_i2c_block_data(DIRECCION_ESP32, trama[0], trama[1:])
                return True
        except OSError as e:
            if e.errno == 11:
                time.sleep(0.05)
            else:
                break
    return False

# --- 3. DEFINICIÓN DE LA MÁQUINA DE ESTADOS ---
class EstadoMavi(Enum):
    REPOSO = 1
    AVANZANDO = 2
    OBSTACULO = 3
    ESQUIVANDO = 4

# Variables globales del robot
estado_actual = EstadoMavi.REPOSO
tiempo_estado = time.time()  # Para medir cuánto tiempo llevamos en un estado

# --- 4. FUNCIÓN SIMULADORA DE SENSORES (Futura Visión Artificial) ---
def simular_vision_artificial(estado):
    """
    Esta función simula lo que haría tu cámara con OpenCV.
    Por ahora, usamos el tiempo para forzar cambios de estado y probar la lógica.
    """
    tiempo_transcurrido = time.time() - tiempo_estado
    
    if estado == EstadoMavi.REPOSO and tiempo_transcurrido > 3:
        return "VIA_LIBRE" # Después de 3 seg de reposo, simulamos que puede arrancar
        
    elif estado == EstadoMavi.AVANZANDO and tiempo_transcurrido > 5:
        return "PELIGRO_FRENTE" # A los 5 seg de avanzar, "aparece" un obstáculo
        
    elif estado == EstadoMavi.ESQUIVANDO and tiempo_transcurrido > 2:
        return "VIA_LIBRE" # Después de girar 2 seg, ya no hay obstáculo
        
    return "NADA_NUEVO"

# --- 5. BUCLE PRINCIPAL (EL CEREBRO) ---
if __name__ == "__main__":
    print("🤖 Iniciando Cerebro M.A.V.I. - Máquina de Estados")
    
    # Encendemos el sistema de movimiento (Registro 1, Valor 1)
    enviar_orden_segura(1, 1) 
    print("=> Sistema de motores ENCENDIDO")

    try:
        while True:
            # 1. Leer "sensores" (En el futuro, aquí llamas a tu cámara)
            evento = simular_vision_artificial(estado_actual)

            # 2. LÓGICA DE TRANSICIÓN DE ESTADOS
            if estado_actual == EstadoMavi.REPOSO:
                if evento == "VIA_LIBRE":
                    print("\n[DECISIÓN] Vía libre detectada. Iniciando marcha.")
                    estado_actual = EstadoMavi.AVANZANDO
                    tiempo_estado = time.time()
                    enviar_orden_segura(2, DIR_ADELANTE) # Orden I2C

            elif estado_actual == EstadoMavi.AVANZANDO:
                if evento == "PELIGRO_FRENTE":
                    print("\n[DECISIÓN] ¡OBSTÁCULO! FRENANDO.")
                    estado_actual = EstadoMavi.OBSTACULO
                    tiempo_estado = time.time()
                    enviar_orden_segura(2, DIR_QUIETO) # Orden I2C para frenar

            elif estado_actual == EstadoMavi.OBSTACULO:
                # El robot está detenido, decide girar
                print("\n[DECISIÓN] Calculando ruta... Girando a la izquierda.")
                estado_actual = EstadoMavi.ESQUIVANDO
                tiempo_estado = time.time()
                enviar_orden_segura(2, DIR_IZQUIERDA) # Orden I2C

            elif estado_actual == EstadoMavi.ESQUIVANDO:
                if evento == "VIA_LIBRE":
                    print("\n[DECISIÓN] Obstáculo superado. Retomando ruta.")
                    estado_actual = EstadoMavi.AVANZANDO
                    tiempo_estado = time.time()
                    enviar_orden_segura(2, DIR_ADELANTE) # Orden I2C

            # Pequeña pausa para no saturar el procesador de la Raspberry
            time.sleep(0.1)

    except KeyboardInterrupt:
        # Si presionas Ctrl+C en la terminal, apagamos el robot de forma segura
        print("\n🛑 Apagando M.A.V.I...")
        enviar_orden_segura(2, DIR_QUIETO) # Frenar
        enviar_orden_segura(1, 0)          # Apagar sistema
        print("Robot detenido de forma segura.")