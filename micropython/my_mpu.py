from mpu6050 import MPU6050


class MyMpu(MPU6050):
    LATCH_INTERRUPT = True

    def start(self):
        """
        My own version of the Adafruit/eluke.nl code
        """
        # mpu->setMotionDetectionThreshold(1);
        self.__writeByte(0x1F, 0x01)
        # mpu->setMotionDetectionDuration(1);
        self.__writeByte(0x20, 0x01)
        # mpu->setInterruptPinLatch(true);	// Keep it latched.  Will turn off when reinitialized.
        # Want to set 5th (latch until clear).
        # Could *also* set 4th bit (clear by reading 0x3a / d58), but will leave that for now.
        if self.LATCH_INTERRUPT is True:
            # This also sets interrupt polarity to active high, by writing 0 to the 7th bit.
            self.__writeByte(0x37, 0x20)
        else:
            # but since we're not doing it above, we do it explicitly here.
            self.__writeByte(0x37, 0)
        # mpu->setInterruptPinPolarity(true);
        # This is config'd by setting 0x37, 7th bit to 0.  Done above.
        # mpu->setMotionInterrupt(true);
        # IntEnable is 0x38.  Need to set 6th bit.
        self.__writeByte(0x38, 0x40)
        #
        # And finally, clear interrupts to get ready:
        self.reset_interrupt()

    def reset_interrupt(self):
        """
        This lets the next interrupt happen if interrupts are latched.
        """
        self.__readByte(0x3A)
