#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLEUtils.h>
#include <BLE2902.h>

// ==========================================
// --- 1. DEFINICIÓN DE PINES DE MOTORES ---
// ==========================================
const int pinSTBY = 10;
const int pinPWMA = 11;
const int pinAIN1 = 12;
const int pinAIN2 = 13;
const int pinPWMB = 14;
const int pinBIN1 = 15;
const int pinBIN2 = 16;

// ==========================================
// --- 2. PINES DE ENCODERS (Conexión 3.3V) ---
// ==========================================
const int encoderM1_A = 5; 
const int encoderM1_B = 4; 
const int encoderM2_A = 17; 
const int encoderM2_B = 7; 

// ==========================================
// --- 3. CONFIGURACIÓN PWM Y CALIBRACIÓN ---
// ==========================================
const int freq = 20000;    
const int resolution = 8;  

float factorCompensacionA = 1.00; 
float factorCompensacionB = 0.90; 

// ==========================================
// --- 4. CONSTANTES DE ODOMETRÍA (PPR) ---
// ==========================================
const float PPR_IZQ = 1981.0; 
const float PPR_DER = 1981.0; 

volatile long contadorM1 = 0; 
volatile long contadorM2 = 0;
long prevM1 = 0;
long prevM2 = 0;
unsigned long tiempoAnterior = 0;

// Filtro Antirruido Hardware (Debounce)
volatile unsigned long ultimo_pulso_M1 = 0;
volatile unsigned long ultimo_pulso_M2 = 0;

// Filtro de Promedio Software
int contadorMuestras = 0;
float sumaRPM_M1 = 0;
float sumaRPM_M2 = 0;

// ==========================================
// --- 5. VARIABLES BLUETOOTH BLE ---
// ==========================================
BLEServer *pServer = NULL;
BLECharacteristic * pTxCharacteristic; 
bool deviceConnected = false;
bool oldDeviceConnected = false;

#define SERVICE_UUID           "6E400001-B5A3-F393-E0A9-E50E24DCCA9E" 
#define CHARACTERISTIC_UUID_RX "6E400002-B5A3-F393-E0A9-E50E24DCCA9E" 
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E" 

// ==========================================
// --- RUTINAS DE INTERRUPCIÓN (CON FILTRO) ---
// ==========================================
void IRAM_ATTR ISR_EncoderM1() {
  unsigned long tiempo_actual = micros();
  if (tiempo_actual - ultimo_pulso_M1 > 300) { 
    if (digitalRead(encoderM1_B) == HIGH) contadorM1++;
    else contadorM1--;
    ultimo_pulso_M1 = tiempo_actual;
  }
}

void IRAM_ATTR ISR_EncoderM2() {
  unsigned long tiempo_actual = micros();
  if (tiempo_actual - ultimo_pulso_M2 > 400) { 
    if (digitalRead(encoderM2_B) == HIGH) contadorM2++;
    else contadorM2--;
    ultimo_pulso_M2 = tiempo_actual;
  }
}

// ==========================================
// --- FUNCIONES DE CONTROL DE MOTORES ---
// ==========================================
void controlMotorA(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) {
    digitalWrite(pinAIN1, HIGH); digitalWrite(pinAIN2, LOW);
  } else {
    digitalWrite(pinAIN1, LOW); digitalWrite(pinAIN2, HIGH);
  }
  int velocidadAjustada = constrain(velocidad * factorCompensacionA, 0, 255);
  ledcWrite(pinPWMA, velocidadAjustada); 
}

void controlMotorB(int velocidad, bool sentidoHorario) {
  if (sentidoHorario) {
    digitalWrite(pinBIN1, HIGH); digitalWrite(pinBIN2, LOW);
  } else {
    digitalWrite(pinBIN1, LOW); digitalWrite(pinBIN2, HIGH);
  }
  int velocidadAjustada = constrain(velocidad * factorCompensacionB, 0, 255);
  ledcWrite(pinPWMB, velocidadAjustada); 
}

void frenar() {
  digitalWrite(pinAIN1, HIGH); digitalWrite(pinAIN2, HIGH);
  digitalWrite(pinBIN1, HIGH); digitalWrite(pinBIN2, HIGH);
  ledcWrite(pinPWMA, 0); ledcWrite(pinPWMB, 0);
}

// ==========================================
// --- CALLBACKS BLUETOOTH ---
// ==========================================
class MyServerCallbacks: public BLEServerCallbacks {
    void onConnect(BLEServer* pServer) { deviceConnected = true; };
    void onDisconnect(BLEServer* pServer) { deviceConnected = false; }
};

class MyCallbacks: public BLECharacteristicCallbacks {
    void onWrite(BLECharacteristic *pCharacteristic) {
      String rxValue = pCharacteristic->getValue(); 

      if (rxValue.length() > 0) {
        if (rxValue[0] == '!' && rxValue[1] == 'B') {
          char boton = rxValue[2];   
          char estado = rxValue[3];  

          if (estado == '1') { 
            switch (boton) {
              case '5': controlMotorA(180, true); controlMotorB(180, false); break; 
              case '6': controlMotorA(180, false); controlMotorB(180, true); break; 
              case '7': controlMotorA(150, false); controlMotorB(150, false); break; 
              case '8': controlMotorA(150, true); controlMotorB(150, true); break;
            }
          } 
          else if (estado == '0') { 
            frenar();
          }
        }
      }
    }
};

// ==========================================
// --- SETUP PRINCIPAL ---
// ==========================================
void setup() {
  Serial.begin(115200);

  pinMode(pinSTBY, OUTPUT);
  pinMode(pinAIN1, OUTPUT); pinMode(pinAIN2, OUTPUT);
  pinMode(pinBIN1, OUTPUT); pinMode(pinBIN2, OUTPUT);
  ledcAttach(pinPWMA, freq, resolution);
  ledcAttach(pinPWMB, freq, resolution);
  digitalWrite(pinSTBY, HIGH); 
  frenar(); 

  pinMode(encoderM1_A, INPUT_PULLUP); pinMode(encoderM1_B, INPUT_PULLUP);
  pinMode(encoderM2_A, INPUT_PULLUP); pinMode(encoderM2_B, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(encoderM1_A), ISR_EncoderM1, RISING);
  attachInterrupt(digitalPinToInterrupt(encoderM2_A), ISR_EncoderM2, RISING);

  BLEDevice::init("ROBOT_MECATRONICA"); 
  pServer = BLEDevice::createServer();
  pServer->setCallbacks(new MyServerCallbacks());
  BLEService *pService = pServer->createService(SERVICE_UUID);

  BLECharacteristic * pRxCharacteristic = pService->createCharacteristic(
      CHARACTERISTIC_UUID_RX, BLECharacteristic::PROPERTY_WRITE
  );
  pRxCharacteristic->setCallbacks(new MyCallbacks());

  pTxCharacteristic = pService->createCharacteristic(
      CHARACTERISTIC_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY
  );
  pTxCharacteristic->addDescriptor(new BLE2902()); 

  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("======================================");
  Serial.println(" SISTEMA V1.3 (PINES I2C LIBERADOS) ");
  Serial.println("======================================");
}

// ==========================================
// --- LOOP PRINCIPAL ---
// ==========================================
void loop() {
  if (!deviceConnected && oldDeviceConnected) {
      delay(500); pServer->startAdvertising(); 
      oldDeviceConnected = deviceConnected; frenar(); 
  }
  if (deviceConnected && !oldDeviceConnected) {
      oldDeviceConnected = deviceConnected;
  }

  // --- CÁLCULO DE VELOCIDAD CADA 100ms ---
  if (millis() - tiempoAnterior >= 100) {
    tiempoAnterior = millis();
    
    noInterrupts();
    long lecturaActualM1 = contadorM1;
    long lecturaActualM2 = contadorM2;
    interrupts();

    long deltaM1 = lecturaActualM1 - prevM1;
    long deltaM2 = lecturaActualM2 - prevM2;

    prevM1 = lecturaActualM1;
    prevM2 = lecturaActualM2;

    float rpmInst_M1 = abs(((float)deltaM1 / PPR_IZQ) * 600.0);
    float rpmInst_M2 = abs(((float)deltaM2 / PPR_DER) * 600.0);

    sumaRPM_M1 += rpmInst_M1;
    sumaRPM_M2 += rpmInst_M2;
    contadorMuestras++;

    if (contadorMuestras >= 10) {
      float promedio_M1 = sumaRPM_M1 / 10.0;
      float promedio_M2 = sumaRPM_M2 / 10.0;

      if (promedio_M1 > 0 || promedio_M2 > 0) {
        Serial.print("Velocidad Promedio IZQ: ");
        Serial.print(promedio_M1, 1); 
        Serial.print(" RPM \t|\t Velocidad Promedio DER: ");
        Serial.print(promedio_M2, 1);
        Serial.println(" RPM");
      }

      sumaRPM_M1 = 0;
      sumaRPM_M2 = 0;
      contadorMuestras = 0;
    }
  }
}