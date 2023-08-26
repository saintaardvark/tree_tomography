def process_data(d, PIEZO_PIN=0b10, MPU_PIN=0b01):
    """
    Process data & print nicer report

    Example data:
    ('I', [2, 42949, 3, 961372, 1, 1389, 3, 7278])
    """
    i = 0
    msg = ""
    for i in range(4):
        pins = d[i * 2]
        piezo_state = "ON" if (pins & PIEZO_PIN) > 0 else "OFF"
        mpu_state = "ON" if (pins & MPU_PIN) > 0 else "OFF"
        time = d[i * 2 + 1] * 10  # nanoseconds
        time /= 10e3  # microseconds
        print(
            "Piezo: {:<5} MPU: {:<5} Time: {:<5} microseconds".format(
                piezo_state, mpu_state, time
            )
        )

    print()
