#include <Arduino.h>
#include <Wire.h>

// =====================================================================
// 1. CONFIGURACIÓN I2C Y WATCHDOG DE CONEXIÓN
// =====================================================================
#define ESP32_I2C_ADDR 0x08
#define SDA_PIN 9
#define SCL_PIN 8

const unsigned long TIMEOUT_CONEXION_MS = 3000;
volatile unsigned long ultimoContactoI2C = 0;
bool conexionEstablecida = false;

// Registros que la Raspberry Pi LEE (telemetría)
volatile uint8_t reg_estado  = 1;
volatile uint8_t reg_rpm_izq = 0;
volatile uint8_t reg_rpm_der = 0;

// =====================================================================
// 2. PINES DE MOTORES (TB6612) Y ENCODERS
// =====================================================================
const int pinSTBY = 10;
const int pinPWMA = 11, pinAIN1 = 12, pinAIN2 = 13; // Motor A = Físicamente Derecho
const int pinPWMB = 14, pinBIN1 = 15, pinBIN2 = 16; // Motor B = Físicamente Izquierdo

const int encoderM1_A = 5,  encoderM1_B = 4;
const int encoderM2_A = 17, encoderM2_B = 7;

// =====================================================================
// 3. PARÁMETROS DE POTENCIA Y CALIBRACIÓN
// =====================================================================
const int freq = 20000;
const int resolution = 8;

float factorCompensacionA = 1.00;
float factorCompensacionB = 0.90;

const int PWM_MIN = 60;
const float PPR_IZQ = 1981.0;
const float PPR_DER = 1981.0;

// =====================================================================
// 4. VARIABLES DE ESTADO Y COLA DE COMANDOS
// =====================================================================
volatile long contadorM1 = 0, contadorM2 = 0;
long prevM1 = 0, prevM2 = 0;
unsigned long tiempoAnterior = 0;
volatile unsigned long ultimo_pulso_M1 = 0, ultimo_pulso_M2 = 0;

int contadorMuestras = 0;
float sumaRPM_M1 = 0, sumaRPM_M2 = 0;

// Cola atómica de 32 bits: [tipo | a | b]
volatile uint32_t cmd_pendiente = 0;

// =====================================================================
// 5. INTERRUPCIONES DE ENCODERS
// =====================================================================
void IRAM_ATTR ISR_EncoderM1() {
  unsigned long t = micros();
  if (t - ultimo_pulso_M1 > 300) {
    if (digitalRead(encoderM1_B) == HIGH) contadorM1 = contadorM1 + 1;
    else contadorM1 = contadorM1 - 1;
    ultimo_pulso_M1 = t;
  }
}

void IRAM_ATTR ISR_EncoderM2() {
  unsigned long t = micros();
  if (t - ultimo_pulso_M2 > 400) {
    if (digitalRead(encoderM2_B) == HIGH) contadorM2 = contadorM2 + 1;
    else contadorM2 = contadorM2 - 1;
    ultimo_pulso_M2 = t;
  }
}

// =====================================================================
// 6. CONTROL DE MOTORES (IZQUIERDA Y DERECHA CORREGIDAS)
// =====================================================================
void controlMotorA(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) {
    digitalWrite(pinAIN1, HIGH);
    digitalWrite(pinAIN2, LOW);
  } else {
    digitalWrite(pinAIN1, LOW);
    digitalWrite(pinAIN2, HIGH);
  }
  ledcWrite(pinPWMA, constrain((int)(velocidad * factorCompensacionA), 0, 255));
}

void controlMotorB(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) {
    digitalWrite(pinBIN1, HIGH);
    digitalWrite(pinBIN2, LOW);
  } else {
    digitalWrite(pinBIN1, LOW);
    digitalWrite(pinBIN2, HIGH);
  }
  ledcWrite(pinPWMB, constrain((int)(velocidad * factorCompensacionB), 0, 255));
}

void frenar() {
  digitalWrite(pinAIN1, HIGH); digitalWrite(pinAIN2, HIGH);
  digitalWrite(pinBIN1, HIGH); digitalWrite(pinBIN2, HIGH);
  ledcWrite(pinPWMA, 0);
  ledcWrite(pinPWMB, 0);
}

int porcentajeAPwm(int pct) {
  pct = constrain(pct, 0, 100);
  if (pct == 0) return 0;
  return PWM_MIN + (255 - PWM_MIN) * pct / 100;
}

// velIzq > 0 -> rueda izquierda avanza | velIzq < 0 -> rueda izquierda retrocede
// velDer > 0 -> rueda derecha avanza   | velDer < 0 -> rueda derecha retrocede
void moverRuedas(int velIzq, int velDer) {
  if (velIzq == 0 && velDer == 0) {
    frenar();
    return;
  }
  // Intercambiamos velIzq y velDer hacia Motor A y Motor B para corregir giro A/D
  bool dirA = (velDer < 0);
  bool dirB = (velIzq > 0);

  controlMotorA(porcentajeAPwm(abs(velDer)), dirA);
  controlMotorB(porcentajeAPwm(abs(velIzq)), dirB);
}

// =====================================================================
// 7. COMUNICACIÓN I2C
// =====================================================================
void receiveEvent(int howMany) {
  ultimoContactoI2C = millis();

  if (howMany >= 3) {
    uint8_t reg = Wire.read();

    if (reg == 3 && howMany >= 4) {
      // Registro 3: velocidades independientes [3, velI, velD, chk]
      uint8_t vi  = Wire.read();
      uint8_t vd  = Wire.read();
      uint8_t chk = Wire.read();
      if (chk == (uint8_t)(reg + vi + vd)) {
        reg_estado = 1;
        cmd_pendiente = ((uint32_t)2 << 16) | ((uint32_t)vi << 8) | vd;
      } else {
        reg_estado = 0;
      }
    } else {
      // Registro 1 (encendido/apagado) o Registro 2 (dirección fija)
      uint8_t val = Wire.read();
      uint8_t chk = Wire.read();
      if (chk == (uint8_t)(reg + val)) {
        reg_estado = 1;
        if (reg == 2) {
          cmd_pendiente = ((uint32_t)1 << 16) | ((uint32_t)val << 8);
        } else if (reg == 1) {
          cmd_pendiente = ((uint32_t)1 << 16); // Frena al encender/apagar
        }
      } else {
        reg_estado = 0;
      }
    }
  }
  while (Wire.available()) Wire.read();
}

void requestEvent() {
  ultimoContactoI2C = millis();
  uint8_t checksum = reg_estado + reg_rpm_izq + reg_rpm_der;
  uint8_t respuesta[4] = {reg_estado, reg_rpm_izq, reg_rpm_der, checksum};
  Wire.write(respuesta, 4);
}

bool iniciarBusI2C() {
  Wire.end();
  delay(50);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  return Wire.begin((uint8_t)ESP32_I2C_ADDR, SDA_PIN, SCL_PIN, 100000);
}

// =====================================================================
// 8. EJECUCIÓN DE COMANDOS Y CÁLCULO DE RPM
// =====================================================================
void aplicarComando() {
  uint32_t c = __atomic_exchange_n(&cmd_pendiente, (uint32_t)0, __ATOMIC_SEQ_CST);
  if (c == 0) return;

  uint8_t tipo = (c >> 16) & 0xFF;
  uint8_t a    = (c >> 8) & 0xFF;
  uint8_t b    = c & 0xFF;

  digitalWrite(pinSTBY, HIGH);

  if (tipo == 1) {
    switch (a) {
      case 0: frenar(); break;                                            // QUIETO
      case 1: controlMotorA(180, false); controlMotorB(180, true);  break; // ADELANTE
      case 2: controlMotorA(180, true);  controlMotorB(180, false); break; // ATRÁS
      case 3: controlMotorA(150, false); controlMotorB(150, false); break; // IZQUIERDA (corregido)
      case 4: controlMotorA(150, true);  controlMotorB(150, true);  break; // DERECHA   (corregido)
    }
  } else if (tipo == 2) {
    moverRuedas((int8_t)a, (int8_t)b);
  }
}

void actualizarRPM() {
  if (millis() - tiempoAnterior >= 100) {
    tiempoAnterior = millis();

    noInterrupts();
    long lecturaActualM1 = contadorM1, lecturaActualM2 = contadorM2;
    interrupts();

    long deltaM1 = lecturaActualM1 - prevM1;
    long deltaM2 = lecturaActualM2 - prevM2;
    prevM1 = lecturaActualM1;
    prevM2 = lecturaActualM2;

    sumaRPM_M1 += abs(((float)deltaM1 / PPR_IZQ) * 600.0);
    sumaRPM_M2 += abs(((float)deltaM2 / PPR_DER) * 600.0);
    contadorMuestras++;

    if (contadorMuestras >= 5) {
      reg_rpm_izq = (uint8_t)min(255.0f, sumaRPM_M1 / 5.0f);
      reg_rpm_der = (uint8_t)min(255.0f, sumaRPM_M2 / 5.0f);
      sumaRPM_M1 = 0;
      sumaRPM_M2 = 0;
      contadorMuestras = 0;
    }
  }
}

// =====================================================================
// 9. SETUP Y LOOP PRINCIPAL
// =====================================================================
void setup() {
  Serial.begin(115200);

  // Configurar todos los pines del TB6612 como salida
  pinMode(pinSTBY, OUTPUT);
  pinMode(pinAIN1, OUTPUT);
  pinMode(pinAIN2, OUTPUT);
  pinMode(pinBIN1, OUTPUT);
  pinMode(pinBIN2, OUTPUT);

  ledcAttach(pinPWMA, freq, resolution);
  ledcAttach(pinPWMB, freq, resolution);
  digitalWrite(pinSTBY, HIGH);
  frenar();

  // Configurar encoders
  pinMode(encoderM1_A, INPUT_PULLUP);
  pinMode(encoderM1_B, INPUT_PULLUP);
  pinMode(encoderM2_A, INPUT_PULLUP);
  pinMode(encoderM2_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderM1_A), ISR_EncoderM1, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderM2_A), ISR_EncoderM2, RISING);

  // Iniciar I2C
  bool ok = iniciarBusI2C();
  ultimoContactoI2C = millis();
  Serial.printf("I2C esclavo: %s | dir 0x%02X | SDA %d | SCL %d\n",
                ok ? "OK" : "FALLO", ESP32_I2C_ADDR, SDA_PIN, SCL_PIN);
}

void loop() {
  unsigned long ahora = millis();

  aplicarComando();
  actualizarRPM();

  // Watchdog de conexión I2C (si la Raspberry Pi aún está arrancando o perdió señal)
  if (ahora - ultimoContactoI2C >= TIMEOUT_CONEXION_MS) {
    frenar();
    if (conexionEstablecida) {
      Serial.println("Conexion I2C perdida. Reintentando...");
      conexionEstablecida = false;
    }
    iniciarBusI2C();
    ultimoContactoI2C = ahora;
  } else if (!conexionEstablecida && ultimoContactoI2C > 0) {
    conexionEstablecida = true;
    Serial.println("Conexion I2C establecida con la Raspberry Pi.");
  }
}