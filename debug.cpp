#include <Adafruit_Sensor.h>

#include "constants.h"

void maybe_debug(sensors_event_t *a, int state, int buttonState) {
  if (DEBUG > 0) {
    Serial.print("Acceleration_X:");
    Serial.print(a->acceleration.x);
    Serial.print(",Acceleration_Y:");
    Serial.print(a->acceleration.y);
    Serial.print(",Acceleration_Z:");
    Serial.print(a->acceleration.z);
    int buttonState = digitalRead(HAMMER_PIN);
    
    Serial.print(",State:");
    Serial.println(state);
  }
}
