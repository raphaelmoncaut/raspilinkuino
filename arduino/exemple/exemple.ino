#include <Arduino_JSON.h>

void setup() {
  Serial.begin(1000000); // 1 Mbaud because we can
}

void loop() {
  JSONVar obj; // Create a JSON object to store data in
  obj["prop1"] = 42;
  obj["prop2"] = "Look at my String";
  Serial.print(obj); // Send the JSON object through the serial port
  Serial.print("\x03"); // Send ETX to indicate that the transmission in finished
  delay(5000);
}
