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

/* Looks like maybe I should avoid GPIO 0, since it's labelled CLK1? */
#define HAMMER_PIN 2

/* Waiting for touch to be triggered */
#define STATE_WAITING 0
/* Touch triggered; timer armed; waiting for accel shock to actually start timer */
#define STATE_ARMED 1
/* Hammerpin interrupt happened; start timer. */
#define STATE_TIMER_STARTED 2
/*
   Note: I don't know that I need this...I think I can just go
   back to STATE_WAITING.
*/
#define STATE_TIMER_ENDED 3
/* After that: go to STATE_WAITING */

#define THRESHOLD_PERCENTAGE 5

#define SLEEPYTIME 0
