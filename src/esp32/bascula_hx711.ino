// Báscula con HX711 + celda de carga en ESP32-C3 Super Mini
// Librería: "HX711 Arduino Library" de Bogdan Necula (bogde)
//
// Conexiones:
//   HX711 VCC -> 3V3
//   HX711 GND -> GND
//   HX711 DT  -> GPIO4
//   HX711 SCK -> GPIO5
//
// Comandos por el Monitor Serie (115200 baudios):
//   t -> tara (poner a cero)
//   c -> calibrar con un peso conocido

#include <HX711.h>
#include <Preferences.h>

const int PIN_DT  = 4;
const int PIN_SCK = 5;

HX711 scale;
Preferences prefs;
float factor = 1.0;  // factor de calibración (se guarda en memoria)

void calibrar() {
  Serial.println("Quita todo de la bascula y espera...");
  delay(2000);
  scale.set_scale();   // factor = 1
  scale.tare(20);

  Serial.println("Pon el peso conocido y escribe su valor en gramos (ej: 500), luego Enviar.");
  while (Serial.available()) Serial.read();   // limpiar buffer
  while (!Serial.available()) delay(10);
  float pesoConocido = Serial.parseFloat();
  delay(100);
  while (Serial.available()) Serial.read();

  if (pesoConocido <= 0) {
    Serial.println("Valor invalido. Calibracion cancelada.");
    scale.set_scale(factor);
    return;
  }

  Serial.println("Midiendo...");
  delay(1000);
  float lectura = scale.get_value(20);        // lectura cruda menos la tara
  factor = lectura / pesoConocido;
  scale.set_scale(factor);

  prefs.putFloat("factor", factor);
  Serial.print("Listo. Factor de calibracion: ");
  Serial.println(factor, 4);
}

void setup() {
  Serial.begin(115200);
  delay(1500);

  prefs.begin("bascula", false);
  factor = prefs.getFloat("factor", 1.0);

  scale.begin(PIN_DT, PIN_SCK);
  scale.set_scale(factor);

  Serial.println("Esperando al HX711...");
  while (!scale.is_ready()) delay(100);
  scale.tare(20);

  Serial.println("Bascula lista. Comandos: t = tara, c = calibrar");
  if (factor == 1.0) Serial.println("Aun no calibrada: escribe 'c'.");
}

void loop() {
  if (Serial.available()) {
    char cmd = Serial.read();
    if (cmd == 't') {
      scale.tare(20);
      Serial.println("Tara hecha.");
    } else if (cmd == 'c') {
      calibrar();
    }
  }

  if (scale.is_ready()) {
    float gramos = scale.get_units(5);
    Serial.print("Peso: ");
    Serial.print(gramos, 1);
    Serial.println(" g");
  }
  delay(300);
}
