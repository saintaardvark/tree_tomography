#include <Adafruit_Sensor.h>

#include "constants.h"


void maybe_debug(sensors_event_t *a, int state, int buttonState, int64_t start_time, int64_t impact_time, int64_t elapsed_time) {
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
    Serial.print(",StartTime:");
    Serial.print(start_time);
    Serial.print(",ImpactTime:");
    Serial.print(impact_time);
    Serial.print(",ElapsedTime:");
    Serial.print(elapsed_time);
    Serial.print(",Now:");
    Serial.println(esp_timer_get_time());
  }
}
