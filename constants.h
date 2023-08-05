#define I2C_SDA 23
#define I2C_SCL 19

/*
  0: no debugging
  1: some debugging
  2; more debugging
*/
#define DEBUG 1

#define TOUCH_PIN 4
#define TOUCH_THRESHOLD 40

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

#define THRESHOLD_PERCENTAGE 5

#define SLEEPYTIME 2000
