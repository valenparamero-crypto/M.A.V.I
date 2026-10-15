#include <Wire.h>

// Configuración de I2C
#define ESP32_I2C_ADDR 0x08  // Debe ser igual que DIRECCION_ESP32 en Python
#define SDA_PIN 8            // Pin SDA físico de tu ESP32
#define SCL_PIN 9            // Pin SCL físico de tu ESP32

// Memoria de la ESP32 (Mapa de Registros)
uint8_t reg_encendido = 0; // Registro 1: 0=Apagado, 1=Encendido
uint8_t reg_direccion = 0; // Registro 2: 0=Quieto, 1=Adelante, etc.
uint8_t reg_estado = 1;    // Registro 3: 1=Todo OK, 0=Error (Checksum inválido)

// --- FUNCIÓN 1: CUANDO PYTHON ENVÍA DATOS (bus.write_i2c_block_data) ---
void receiveEvent(int howMany) {
  // Python envía 3 bytes: [Registro, Valor, Checksum]
  if (howMany >= 3) {
    uint8_t reg = Wire.read();
    uint8_t val = Wire.read();
    uint8_t chk = Wire.read();

    Serial.print("-> Recibido: Reg="); Serial.print(reg);
    Serial.print(", Val="); Serial.print(val);
    Serial.print(", Chk="); Serial.println(chk);

    // Verificamos si el mensaje se dañó en el cable
    if (chk == (reg + val)) {
      Serial.println("   [EXITO] Checksum correcto. Ejecutando orden...");
      
      if (reg == 1) reg_encendido = val;
      else if (reg == 2) reg_direccion = val;
      
      reg_estado = 1; // Guardamos que la última orden fue exitosa
    } else {
      Serial.println("   [ERROR] Checksum INCORRECTO. Orden descartada.");
      reg_estado = 0; // Guardamos que hubo un error
    }
  } 
  
  // Limpiamos cualquier basura extra que quede en el cable
  while(Wire.available()) Wire.read(); 
}

// --- FUNCIÓN 2: CUANDO PYTHON PIDE DATOS (bus.read_i2c_block_data) ---
void requestEvent() {
  // Python espera 3 bytes de vuelta: [3 (Registro), Estado, Checksum]
  uint8_t checksum_respuesta = 3 + reg_estado;
  uint8_t respuesta[3] = {3, reg_estado, checksum_respuesta};
  
  // Enviamos la respuesta a la Raspberry Pi
  Wire.write(respuesta, 3);
  Serial.println("<- Raspberry Pi pidio estado. Respuesta enviada.");
}

void setup() {
  Serial.begin(115200);
  
  // Configuración de pines para ESP32
  Wire.setPins(SDA_PIN, SCL_PIN);
  
  // Iniciar el bus I2C como ESCLAVO en la dirección 0x08
  Wire.begin((uint8_t)ESP32_I2C_ADDR);
  
  // Enlazar las funciones a los eventos I2C
  Wire.onReceive(receiveEvent);
  Wire.onRequest(requestEvent);
  
  Serial.println("======================================");
  Serial.println(" ESP32-S3 LISTA Y ESPERANDO ORDENES");
  Serial.println(" Direccion I2C: 0x08");
  Serial.println("======================================");
}

void loop() {
  // El loop se queda libre. El I2C funciona por interrupciones en el fondo.
  // Aquí es donde en el futuro pondrás el código de mover los motores,
  // leer sensores, etc., basándote en las variables 'reg_encendido' y 'reg_direccion'.
  
  delay(100); 
}