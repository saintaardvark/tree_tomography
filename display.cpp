// (setq-default indent-tabs-mode nil)

#include "lcd_screen.h"
#include "constants.h"

void displayTimer(float elapsed_time, float percentage_diff, float avg, float new_val) {
        u8g2.clearBuffer();
        u8g2.setCursor(0, 0);
        u8g2.print("Break: ");
        // char s[16];
        // sprintf(s, "Time: %f", elapsed_time);
        // u8g2.drawStr(0, 15, s);
        u8g2.print(elapsed_time);
        u8g2.setCursor(0, 20);
        // TODO: Function to wrap text.  21 chars appears to be limit.
        u8g2.print("Press touchpad to");
        u8g2.setCursor(0, 30);
        u8g2.print("restart...");
        u8g2.sendBuffer();
        Serial.print("Break in the continuum: %diff: ");
        Serial.print(percentage_diff);
        Serial.print(" Avg: ");
        Serial.print(avg);
        Serial.print(" New val: ");
        Serial.print(new_val);
        Serial.print(" time: ");
        Serial.println(elapsed_time);
}

void displayArmedOrNot(int state, int buttonState) {
        if (state == STATE_WAITING) {
                return;
        }
        u8g2.clearBuffer();
        u8g2.setCursor(0, 0);
        if (state == STATE_ARMED) {
                u8g2.print("Armed...");
        } else {
                u8g2.print("Press button to time");
        }
        u8g2.setCursor(0, 20);
        u8g2.print("State: ");
        u8g2.print(state);
        u8g2.sendBuffer();
}
