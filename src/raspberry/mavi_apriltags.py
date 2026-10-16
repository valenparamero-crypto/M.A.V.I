import cv2
import numpy as np
from picamera2 import Picamera2

# =====================================================================
# CONFIGURACIÓN DE TAGS
# =====================================================================
CONFIG_TAGS = {
    0: {"tipo": "IDENTIFICACION", "accion": "Estación de carga 1", "color": (0, 255, 0)},
    1: {"tipo": "IDENTIFICACION", "accion": "Estación de carga 2", "color": (0, 255, 0)},
    2: {"tipo": "IDENTIFICACION", "accion": "Estación de descarga 1", "color": (255, 255, 0)},
    6: {"tipo": "ORDEN", "accion": "Ir a Cargar 1", "color": (255, 0, 255)},
}

def main():
    print("Inicializando Hardware de Visión de M.A.V.I...")
    picam2 = Picamera2()
    config = picam2.create_video_configuration(
        main={"size": (640, 480), "format": "BGR888"}
    )
    picam2.configure(config)
    picam2.start()

    try:
        diccionario = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
        parametros = cv2.aruco.DetectorParameters()
        detector = cv2.aruco.ArucoDetector(diccionario, parametros)
    except AttributeError:
        print("[ERROR] Falta el módulo cv2.aruco.")
        picam2.stop()
        return

    print("\n--- Sistema M.A.V.I. Listo ---")

    try:
        while True:
            frame = picam2.capture_array()
            alto, ancho = frame.shape[:2]
            centro_robot = ancho // 2
            
            # Subimos el horizonte al 40% (para que vea el carril más a lo lejos)
            horizonte = int(alto * 0.40) 

            # Convertir a grises (ESTO SE USA PARA LOS TAGS: Es el 100% de la pantalla)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # =================================================================
            # MÓDULO 1: DETECCIÓN DE CARRILES (ROJO Y AMARILLO)
            # =================================================================
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Máscara de suelo (Solo del horizonte hacia abajo)
            mascara_suelo = np.zeros((alto, ancho), dtype=np.uint8)
            mascara_suelo[horizonte:alto, 0:ancho] = 255 

            # Filtros de color
            bajo_rojo1, alto_rojo1 = np.array([0, 120, 70]), np.array([10, 255, 255])
            bajo_rojo2, alto_rojo2 = np.array([170, 120, 70]), np.array([180, 255, 255])
            mask_rojo = cv2.bitwise_or(cv2.inRange(hsv, bajo_rojo1, alto_rojo1), cv2.inRange(hsv, bajo_rojo2, alto_rojo2))
            mask_rojo = cv2.bitwise_and(mask_rojo, mascara_suelo)

            bajo_amarillo, alto_amarillo = np.array([20, 100, 100]), np.array([35, 255, 255])
            mask_amarillo = cv2.inRange(hsv, bajo_amarillo, alto_amarillo)
            mask_amarillo = cv2.bitwise_and(mask_amarillo, mascara_suelo)

            # Lógica de dirección
            M_rojo = cv2.moments(mask_rojo)
            M_amarillo = cv2.moments(mask_amarillo)
            
            cx_rojo = int(M_rojo["m10"] / M_rojo["m00"]) if M_rojo["m00"] > 500 else 0
            cx_amarillo = int(M_amarillo["m10"] / M_amarillo["m00"]) if M_amarillo["m00"] > 500 else 0

            if cx_rojo > 0: cv2.circle(frame, (cx_rojo, int(M_rojo["m01"]/M_rojo["m00"])), 8, (0, 0, 255), -1)
            if cx_amarillo > 0: cv2.circle(frame, (cx_amarillo, int(M_amarillo["m01"]/M_amarillo["m00"])), 8, (0, 255, 255), -1)

            if cx_rojo > 0 and cx_amarillo > 0:
                centro_carril = (cx_rojo + cx_amarillo) // 2
                cy_medio = int((int(M_rojo["m01"]/M_rojo["m00"]) + int(M_amarillo["m01"]/M_amarillo["m00"])) / 2)
                
                cv2.line(frame, (centro_robot, alto), (centro_robot, alto - 50), (255, 255, 255), 2)
                cv2.line(frame, (centro_robot, alto), (centro_carril, cy_medio), (0, 255, 0), 3)
                
                if centro_carril < centro_robot - 30: estado_giro, color = "<< IZQUIERDA", (0, 165, 255)
                elif centro_carril > centro_robot + 30: estado_giro, color = "DERECHA >>", (0, 165, 255)
                else: estado_giro, color = "^^ RECTO ^^", (0, 255, 0)
                cv2.putText(frame, estado_giro, (centro_robot - 60, alto - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            # =================================================================
            # MÓDULO 2: DETECCIÓN DE OBSTÁCULOS (ZONA INFERIOR)
            # =================================================================
            zona_y1, zona_y2 = alto - 120, alto - 20
            zona_x1, zona_x2 = int(ancho * 0.25), int(ancho * 0.75)
            roi_peligro = gray[zona_y1:zona_y2, zona_x1:zona_x2] # Usamos el gray completo para cortar esto
            
            bordes = cv2.Canny(cv2.GaussianBlur(roi_peligro, (7, 7), 0), 50, 150)
            if cv2.countNonZero(bordes) > 400:
                cv2.rectangle(frame, (zona_x1, zona_y1), (zona_x2, zona_y2), (0, 0, 255), 2)
                cv2.putText(frame, "OBSTACULO!", (zona_x1, zona_y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # =================================================================
            # MÓDULO 3: LECTOR APRILTAGS (Busca en TODA la imagen 'gray')
            # =================================================================
            esquinas, ids, rechazados = detector.detectMarkers(gray)
            if ids is not None:
                cv2.aruco.drawDetectedMarkers(frame, esquinas, ids)
                for i, tag_id in enumerate(ids.flatten()):
                    x, y = int(esquinas[i][0][0][0]), int(esquinas[i][0][0][1]) - 30 
                    if tag_id in CONFIG_TAGS:
                        info = CONFIG_TAGS[tag_id]
                        cv2.putText(frame, f"[{tag_id}] {info['accion']}", (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, info['color'], 2)

            # =================================================================
            # HUD VISUAL (Línea de Horizonte)
            # =================================================================
            cv2.line(frame, (0, horizonte), (ancho, horizonte), (255, 255, 255), 1)
            cv2.putText(frame, "HORIZONTE (Abajo: Carriles | Todo: Tags)", (10, horizonte - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1)

            # Mostrar ventana principal
            cv2.imshow('M.A.V.I - Sistema Completo', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except KeyboardInterrupt:
        pass
    finally:
        picam2.stop()
        cv2.destroyAllWindows()
        print("Sistemas apagados.")

if __name__ == "__main__":
    main()