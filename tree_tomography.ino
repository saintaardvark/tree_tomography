// Basic demo for accelerometer readings from Adafruit MPU6050

// ESP32 Guide: https://RandomNerdTutorials.com/esp32-mpu-6050-accelerometer-gyroscope-arduino/
// ESP8266 Guide: https://RandomNerdTutorials.com/esp8266-nodemcu-mpu-6050-accelerometer-gyroscope-arduino/
// Arduino Guide: https://RandomNerdTutorials.com/arduino-mpu-6050-accelerometer-gyroscope/

#include <Adafruit_MPU6050.h>
#include <Adafruit_Sensor.h>
#include <Wire.h>

/* Despite the name, Debugging is set in constants.h */
#include "constants.h"
#include "debug.h"
#include "mpu6060_setup.h"
/* TODO: these names overlap; pick something better */
#include "lcd_screen.h"
#include "display.h"

Adafruit_MPU6050 mpu;
U8G2_ST7565_ERC12864_ALT_F_4W_SW_SPI u8g2(U8G2_R0, SCK, MOSI, CS_PIN, RS_PIN, RSE_PIN);

float touch;
volatile int64_t start_time = 0;
volatile int64_t impact_time = 0;
volatile int64_t elapsed_time = 0;
volatile int state = STATE_WAITING;

void setup(void) {
  Serial.begin(115200);
  while (!Serial)
    delay(10); // will pause Zero, Leonardo, etc until serial console opens

  Serial.println("Initializing screen...");
  u8g2_prepare();
  u8g2.print("Tree Tomography!");


  /* TODO: Break this out into a separate function */
  Serial.println("Adafruit MPU6050 test!");
  Wire.begin(I2C_SDA, I2C_SCL);

  // Try to initialize!
  if (!mpu.begin()) {
    Serial.println("Failed to find MPU6050 chip");
    u8g2.clearBuffer();
    u8g2.setCursor(0, 20);
    u8g2.print("No MPU6050 found!");
    u8g2.sendBuffer();

    while (1) {
      delay(10);
    }
  }
  Serial.println("MPU6050 Found!");
  mpuSetup(&mpu);
  Serial.println("");

  /* Set up hammer pin */
  pinMode(HAMMER_PIN, INPUT);

  u8g2.setCursor(0, 20);
  u8g2.print("Press touchpad");
  u8g2.setCursor(0, 30);
  u8g2.print("to start...");
  u8g2.sendBuffer();
  Serial.println();

  delay(1000);
  touchAttachInterrupt(T0, TouchISR, TOUCH_THRESHOLD);
  /* TODO: Not sure if RISING or HIGH is better here. I'm assuming
     that the change is what I'm after. */
  attachInterrupt(HAMMER_PIN, HammerISR, RISING);
  attachInterrupt(MPU_PIN, mpuISR, FALLING);
}

void TouchISR() {
  if (state = STATE_ARMED) {
    /* Don't go through this if we've already set state to ARMED */
    return;
  }
  state = STATE_ARMED;
  start_time = 0;
}

void HammerISR() {
  if (state = STATE_TIMER_STARTED) {
    /* Don't go through this if we've already started the timer */
    return;
  }
  start_time = esp_timer_get_time();
  state = STATE_TIMER_STARTED;
}

void mpuISR() {
  /* if (state != STATE_TIMER_STARTED) { */
  /*   /\* Don't go through this if the timer hasn't started *\/ */
  /*   return; */
  /* } */
  impact_time = esp_timer_get_time();
  state = STATE_TIMER_ENDED;
}


void loop() {
  /* Get new sensor events with the readings */
  sensors_event_t a, g, temp;

  float last_5_x[5];
  float last_5_y[5];
  float last_5_z[5];
  mpu.getEvent(&a, &g, &temp);
  int buttonState = 0;
  Serial.println(start_time);
  maybe_debug(&a, state, buttonState, start_time, impact_time, elapsed_time);
  displayArmedOrNot(state, buttonState);
  delay(SLEEPYTIME);
}
