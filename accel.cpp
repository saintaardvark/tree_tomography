#include <Adafruit_Sensor.h>

#include "constants.h"

void maybe_debug_accel(sensors_event_t *a, int state) {
  if (DEBUG > 0) {
    Serial.print("Acceleration_X:");
    Serial.print(a->acceleration.x);
    Serial.print(",Acceleration_Y:");
    Serial.print(a->acceleration.y);
    Serial.print(",Acceleration_Z:");
    Serial.print(a->acceleration.z);
    Serial.print(",State:");
    Serial.println(state);
  }
}
