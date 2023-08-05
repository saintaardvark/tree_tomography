#include <U8g2lib.h>
#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

void u8g2_prepare() {
  u8g2.begin();
  u8g2.enableUTF8Print();
  u8g2.setContrast(70);
  u8g2.clearBuffer();
  u8g2.setCursor(0, 0);
  u8g2.setFont(u8g2_font_6x10_tf);
  u8g2.setFontRefHeightExtendedText();
  u8g2.setDrawColor(1);
  u8g2.setFontPosTop();
  u8g2.setFontDirection(0);
}
