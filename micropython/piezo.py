from machine import ADC, Pin

PIEZO_TEST_PIN = 26

def test_piezo():
    """
    Simple test routine for seeing signals from the piezo.
    """
    max = 0
    pot = ADC(Pin(PIEZO_TEST_PIN))
    while True:
        reading = pot.read_u16()
        if reading > max:
            max = reading
            print(f"New max: {max}")


