#include <U8g2lib.h>
#ifdef U8X8_HAVE_HW_SPI
#include <SPI.h>
#endif
#ifdef U8X8_HAVE_HW_I2C
#include <Wire.h>
#endif

#define CS_PIN 32               /* Goes to pin 1, labelled CS */
#define SS 32                   /* for clarity */
// st7565 1 pin (CS)

#define RSE_PIN 33              /* Goes to pin 2, labelled RSE */
// st7565 2 pin (RSE)

#define RS_PIN 25               /* Goes to pin 3, labelled RS */
// st7565 3 Pin (RS)

#define SCL_PIN 26              /* Goes to pin 4, labelled SCL */
#define SCK 26                  /* for clarity */
// st7565 4 pin (SCL)

#define SI_PIN 27               /* Goes to pin 5, labelled SI*/
#define MOSI 27                 /* for clarity */
// st7565 5 pin (SI)

// https://www.youtube.com/watch?v=wXDFW6NsDK4

extern U8G2_ST7565_ERC12864_ALT_F_4W_SW_SPI u8g2;

void u8g2_prepare();

