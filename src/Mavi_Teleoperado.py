import cv2
import numpy as np
import time
from smbus2 import SMBus
from picamera2 import Picamera2

# =====================================================================
# CONFIGURACIÓN I2C Y DIRECCIONES
# =====================================================================
DIRECCION_ESP32 = 0x08
NUMERO_BUS = 1

DIR_QUIETO = 0
DIR_ADELANTE = 1
DIR_ATRAS = 2
DIR_IZQUIERDA = 3
DIR_DERECHA = 4

direccion_actual_robot = -1 
telemetria_actual = {"estado": 1, "rpm_izq": 0, "rpm_der": 0}
tiempo_ultima_telemetria = 0

def enviar_orden_segura(registro, valor, max_reintentos=2):
    trama = [registro, valor, (registro + valor) & 0xFF]
    for intento in range(max_reintentos):
        try:
            with SMBus(NUMERO_BUS) as bus:
                bus.write_i2c_block_data(DIRECCION_ESP32, trama[0], trama[1:])
                return True
        except OSError:
            time.sleep(0.02)
    return False

def leer_telemetria_segura():
    try:
        with SMBus(NUMERO_BUS) as bus:
            data = bus.read_i2c_block_data(DIRECCION_ESP32, 0, 4)
            if data[3] == ((data[0] + data[1] + data[2]) & 0xFF):
                return {"rpm_izq": data[1], "rpm_der": data[2]}
    except:
        pass
    return None

def cambiar_direccion(nueva_direccion):
    global direccion_actual_robot
    if direccion_actual_robot != nueva_direccion:
        enviar_orden_segura(2, nueva_direccion)
        direccion_actual_robot = nueva_direccion

# =====================================================================
# MAIN (TELEOPERACIÓN + CÁMARA)
# =====================================================================
def main():
    global telemetria_actual, tiempo_ultima_telemetria
    
    print("🎮 Iniciando Modo Teleoperado con Cámara...")
    enviar_orden_segura(1, 1) # Encender ESP32
    cambiar_direccion(DIR_QUIETO)
    
    picam2 = Picamera2()
    config = picam2.create_video_configuration(main={"size": (640, 480), "format": "BGR888"})
    picam2.configure(config)
    picam2.start()

    print("✅ Todo listo. Haz clic en la ventana de video para controlarlo.")
    print("Controles: W (Adelante), S (Atras), A (Izq), D (Der), ESPACIO (Frenar), Q (Salir)")

    estado_texto = "QUIETO (Presiona W/A/S/D)"
    prev_time = time.time()

    try:
        while True:
            # 1. Capturar Video y FPS
            frame = picam2.capture_array()
            alto, ancho = frame.shape[:2]
            
            curr_time = time.time()
            fps = 1 / (curr_time - prev_time + 0.001)
            prev_time = curr_time

            # 2. Leer Encoders por I2C (cada 0.3s para no saturar)
            if (curr_time - tiempo_ultima_telemetria) > 0.3:
                nueva_telemetria = leer_telemetria_segura()
                if nueva_telemetria: 
                    telemetria_actual = nueva_telemetria
                tiempo_ultima_telemetria = curr_time

            # 3. Dibujar HUD (Interfaz) en el Video
            cv2.line(frame, (0, int(alto*0.4)), (ancho, int(alto*0.4)), (255, 255, 255), 1) # Horizonte
            
            # Textos de Control y Estado
            cv2.putText(frame, f"ESTADO: {estado_texto}", (20, alto - 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            cv2.putText(frame, "Controles: W, A, S, D | Freno: Espacio | Salir: Q", (20, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Textos de Encoders (En cyan, arriba)
            cv2.putText(frame, f"ENC IZQ: {telemetria_actual['rpm_izq']} RPM", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"ENC DER: {telemetria_actual['rpm_der']} RPM", (ancho - 250, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
            cv2.putText(frame, f"FPS: {int(fps)}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

            # 4. Mostrar ventana
            cv2.imshow('M.A.V.I - Teleoperado', frame)

            # 5. LÓGICA DE TECLADO
            # waitKey espera 1 milisegundo por una tecla.
            key = cv2.waitKey(1) & 0xFF

            if key == ord('w'):
                cambiar_direccion(DIR_ADELANTE)
                estado_texto = "⬆️ AVANZANDO"
            elif key == ord('s'):
                cambiar_direccion(DIR_ATRAS)
                estado_texto = "⬇️ RETROCEDIENDO"
            elif key == ord('a'):
                cambiar_direccion(DIR_IZQUIERDA)
                estado_texto = "⬅️ GIRANDO IZQ"
            elif key == ord('d'):
                cambiar_direccion(DIR_DERECHA)
                estado_texto = "➡️ GIRANDO DER"
            elif key == ord(' ') or key == ord('x'): # Barra espaciadora o la 'X' para frenar
                cambiar_direccion(DIR_QUIETO)
                estado_texto = "⏹️ FRENADO"
            elif key == ord('q'):
                break # Salir del programa

    except KeyboardInterrupt:
        pass
    finally:
        cambiar_direccion(DIR_QUIETO)
        enviar_orden_segura(1, 0) 
        picam2.stop()
        cv2.destroyAllWindows()
        print("Sistemas apagados.")

if __name__ == "__main__":
    main()