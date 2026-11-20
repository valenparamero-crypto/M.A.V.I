import cv2
import numpy as np
import time
import json
import os
import queue
import threading
import logging
from smbus2 import SMBus
from picamera2 import Picamera2
from flask import Flask, Response, request, jsonify

# =====================================================================
# 1. CONFIGURACIÓN I2C Y PROTOCOLO CON ESP32-S3
# =====================================================================
DIRECCION_ESP32 = 0x08
NUMERO_BUS = 1
ARCHIVO_CALIBRACION = "calibracion_mavi.json"

DIR_QUIETO = 0
DIR_ADELANTE = 1
DIR_ATRAS = 2
DIR_IZQUIERDA = 3
DIR_DERECHA = 4

telemetria_actual = {"estado": 1, "rpm_izq": 0, "rpm_der": 0}
tiempo_ultima_telemetria = 0
ultimas_velocidades = (0, 0)

def enviar_trama_i2c(bytes_datos, max_reintentos=2):
    """Envía [reg, ...datos, checksum] por I2C."""
    checksum = sum(bytes_datos) & 0xFF
    registro = bytes_datos[0]
    payload = bytes_datos[1:] + [checksum]
    for _ in range(max_reintentos):
        try:
            with SMBus(NUMERO_BUS) as bus:
                bus.write_i2c_block_data(DIRECCION_ESP32, registro, payload)
                return True
        except OSError:
            time.sleep(0.01)
    return False

def enviar_velocidades_ruedas(vel_izq, vel_der):
    """Usa el Registro 3 de tu ESP32-S3: [3, velI(int8), velD(int8), chk]."""
    global ultimas_velocidades
    # [CAMBIO 7] Compensa motores distintos. Positivo = le da más a la IZQUIERDA
    # y menos a la DERECHA (úsalo si el robot se tuerce hacia la izquierda).
    b = params["balance_motores"] / 100.0
    vel_izq = vel_izq * (1.0 + b)
    vel_der = vel_der * (1.0 - b)
    vi = int(np.clip(round(vel_izq), -100, 100))
    vd = int(np.clip(round(vel_der), -100, 100))
    if (vi, vd) == ultimas_velocidades:
        return
    vi_byte = vi & 0xFF
    vd_byte = vd & 0xFF
    if enviar_trama_i2c([3, vi_byte, vd_byte]):
        ultimas_velocidades = (vi, vd)

def frenar_robot():
    enviar_velocidades_ruedas(0, 0)
    enviar_trama_i2c([2, DIR_QUIETO])

def leer_telemetria_segura():
    try:
        with SMBus(NUMERO_BUS) as bus:
            data = bus.read_i2c_block_data(DIRECCION_ESP32, 0, 4)
            if data[3] == ((data[0] + data[1] + data[2]) & 0xFF):
                return {"estado": data[0], "rpm_izq": data[1], "rpm_der": data[2]}
    except Exception:
        pass
    return None

# =====================================================================
# 2. PARÁMETROS CALIBRABLES EN VIVO (SE GUARDAN EN JSON)
# =====================================================================
PUERTO_WEB = 5000
TIEMPO_SIN_WEB = 5.0   # s sin aviso de la página antes del freno de seguridad (antes 2.0)

# Resolución 16:9 panorámica: usa todo el ancho del sensor con menos píxeles que 640x480
ANCHO_CAM = 640
ALTO_CAM = 360

PARAMS_DEFAULT = {
    "vel_base": 45.0,       # Velocidad crucero en recta (0 a 100%)
    "vel_manual": 55.0,     # Velocidad en modo manual WASD (0 a 100%)
    "kp": 38.0,             # Ganancia Proporcional (reacción inmediata al error)
    "ki": 0.5,              # Ganancia Integral (corrige desvíos sostenidos)
    "kd": 14.0,             # Ganancia Derivativa (amortigua oscilaciones/zig-zag)
    "k_ang": 0.45,          # Anticipación de curva (lookahead angular)
    "freno_curva": 0.35,    # Reducción de velocidad en curvas cerradas (0.0 a 0.8)
    "offset_centro": 0.0,   # Desplazamiento lateral (-0.30 a +0.30)
    "fraccion_roi": 0.45,   # Altura desde donde analiza (0.25 = más lejos, 0.70 = más cerca)
    "invertir_giro": 0,     # 0 = normal, 1 = invierte dirección de giro
    # --- Color rojo (ajustable en vivo; la cámara le da un tinte rosado) ---
    "rojo_h": 10.0,         # Qué tan "ancho" es el rango de tonos rojos (más = acepta rojos rosados/naranjas)
    "rojo_s_min": 100.0,    # Saturación mínima: más bajo = acepta rojos más pálidos
    "rojo_v_min": 60.0,     # Brillo mínimo: más bajo = acepta rojos más oscuros
    # --- AprilTags ---
    "parar_en_tag": 0,      # 0 = solo detecta y muestra | 1 = frena en tags de estación (0 a 5)
    "tam_parada": 45.0,     # Tamaño del tag en pantalla (píxeles) para frenar: más grande = más cerca
    "pausa_tag": 3.0,       # Segundos que se queda quieto en la estación
    # --- Tope de giro (datos del análisis de estabilidad) ---
    "tope_giro": 2.0,       # 1.0 = gira justo lo de la curva | 2.0 = el doble | 3.5 = sin tope
    # --- Motores ---
    "balance_motores": 0.0, # % de compensación entre motores (+ = más fuerza a la izquierda)
    # --- Cruce con tag 6 (girar a la izquierda) ---
    "tam_tag_cruce": 40.0,  # Tamaño del tag 6 (px) para "prepararse"
    "espera_giro": 1.0,     # Segundos que sigue el carril después de ver el tag, antes de girar
    "giro_izq_tiempo": 1.5, # Segundos MÁXIMOS girando (para antes si ya encontró el carril nuevo)
    "giro_interior": 0.2    # Velocidad de la rueda izquierda al girar (0.2 = 20% de la derecha)
}

params = PARAMS_DEFAULT.copy()
if os.path.exists(ARCHIVO_CALIBRACION):
    try:
        with open(ARCHIVO_CALIBRACION, "r") as f:
            params.update(json.load(f))
    except Exception:
        pass

# =====================================================================
# 3. VISIÓN POR COMPUTADORA (CARRIL AZUL IZQ | ROJO DER)
# =====================================================================
NUM_BANDAS = 8
AREA_MIN_BANDA = 6        # Bajo para detectar líneas muy delgadas incluso a lo lejos
ANCHO_MAX_LINEA = 80      # Descarta bloques anchos (soportes morados, manos, ropa)
MIN_BANDAS_LINEA = 2
FRAMES_PERDIDA_MAX = 8

# Rojo saturado: corta tonos cálidos/naranja de piel humana (H > 6 y S < 155)
HSV_ROJO = [
    (np.array([0, 155, 65]),   np.array([6, 255, 255])),
    (np.array([172, 155, 65]), np.array([180, 255, 255]))
]

# Azul puro: corta el morado/violeta (H > 122)
HSV_AZUL = [
    (np.array([98, 125, 50]),  np.array([122, 255, 255]))
]
KERNEL = np.ones((3, 3), np.uint8)

# [CAMBIO 2] Ancho del carril POR FRANJA: por la perspectiva, el carril se ve
# angosto arriba (lejos) y ancho abajo (cerca), como los rieles de un tren.
# Arranca con un valor aproximado y se va aprendiendo solo cuando ve ambas líneas.
ancho_carril_banda = [ANCHO_CAM * (0.35 + 0.40 * i / (NUM_BANDAS - 1)) for i in range(NUM_BANDAS)]

# Dónde estaba el centro del carril (franja más cercana) en la foto anterior
centro_previo = ANCHO_CAM * 0.5

def candidatos_x(mascara_banda):
    """[CAMBIO 1] Separa cada línea de la franja por aparte y devuelve la X de cada una.
    Antes se promediaba todo el color junto: si se veían dos líneas rojas,
    el punto quedaba en el piso entre las dos."""
    n, _, stats, cents = cv2.connectedComponentsWithStats(mascara_banda, connectivity=8)
    alto_banda = mascara_banda.shape[0]
    xs = []
    for j in range(1, n):  # el 0 es el fondo
        w = stats[j, cv2.CC_STAT_WIDTH]
        h = stats[j, cv2.CC_STAT_HEIGHT]
        area = stats[j, cv2.CC_STAT_AREA]
        if area < AREA_MIN_BANDA:
            continue  # ruido (puntico suelto)
        # Una mancha ancha, que llena toda la franja, no es una línea (mano, ropa).
        # Una línea acostada en una curva SÍ pasa: es ancha pero delgada.
        if w > ANCHO_MAX_LINEA and h >= 0.8 * alto_banda and area > 0.6 * w * h:
            continue
        xs.append(float(cents[j][0]))
    return xs

def elegir_lineas(xs_azul, xs_roja, ref):
    """Escoge las líneas de NUESTRO carril: la azul más cercana a la izquierda
    del centro esperado y la roja más cercana a la derecha."""
    izq = [x for x in xs_azul if x < ref]
    der = [x for x in xs_roja if x > ref]
    xa = max(izq) if izq else None
    xr = min(der) if der else None
    return xa, xr

def reiniciar_vision():
    global centro_previo
    centro_previo = ANCHO_CAM * 0.5

def detectar_carril(frame):
    global centro_previo

    alto, ancho = frame.shape[:2]
    y0 = int(alto * np.clip(params["fraccion_roi"], 0.25, 0.75))
    # Desenfoque suave (3x3) para no difuminar líneas muy delgadas
    roi = cv2.GaussianBlur(frame[y0:alto, :], (3, 3), 0)
    hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    mask_azul = np.zeros(hsv.shape[:2], np.uint8)
    for lo, hi in HSV_AZUL:
        mask_azul |= cv2.inRange(hsv, lo, hi)

    # [CAMBIO 5] El rojo se arma con los valores del panel, para calibrarlo en vivo.
    # El rojo está en los dos extremos del círculo de tonos (0 y 180).
    h = int(np.clip(params["rojo_h"], 1, 30))
    s = int(np.clip(params["rojo_s_min"], 0, 255))
    v = int(np.clip(params["rojo_v_min"], 0, 255))
    rangos_rojo = [(np.array([0, s, v]), np.array([h, 255, 255])),
                   (np.array([180 - h, s, v]), np.array([180, 255, 255]))]
    mask_roja = np.zeros(hsv.shape[:2], np.uint8)
    for lo, hi in rangos_rojo:
        mask_roja |= cv2.inRange(hsv, lo, hi)

    # Cierre morfológico suave (1 iteración) para unir trazos delgados sin ensancharlos
    mask_azul = cv2.morphologyEx(mask_azul, cv2.MORPH_CLOSE, KERNEL, iterations=1)
    mask_roja = cv2.morphologyEx(mask_roja, cv2.MORPH_CLOSE, KERNEL, iterations=1)

    alto_roi = hsv.shape[0]
    puntos = [None] * NUM_BANDAS

    # Se recorre de ABAJO (cerca) hacia ARRIBA (lejos): cada franja usa el centro
    # de la franja de abajo como referencia. Así se "sigue" el carril en la curva.
    ref = centro_previo
    for i in reversed(range(NUM_BANDAS)):
        ya = i * alto_roi // NUM_BANDAS
        yb = (i + 1) * alto_roi // NUM_BANDAS
        xa, xr = elegir_lineas(candidatos_x(mask_azul[ya:yb, :]),
                               candidatos_x(mask_roja[ya:yb, :]), ref)

        medio = None
        if xa is not None and xr is not None:
            medio = (xa + xr) * 0.5
            medido = xr - xa
            if 0.15 * ancho < medido < 0.95 * ancho:  # solo si el valor es razonable
                ancho_carril_banda[i] = 0.85 * ancho_carril_banda[i] + 0.15 * medido
        elif xa is not None:
            medio = xa + ancho_carril_banda[i] * 0.5
        elif xr is not None:
            medio = xr - ancho_carril_banda[i] * 0.5

        if medio is not None:
            ref = medio

        puntos[i] = {
            "y": y0 + (ya + yb) // 2,
            "azul": xa,
            "rojo": xr,
            "medio": medio,
            "estimado": (xa is None or xr is None) and (medio is not None)
        }

    # Recordar el centro más cercano para la próxima foto
    cercanos = [p["medio"] for p in reversed(puntos) if p["medio"] is not None]
    centro_previo = cercanos[0] if cercanos else ancho * 0.5

    xs_azul = [p["azul"] for p in puntos if p["azul"] is not None]
    xs_roja = [p["rojo"] for p in puntos if p["rojo"] is not None]
    ve_azul = len(xs_azul) >= MIN_BANDAS_LINEA
    ve_roja = len(xs_roja) >= MIN_BANDAS_LINEA

    if ve_azul and ve_roja:
        situacion = "AMBAS"
    elif ve_azul:
        situacion = "SOLO_AZUL"
    elif ve_roja:
        situacion = "SOLO_ROJA"
    else:
        return puntos, "NINGUNA", 0.0, 0.0, mask_azul, mask_roja, y0

    validos = [(i, p["medio"]) for i, p in enumerate(puntos) if p["medio"] is not None]
    if not validos:
        return puntos, "NINGUNA", 0.0, 0.0, mask_azul, mask_roja, y0

    suma_x, suma_w = 0.0, 0.0
    for idx, cx in validos:
        peso = 1.0 + (idx / max(1, NUM_BANDAS - 1)) * 1.5
        suma_x += cx * peso
        suma_w += peso
    centro_ponderado = suma_x / suma_w
    error_pos = ((centro_ponderado - (ancho * 0.5)) / (ancho * 0.5)) - params["offset_centro"]

    if len(validos) >= 2:
        x_lejano = validos[0][1]
        x_cercano = validos[-1][1]
        error_ang = (x_lejano - x_cercano) / (ancho * 0.5)
    else:
        error_ang = 0.0

    return puntos, situacion, float(error_pos), float(error_ang), mask_azul, mask_roja, y0

# =====================================================================
# 4. CONTROLADOR PID DIFERENCIAL CONTINUO
# =====================================================================
# Medidas del robot y de la pista (análisis de estabilidad del equipo)
ANCHO_RUEDAS = 0.20   # m: distancia entre rueda IZQUIERDA y DERECHA
RADIO_CURVA = 0.32    # m: radio de la curva, en el centro del carril
FACTOR_CURVA = ANCHO_RUEDAS / (2 * RADIO_CURVA)   # = 0.31 -> rueda externa +31%, interna -31%

class ControladorCarrilPID:
    def __init__(self):
        self.integral = 0.0
        self.error_previo = 0.0
        self.derivada_filtrada = 0.0
        self.ultimo_tiempo = time.time()
        self.frames_perdidos = 0
        self.situacion_previa = None
        self.ultimo_giro = 0.0

    def reset(self):
        self.integral = 0.0
        self.error_previo = 0.0
        self.derivada_filtrada = 0.0
        self.ultimo_tiempo = time.time()
        self.frames_perdidos = 0
        self.situacion_previa = None
        self.ultimo_giro = 0.0
        reiniciar_vision()

    def calcular(self, situacion, error_pos, error_ang):
        ahora = time.time()
        dt = np.clip(ahora - self.ultimo_tiempo, 0.005, 0.2)
        self.ultimo_tiempo = ahora

        if situacion == "NINGUNA":
            self.frames_perdidos += 1
            if self.frames_perdidos >= FRAMES_PERDIDA_MAX:
                self.reset()
                return 0.0, 0.0, 0.0, "AUTO: CARRIL PERDIDO (FRENADO)"
            # [CAMBIO 4] Sigue girando hacia el último lado donde vio el carril,
            # despacio, en vez de frenar de golpe.
            vel = params["vel_base"] * 0.5
            g = float(np.clip(self.ultimo_giro, -vel, vel))
            return vel + g, vel - g, 0.0, "AUTO: BUSCANDO..."

        self.frames_perdidos = 0

        error_total = error_pos + params["k_ang"] * error_ang
        self.integral = np.clip(self.integral + error_total * dt, -0.5, 0.5)

        # [CAMBIO 3] Si cambió lo que ve (p. ej. de AMBAS a SOLO_AZUL), el error
        # salta de golpe. Ese salto no es real: no se usa para la parte D.
        if situacion != self.situacion_previa:
            self.error_previo = error_total
        self.situacion_previa = situacion

        derivada_cruda = (error_total - self.error_previo) / dt
        self.derivada_filtrada = 0.6 * self.derivada_filtrada + 0.4 * derivada_cruda
        self.error_previo = error_total

        giro = (
            params["kp"] * error_total
            + params["ki"] * self.integral
            + params["kd"] * self.derivada_filtrada
        )

        if int(params["invertir_giro"]) == 1:
            giro = -giro
        factor_freno = 1.0 - params["freno_curva"] * min(1.0, abs(error_total))
        vel_crucero = params["vel_base"] * max(0.35, factor_freno)

        # [CAMBIO 6] Tope de giro con las medidas del robot y de la pista.
        # En una curva perfecta: rueda externa = v*(1 + W/2R), interna = v*(1 - W/2R).
        # Se deja girar hasta "tope_giro" veces eso (para poder corregir), no más.
        # tope_giro = 1.0 -> justo lo de la curva | 3.5 -> sin tope (como antes)
        topado = False
        if params["tope_giro"] < 3.5:
            giro_max = vel_crucero * FACTOR_CURVA * params["tope_giro"]
            if abs(giro) > giro_max:
                giro = float(np.sign(giro) * giro_max)
                topado = True
        self.ultimo_giro = giro

        vel_izq = np.clip(vel_crucero + giro, -100.0, 100.0)
        vel_der = np.clip(vel_crucero - giro, -100.0, 100.0)

        estado = f"AUTO [{situacion}] E:{error_total:+.2f} | I:{vel_izq:.0f}% D:{vel_der:.0f}%"
        if topado:
            estado += " TOPE"
        return vel_izq, vel_der, error_total, estado

pid = ControladorCarrilPID()

# =====================================================================
# 4B. APRILTAGS (familia tag36h11)  [NUEVO]
# =====================================================================
NOMBRES_TAGS = {
    0: "Estacion de carga 1",   1: "Estacion de carga 2",
    2: "Estacion de descarga 1", 3: "Estacion de descarga 2",
    4: "Estacion de descarga 3", 5: "Estacion de descarga 4",
    6: "Descarga 3 y 4 a la izq", 7: "Giro obligatorio izq",
    8: "Ir a descarga 1", 9: "Ir a descarga 2",
    10: "Ir a descarga 3", 11: "Ir a descarga 4",
    12: "Ir a carga 2", 13: "Ir a carga 1",
}
TAGS_ESTACION = (0, 1, 2, 3, 4, 5)
ENFRIAMIENTO_TAG = 8.0  # s: después de la pausa, no vuelve a parar en ese mismo tag

def crear_detector_tags():
    """Funciona con OpenCV nuevo (4.7 o más) y viejo. Devuelve una función o None."""
    if not hasattr(cv2, "aruco"):
        return None
    dic = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_APRILTAG_36h11)
    if hasattr(cv2.aruco, "ArucoDetector"):            # OpenCV nuevo
        det = cv2.aruco.ArucoDetector(dic, cv2.aruco.DetectorParameters())
        return lambda gris: det.detectMarkers(gris)
    parametros = cv2.aruco.DetectorParameters_create()  # OpenCV viejo
    return lambda gris: cv2.aruco.detectMarkers(gris, dic, parameters=parametros)

detector_tags = crear_detector_tags()

def detectar_tags(frame):
    """Devuelve una lista de tags vistos: id, esquinas, centro y tamaño (lado en px)."""
    if detector_tags is None:
        return []
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    esquinas, ids, _ = detector_tags(gris)
    tags = []
    if ids is None:
        return tags
    for esq, id_tag in zip(esquinas, ids.flatten()):
        pts = esq.reshape(4, 2)
        lado = float(np.mean([np.linalg.norm(pts[k] - pts[(k + 1) % 4]) for k in range(4)]))
        tags.append({"id": int(id_tag), "pts": pts, "centro": pts.mean(axis=0), "lado": lado})
    return tags

class GestorTags:
    """Decide si el robot debe frenar en una estación."""
    def __init__(self):
        self.pausa_hasta = 0.0
        self.ultimo_parado = None
        self.tiempo_parado = 0.0
        self.texto = "TAG: ---"
        self.t_visto = 0.0

    def actualizar(self, tags, ahora):
        if tags:
            t = max(tags, key=lambda d: d["lado"])  # el más cercano
            self.texto = f"TAG {t['id']}: {NOMBRES_TAGS.get(t['id'], 'desconocido')} ({t['lado']:.0f}px)"
            self.t_visto = ahora
        elif ahora - self.t_visto > 1.0:
            self.texto = "TAG: ---"   # ya no ve ninguno: no deja el número viejo

        if not modo_auto or int(params["parar_en_tag"]) != 1:
            return
        for t in tags:
            cerca = t["lado"] >= params["tam_parada"]
            repetido = (t["id"] == self.ultimo_parado and
                        ahora - self.tiempo_parado < params["pausa_tag"] + ENFRIAMIENTO_TAG)
            if t["id"] in TAGS_ESTACION and cerca and not repetido:
                self.pausa_hasta = ahora + params["pausa_tag"]
                self.ultimo_parado = t["id"]
                self.tiempo_parado = ahora
                break

    def en_pausa(self, ahora):
        return ahora < self.pausa_hasta

gestor_tags = GestorTags()

# =====================================================================
# 4C. CRUCE: GIRAR A LA IZQUIERDA CUANDO VE EL TAG 6  [NUEVO]
# =====================================================================
# Si ve el tag 6 -> en el próximo cruce gira a la izquierda.
# Si NO lo ve    -> no hace nada especial: sigue la roja de afuera (derecho).
TAGS_IZQUIERDA = (6,)   # se puede agregar el 7 (giro obligatorio): (6, 7)
GIRO_MIN = 0.5          # s: gira al menos esto antes de aceptar el carril nuevo
IGNORAR_TRAS_GIRO = 5.0 # s: después de girar, ignora el tag 6 (para no repetir)

class GestorCruce:
    """
    NORMAL     -> sigue el carril. Si ve el tag 6 cerca, pasa a PREPARADO.
    PREPARADO  -> sigue el carril "espera_giro" segundos (llegando al hueco).
    GIRANDO    -> rueda izq lenta, der normal, hasta ver el carril nuevo
                  centrado (o hasta "giro_izq_tiempo"). Luego vuelve a NORMAL.
    """
    def __init__(self):
        self.estado = "NORMAL"
        self.t_estado = 0.0
        self.ignorar_hasta = 0.0

    def reset(self):
        self.estado = "NORMAL"
        self.t_estado = 0.0

    def actualizar(self, tags, situacion, err_pos, ahora):
        """Devuelve (vel_izq, vel_der, texto) si el cruce manda, o None si manda el PID."""
        t = ahora - self.t_estado

        if self.estado == "NORMAL":
            if ahora >= self.ignorar_hasta and any(
                    d["id"] in TAGS_IZQUIERDA and d["lado"] >= params["tam_tag_cruce"] for d in tags):
                self.estado, self.t_estado = "PREPARADO", ahora
            return None

        if self.estado == "PREPARADO":
            if t < params["espera_giro"]:
                return None                     # sigue el carril con el PID
            self.estado, self.t_estado = "GIRANDO", ahora
            t = 0.0

        # GIRANDO
        encontro = t >= GIRO_MIN and situacion == "AMBAS" and abs(err_pos) < 0.35
        if encontro or t >= params["giro_izq_tiempo"]:
            self.reset()
            self.ignorar_hasta = ahora + IGNORAR_TRAS_GIRO
            pid.reset()                         # el PID retoma limpio en el carril nuevo
            return None
        v = params["vel_base"]
        return v * params["giro_interior"], v, f"CRUCE: GIRANDO IZQ ({t:.1f}s)"

gestor_cruce = GestorCruce()

# =====================================================================
# 5. SERVIDOR WEB CON PANEL DE CALIBRACIÓN EN VIVO
# =====================================================================
modo_auto = False
estado_texto = "QUIETO (W/A/S/D)"
ultimo_ping = time.time()
cola_teclas = queue.Queue()
lock_frame = threading.Lock()
ultimo_jpg = None

PAGINA = """<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>M.A.V.I - Control PID</title>
<style>
  body{margin:0;background:#121212;color:#e0e0e0;font-family:system-ui,sans-serif;display:flex;flex-direction:column;align-items:center}
  .contenedor{display:flex;flex-wrap:wrap;justify-content:center;gap:16px;max-width:1440px;padding:12px;width:100%;box-sizing:border-box}
  .visor{flex:1 1 680px;text-align:center}
  img{width:100%;max-width:860px;border-radius:8px;border:1px solid #333}
  .controles{margin-top:10px}
  button{background:#252525;color:#fff;border:1px solid #444;border-radius:6px;padding:10px 16px;margin:3px;font-size:15px;cursor:pointer}
  button:hover{background:#333}
  button.auto{background:#0d47a1;border-color:#1976d2}
  button.stop{background:#b71c1c;border-color:#d32f2f}
  .panel{flex:1 1 300px;background:#1e1e1e;padding:16px;border-radius:8px;border:1px solid #333;max-width:380px}
  .panel h3{margin-top:0;font-size:16px;border-bottom:1px solid #333;padding-bottom:8px}
  .slider-row{margin-bottom:10px;text-align:left}
  .slider-row label{display:flex;justify-content:space-between;font-size:13px;margin-bottom:3px}
  input[type=range]{width:100%;accent-color:#2196f3}
  .acciones{display:flex;gap:8px;margin-top:12px}
  .acciones button{flex:1;font-size:13px;padding:8px}
</style></head><body>
<div class="contenedor">
  <div class="visor">
    <img src="/video">
    <div class="controles">
      <button onclick="e('a')">&#9664; IZQ</button>
      <button onclick="e('w')">&#9650; ADEL</button>
      <button onclick="e('s')">&#9660; ATRAS</button>
      <button onclick="e('d')">DER &#9654;</button>
      <button class="stop" onclick="e('x')">STOP</button>
      <button class="auto" onclick="e('m')">AUTO (M)</button>
    </div>
    <p style="font-size:12px;color:#888">Teclado: W A S D mover &middot; ESPACIO frenar &middot; M alternar autónomo</p>
  </div>

  <div class="panel">
    <h3>Calibración PID en Vivo</h3>
    <div id="sliders"></div>
    <div class="acciones">
      <button onclick="guardar()" style="background:#1b5e20;border-color:#2e7d32">Guardar</button>
      <button onclick="resetear()">Restaurar Default</button>
    </div>
    <p id="msg" style="font-size:12px;color:#4caf50;text-align:center;margin-bottom:0"></p>
  </div>
</div>

<script>
const CONFIG = [
  {k:'vel_base',      nom:'Velocidad Crucero (%)',  min:15,  max:100, step:1},
  {k:'kp',            nom:'Kp (Giro Proporcional)', min:0,   max:100, step:1},
  {k:'kd',            nom:'Kd (Amortiguación)',     min:0,   max:50,  step:0.5},
  {k:'ki',            nom:'Ki (Corrección Fija)',   min:0,   max:10,  step:0.1},
  {k:'k_ang',         nom:'Anticipación Curva',     min:0,   max:1.5, step:0.05},
  {k:'freno_curva',   nom:'Freno en Curvas',        min:0,   max:0.8, step:0.05},
  {k:'offset_centro', nom:'Offset Centro Cámara',   min:-0.3,max:0.3, step:0.01},
  {k:'fraccion_roi',  nom:'Altura Horizonte (ROI)', min:0.25,max:0.70,step:0.02},
  {k:'invertir_giro', nom:'Invertir Giro (0 / 1)',  min:0,   max:1,   step:1},
  {k:'rojo_s_min',    nom:'Rojo: Intensidad Mínima', min:40, max:200, step:5},
  {k:'rojo_h',        nom:'Rojo: Rango de Tono',    min:3,   max:25,  step:1},
  {k:'rojo_v_min',    nom:'Rojo: Brillo Mínimo',    min:20,  max:200, step:5},
  {k:'tope_giro',     nom:'Tope de Giro (1=curva, 3.5=sin tope)', min:1, max:3.5, step:0.1},
  {k:'balance_motores', nom:'Balance Motores (+ = más a la IZQ)', min:-30, max:30, step:1},
  {k:'tam_tag_cruce', nom:'Tag 6: Tamaño para Prepararse (px)', min:15, max:120, step:1},
  {k:'espera_giro',   nom:'Tag 6: Espera antes de Girar (s)', min:0, max:4, step:0.1},
  {k:'giro_izq_tiempo', nom:'Tag 6: Tiempo Máx. Girando (s)', min:0.5, max:4, step:0.1},
  {k:'giro_interior', nom:'Tag 6: Rueda Izq al Girar (0=pivote)', min:0, max:0.8, step:0.05},
  {k:'parar_en_tag',  nom:'Frenar en Estación (0 / 1)', min:0, max:1, step:1},
  {k:'tam_parada',    nom:'Tamaño Tag para Frenar (px)', min:15, max:150, step:1},
  {k:'pausa_tag',     nom:'Pausa en Estación (s)',  min:0.5, max:10, step:0.5}
];

function e(k){ fetch('/cmd/'+k); }
const MAPA={w:'w',a:'a',s:'s',d:'d',' ':'x',x:'x',m:'m'};
document.addEventListener('keydown',ev=>{
  const k=MAPA[ev.key.toLowerCase()];
  if(k && !ev.repeat){ ev.preventDefault(); e(k); }
});
setInterval(()=>fetch('/ping'), 500);

async function cargarSliders(){
  const res = await fetch('/params');
  const data = await res.json();
  const cont = document.getElementById('sliders');
  cont.innerHTML = '';
  CONFIG.forEach(c => {
    const val = data[c.k];
    cont.innerHTML += `
      <div class="slider-row">
        <label><span>${c.nom}</span><strong id="v_${c.k}">${val}</strong></label>
        <input type="range" min="${c.min}" max="${c.max}" step="${c.step}" value="${val}"
               oninput="actualizar('${c.k}', this.value)">
      </div>`;
  });
}

function actualizar(k, val){
  document.getElementById('v_'+k).innerText = val;
  fetch('/params', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({[k]: parseFloat(val)})
  });
}

async function guardar(){
  await fetch('/params/save', {method:'POST'});
  document.getElementById('msg').innerText = 'Calibración guardada en Raspberry Pi.';
  setTimeout(()=>document.getElementById('msg').innerText='', 2500);
}

async function resetear(){
  await fetch('/params/reset', {method:'POST'});
  cargarSliders();
}

cargarSliders();
</script></body></html>"""

app = Flask(__name__)

@app.route("/")
def index():
    return PAGINA

@app.route("/cmd/<k>")
def cmd(k):
    global ultimo_ping
    ultimo_ping = time.time()
    if k in ('w', 'a', 's', 'd', 'x', 'm'):
        cola_teclas.put(k)
    return "ok"

@app.route("/ping")
def ping():
    global ultimo_ping
    ultimo_ping = time.time()
    return "ok"

@app.route("/params", methods=["GET", "POST"])
def api_params():
    if request.method == "POST":
        datos = request.get_json(silent=True) or {}
        for k, v in datos.items():
            if k in params:
                params[k] = float(v)
        return jsonify({"ok": True})
    return jsonify(params)

@app.route("/params/save", methods=["POST"])
def api_params_save():
    with open(ARCHIVO_CALIBRACION, "w") as f:
        json.dump(params, f, indent=2)
    return jsonify({"ok": True})

@app.route("/params/reset", methods=["POST"])
def api_params_reset():
    params.update(PARAMS_DEFAULT)
    pid.reset()
    return jsonify({"ok": True})

def generar_mjpeg():
    while True:
        with lock_frame:
            jpg = ultimo_jpg
        if jpg:
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + jpg + b"\r\n"
        time.sleep(0.08)  # ~12 fotos/s al navegador: menos carga para la conexión

@app.route("/video")
def video():
    return Response(generar_mjpeg(), mimetype="multipart/x-mixed-replace; boundary=frame")

def iniciar_servidor():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    app.run(host="0.0.0.0", port=PUERTO_WEB, threaded=True)

# =====================================================================
# 6. PROCESAMIENTO DE TECLAS MANUALES
# =====================================================================
def procesar_tecla(k):
    global modo_auto, estado_texto
    if k == 'm':
        modo_auto = not modo_auto
        pid.reset()
        gestor_tags.pausa_hasta = 0.0
        gestor_cruce.reset()
        if modo_auto:
            estado_texto = "AUTONOMO PID ACTIVADO"
        else:
            frenar_robot()
            estado_texto = "MANUAL - FRENADO"
        return

    modo_auto = False
    pid.reset()
    v = params["vel_manual"]
    if k == 'w':
        enviar_velocidades_ruedas(v, v)
        estado_texto = f"MANUAL: ADELANTE ({v:.0f}%)"
    elif k == 's':
        enviar_velocidades_ruedas(-v, -v)
        estado_texto = f"MANUAL: ATRAS ({v:.0f}%)"
    elif k == 'a':
        enviar_velocidades_ruedas(-v * 0.7, v * 0.7)
        estado_texto = "MANUAL: GIRO IZQ"
    elif k == 'd':
        enviar_velocidades_ruedas(v * 0.7, -v * 0.7)
        estado_texto = "MANUAL: GIRO DER"
    elif k == 'x':
        frenar_robot()
        estado_texto = "MANUAL: FRENADO"

# =====================================================================
# 7. BUCLE PRINCIPAL
# =====================================================================
def main():
    global telemetria_actual, tiempo_ultima_telemetria, ultimo_jpg
    global modo_auto, estado_texto

    print("Iniciando M.A.V.I con Control Diferencial PID (Vista Panorámica 16:9)...")
    enviar_trama_i2c([1, 1])
    frenar_robot()

    picam2 = Picamera2()
    # Formato panorámico 16:9 (640x360) para máximo ángulo horizontal sin recortar el sensor
    config = picam2.create_video_configuration(
        main={"size": (ANCHO_CAM, ALTO_CAM), "format": "RGB888"}
    )
    picam2.configure(config)
    picam2.start()

    threading.Thread(target=iniciar_servidor, daemon=True).start()
    print(f"Interfaz web lista en: http://<IP-de-la-Pi>:{PUERTO_WEB}")

    prev_time = time.time()

    try:
        while True:
            frame = picam2.capture_array()
            alto, ancho = frame.shape[:2]
            curr_time = time.time()
            fps = 1.0 / max(0.001, curr_time - prev_time)
            prev_time = curr_time

            while not cola_teclas.empty():
                procesar_tecla(cola_teclas.get())

            if (curr_time - ultimo_ping) > TIEMPO_SIN_WEB and ultimas_velocidades != (0, 0):
                modo_auto = False
                pid.reset()
                frenar_robot()
                estado_texto = "SIN CONEXION WEB - FRENADO"

            if (curr_time - tiempo_ultima_telemetria) > 0.3:
                nueva = leer_telemetria_segura()
                if nueva:
                    telemetria_actual = nueva
                tiempo_ultima_telemetria = curr_time

            # AprilTags: se buscan en la foto completa, ANTES de dibujar encima
            tags = detectar_tags(frame)
            gestor_tags.actualizar(tags, curr_time)

            puntos, situacion, err_pos, err_ang, mask_azul, mask_roja, y0 = detectar_carril(frame)

            if modo_auto:
                if gestor_tags.en_pausa(curr_time):
                    enviar_velocidades_ruedas(0, 0)
                    pid.reset()  # al arrancar de nuevo, el PID empieza limpio
                    falta = gestor_tags.pausa_hasta - curr_time
                    estado_texto = f"AUTO: EN ESTACION (TAG {gestor_tags.ultimo_parado}) {falta:.1f}s"
                else:
                    control = gestor_cruce.actualizar(tags, situacion, err_pos, curr_time)
                    if control is not None:             # el cruce manda (girando)
                        v_izq, v_der, estado_texto = control
                        enviar_velocidades_ruedas(v_izq, v_der)
                    else:                               # manda el PID (normal)
                        v_izq, v_der, error_total, estado_texto = pid.calcular(situacion, err_pos, err_ang)
                        enviar_velocidades_ruedas(v_izq, v_der)
                        if gestor_cruce.estado == "PREPARADO":
                            falta = params["espera_giro"] - (curr_time - gestor_cruce.t_estado)
                            estado_texto = f"TAG 6: GIRO IZQ EN {max(0.0, falta):.1f}s"

            # --- HUD Visual sobre el video ---
            zona = frame[y0:alto, :]
            zona[mask_azul > 0] = (255, 120, 0)
            zona[mask_roja > 0] = (0, 0, 255)
            cv2.line(frame, (0, y0), (ancho, y0), (200, 200, 200), 1)

            objetivo_x = int(ancho * 0.5 * (1.0 + params["offset_centro"]))
            cv2.line(frame, (objetivo_x, y0), (objetivo_x, alto), (255, 255, 255), 1)

            medios = []
            for p in puntos:
                y = p["y"]
                if p["azul"] is not None:
                    cv2.circle(frame, (int(p["azul"]), y), 5, (255, 255, 0), -1)
                if p["rojo"] is not None:
                    cv2.circle(frame, (int(p["rojo"]), y), 5, (0, 255, 255), -1)
                if p["medio"] is not None:
                    color_centro = (0, 165, 255) if p["estimado"] else (0, 255, 0)
                    cv2.circle(frame, (int(p["medio"]), y), 5, color_centro, -1)
                    medios.append((int(p["medio"]), y))

            if len(medios) > 1:
                cv2.polylines(frame, [np.array(medios, np.int32)], False, (0, 255, 0), 2)

            # Recuadro morado y número sobre cada AprilTag detectado
            for t in tags:
                cv2.polylines(frame, [t["pts"].astype(np.int32)], True, (255, 0, 255), 2)
                cx, cy = t["centro"].astype(int)
                cv2.putText(frame, f"ID {t['id']}", (cx - 25, cy - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 255), 2)
            texto_tag = gestor_tags.texto if detector_tags else "TAG: OpenCV sin modulo aruco"
            cv2.putText(frame, texto_tag, (10, 66),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

            cv2.putText(frame, f"VEO: {situacion} | POS: {err_pos:+.2f} | ANG: {err_ang:+.2f}",
                        (10, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 255), 2)
            cv2.putText(frame, estado_texto, (10, alto - 12),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
            cv2.putText(frame, f"RPM IZQ: {telemetria_actual['rpm_izq']} | DER: {telemetria_actual['rpm_der']} | FPS: {int(fps)}",
                        (10, 44), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (255, 255, 255), 1)

            ok, buf = cv2.imencode(".jpg", frame, [cv2.IMWRITE_JPEG_QUALITY, 55])
            if ok:
                with lock_frame:
                    ultimo_jpg = buf.tobytes()

    except KeyboardInterrupt:
        pass
    finally:
        frenar_robot()
        enviar_trama_i2c([1, 0])
        picam2.stop()
        print("Sistemas apagados.")

if __name__ == "__main__":
    main()