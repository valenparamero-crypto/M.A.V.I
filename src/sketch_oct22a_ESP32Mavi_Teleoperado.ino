#include <Wire.h> 

// ==========================================
// --- CONFIGURACIÓN I2C ---
// ==========================================
#define ESP32_I2C_ADDR 0x08
#define SDA_PIN 8
#define SCL_PIN 9

uint8_t reg_estado = 1;
uint8_t reg_rpm_izq = 0;
uint8_t reg_rpm_der = 0;

// ==========================================
// --- PINES DE MOTORES Y ENCODERS ---
// ==========================================
const int pinSTBY = 10, pinPWMA = 11, pinAIN1 = 12, pinAIN2 = 13;
const int pinPWMB = 14, pinBIN1 = 15, pinBIN2 = 16;
const int encoderM1_A = 5, encoderM1_B = 4; 
const int encoderM2_A = 17, encoderM2_B = 7; 

const int freq = 20000;    
const int resolution = 8;  
float factorCompensacionA = 1.00; 
float factorCompensacionB = 0.90; 
const float PPR_IZQ = 1981.0, PPR_DER = 1981.0; 

volatile long contadorM1 = 0, contadorM2 = 0;
long prevM1 = 0, prevM2 = 0;
unsigned long tiempoAnterior = 0;
volatile unsigned long ultimo_pulso_M1 = 0, ultimo_pulso_M2 = 0;

int contadorMuestras = 0;
float sumaRPM_M1 = 0, sumaRPM_M2 = 0;

// ==========================================
// --- FUNCIONES DE HARDWARE ---
// ==========================================
void IRAM_ATTR ISR_EncoderM1() {
  unsigned long tiempo_actual = micros();
  if (tiempo_actual - ultimo_pulso_M1 > 300) { 
    if (digitalRead(encoderM1_B) == HIGH) contadorM1++; else contadorM1--;
    ultimo_pulso_M1 = tiempo_actual;
  }
}

void IRAM_ATTR ISR_EncoderM2() {
  unsigned long tiempo_actual = micros();
  if (tiempo_actual - ultimo_pulso_M2 > 400) { 
    if (digitalRead(encoderM2_B) == HIGH) contadorM2++; else contadorM2--;
    ultimo_pulso_M2 = tiempo_actual;
  }
}

void controlMotorA(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) { digitalWrite(pinAIN1, HIGH); digitalWrite(pinAIN2, LOW); } 
  else { digitalWrite(pinAIN1, LOW); digitalWrite(pinAIN2, HIGH); }
  ledcWrite(pinPWMA, constrain(velocidad * factorCompensacionA, 0, 255)); 
}

void controlMotorB(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) { digitalWrite(pinBIN1, HIGH); digitalWrite(pinBIN2, LOW); } 
  else { digitalWrite(pinBIN1, LOW); digitalWrite(pinBIN2, HIGH); }
  ledcWrite(pinPWMB, constrain(velocidad * factorCompensacionB, 0, 255)); 
}

void frenar() {
  digitalWrite(pinAIN1, HIGH); digitalWrite(pinAIN2, HIGH);
  digitalWrite(pinBIN1, HIGH); digitalWrite(pinBIN2, HIGH);
  ledcWrite(pinPWMA, 0); ledcWrite(pinPWMB, 0);
}

// ==========================================
// --- I2C (LA ÚNICA FORMA DE MOVER EL ROBOT AHORA) ---
// ==========================================
void receiveEvent(int howMany) {
  if (howMany >= 3) {
    uint8_t reg = Wire.read();
    uint8_t val = Wire.read();
    uint8_t chk = Wire.read();

    if (chk == (uint8_t)(reg + val)) {
      reg_estado = 1;
      if (reg == 2) { // ORDEN DE DIRECCIÓN
        digitalWrite(pinSTBY, HIGH); 
        switch (val) {
          case 0: frenar(); break; // QUIETO
          case 1: controlMotorA(180, true); controlMotorB(180, false); break; // ADELANTE
          case 2: controlMotorA(180, false); controlMotorB(180, true); break; // ATRÁS
          case 3: controlMotorA(150, false); controlMotorB(150, false); break; // IZQUIERDA
          case 4: controlMotorA(150, true); controlMotorB(150, true); break; // DERECHA
        }
      }
    } else { reg_estado = 0; }
  }
  while(Wire.available()) Wire.read(); 
}

void requestEvent() {
  uint8_t checksum = reg_estado + reg_rpm_izq + reg_rpm_der;
  uint8_t respuesta[4] = {reg_estado, reg_rpm_izq, reg_rpm_der, checksum};
  Wire.write(respuesta, 4);
}

void setup() {
  Serial.begin(115200);
  pinMode(pinSTBY, OUTPUT);
  pinMode(pinAIN1, OUTPUT); pinMode(pinAIN2, OUTPUT);
  pinMode(pinBIN1, OUTPUT); pinMode(pinBIN2, OUTPUT);
  ledcAttach(pinPWMA, freq, resolution); ledcAttach(pinPWMB, freq, resolution);
  digitalWrite(pinSTBY, HIGH); frenar(); 

  pinMode(encoderM1_A, INPUT_PULLUP); pinMode(encoderM1_B, INPUT_PULLUP);
  pinMode(encoderM2_A, INPUT_PULLUP); pinMode(encoderM2_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderM1_A), ISR_EncoderM1, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderM2_A), ISR_EncoderM2, RISING);

  Wire.setPins(SDA_PIN, SCL_PIN);
  delay(100);
  Wire.begin((uint8_t)ESP32_I2C_ADDR);
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);

  Serial.println("ESP32-S3 LISTA. (Modo Esclavo I2C Puro)");
}

void loop() {
  if (millis() - tiempoAnterior >= 100) {
    tiempoAnterior = millis();
    noInterrupts();
    long lecturaActualM1 = contadorM1, lecturaActualM2 = contadorM2;
    interrupts();
    long deltaM1 = lecturaActualM1 - prevM1, deltaM2 = lecturaActualM2 - prevM2;
    prevM1 = lecturaActualM1; prevM2 = lecturaActualM2;

    sumaRPM_M1 += abs(((float)deltaM1 / PPR_IZQ) * 600.0);
    sumaRPM_M2 += abs(((float)deltaM2 / PPR_DER) * 600.0);
    contadorMuestras++;

    if (contadorMuestras >= 5) { 
      reg_rpm_izq = (uint8_t)(sumaRPM_M1 / 5.0);
      reg_rpm_der = (uint8_t)(sumaRPM_M2 / 5.0);
      sumaRPM_M1 = 0; sumaRPM_M2 = 0; contadorMuestras = 0;
    }
  }
}