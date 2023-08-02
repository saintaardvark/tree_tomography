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
// Original arduino pinout:
// U8G2_ST7565_ERC12864_ALT_F_4W_SW_SPI u8g2(U8G2_R0,/*clock=*/ 8,/* data=*/ 9,/* cs=*/ 5,/* dc=*/ 7,/* reset=*/ 6);u
U8G2_ST7565_ERC12864_ALT_F_4W_SW_SPI u8g2(U8G2_R0, SCK, MOSI, CS_PIN, RS_PIN, RSE_PIN);
