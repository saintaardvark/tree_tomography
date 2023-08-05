#include <Adafruit_Sensor.h>

#include "constants.h"

void maybe_debug(sensors_event_t *a, int state, int buttonState, int64_t last_time) {
  if (DEBUG > 0) {
    Serial.print("Acceleration_X:");
    Serial.print(a->acceleration.x);
    Serial.print(",Acceleration_Y:");
    Serial.print(a->acceleration.y);
    Serial.print(",Acceleration_Z:");
    Serial.print(a->acceleration.z);
    Serial.print(",ButtonState:");
    Serial.print(buttonState);
    Serial.print(",State:");
    Serial.print(state);
    Serial.print(",LastTime:");
    Serial.print(last_time);
    Serial.print(",Now:");
    Serial.println(esp_timer_get_time());
  }
}
