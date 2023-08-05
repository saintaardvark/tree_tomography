// Basic demo for accelerometer readings from Adafruit MPU6050

// ESP32 Guide: https://RandomNerdTutorials.com/esp32-mpu-6050-accelerometer-gyroscope-arduino/
// ESP8266 Guide: https://RandomNerdTutorials.com/esp8266-nodemcu-mpu-6050-accelerometer-gyroscope-arduino/
// Arduino Guide: https://RandomNerdTutorials.com/arduino-mpu-6050-accelerometer-gyroscope/

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

#include "mpu6060_setup.h"
#include "lcd_screen.h"
#include "accel.h"
#include "constants.h"
#include "display.h"

Adafruit_MPU6050 mpu;
U8G2_ST7565_ERC12864_ALT_F_4W_SW_SPI u8g2(U8G2_R0, SCK, MOSI, CS_PIN, RS_PIN, RSE_PIN);

float touch;

int64_t last_time = 0;

/* Waiting for touch to be triggered */
#define STATE_WAITING 0
/* Touch triggered; waiting for accel shock */
#define STATE_TIMER_START 1
/* Accel shock happened; end timer.
   Note: I don't know that I need this...I think I can just go
   back to STATE_WAITING.
*/
#define STATE_TIMER_ENDED 2
/* After that: go to STATE_WAITING */

int state = STATE_WAITING;

#define THRESHOLD_PERCENTAGE 5

#define SLEEPYTIME 2000

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Adafruit MPU6050 test!");
  Wire.begin(I2C_SDA, I2C_SCL);

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  mpuSetup(&mpu);
  Serial.println("");

  Serial.println("Initializing screen...");
  u8g2_prepare();
  u8g2.print("Tree Tomography!");
  u8g2.sendBuffer();
  Serial.println();

  delay(100);
  touchAttachInterrupt(T0, TouchISR, TOUCH_THRESHOLD);
}

void TouchISR() {
  last_time = esp_timer_get_time();
  state = STATE_TIMER_START;
}

int update_array(float my_array[], float new_val) {
  float avg = 0;
  int retval = 0;
  for (int i = 4; i >= 0; i--) {
    if (DEBUG > 1) {
      Serial.print("Value " );
      Serial.print(i);
      Serial.print(": ");
      Serial.println(my_array[i]);
    }
    avg += my_array[i];
  }
  avg /= 5;
  if (DEBUG > 1) {
    Serial.print("New value: ");
    Serial.print(new_val);
    Serial.print(", Avg: ");
    Serial.println(avg);
  }
  if (DEBUG > 0) {
    Serial.print("State: ");
    Serial.println(state);
  }
  /* If > 1% difference */
  float percentage_diff = (abs(new_val - avg) / avg) * 100;
  if ((percentage_diff > THRESHOLD_PERCENTAGE) && (state == STATE_TIMER_START)) {
    float elapsed_time = esp_timer_get_time() - last_time;
    last_time = esp_timer_get_time();
    state = STATE_WAITING;
    retval = 1;
    displayTimer(elapsed_time, percentage_diff, avg, new_val);
  }
  for (int i = 4; i >= 0; i--) {
    if (i == 0) {
      if (DEBUG > 1) {
        Serial.print("Setting new val: ");
        Serial.print(i);
        Serial.print(": ");
        Serial.println(new_val);
      }
      my_array[i] = new_val;
    } else {
      if (DEBUG > 1) {
        Serial.print("Moving values around: Element ");
        Serial.print(i);
        Serial.print(" is now ");
        Serial.println(my_array[i -1]);
      }
      my_array[i] = my_array[i - 1];
    }
  }
  return retval;
}

void loop() {
  /* Get new sensor events with the readings */
	sensors_event_t a, g, temp;

	float last_5_x[5];
	float last_5_y[5];
	float last_5_z[5];
  mpu.getEvent(&a, &g, &temp);
	maybe_debug_accel(&a);
  /* Print out the values.  No space means the Arduino IDE serial plotter will work with it. */
  /* if (update_array(last_5_x, a.acceleration.x) > 0) { */
  /*  Serial.println("Break: X"); */
  /* } */
  /* if (update_array(last_5_y, a.acceleration.y) > 0) { */
  /*  Serial.println("Break: Y"); */
  /* } */
  if (update_array(last_5_z, a.acceleration.z) > 0) {
    Serial.println("Break: Z");
  }
  delay(SLEEPYTIME);
}
