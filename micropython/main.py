# Source: https://forums.raspberrypi.com/viewtopic.php?t=306064&sid=f40cf17605a796b93c59b94721dd322b#p1842706
#
# This is a little bit different from main.py:
#
# - this post comes from the thread & the original author, whereas
#   main.py comes from J. Beale's github repo.
#
# - But also, this code was corrected by the original author (set vs
#   mov), and those changes don't seem to have been captured in the
#   github repo.
#
# - finally, the simulated signals are in here too.

from machine import Pin, mem32
from rp2 import asm_pio, StateMachine, PIO
from time import ticks_ms, ticks_diff
from utime import sleep
import array

from pulsedelay import pulsedelay
from constants.pins import p1, p2, p3, p4, switch, led_1, led_2
from constants.headers import DEFAULT_HEADERS
from simulation import in_sig_sim, start_sig_sim
from trigger import trigger
from counter import counter
from report import process_data
from display import display

data = array.array("I", [0] * 8)
start = ticks_ms()

START_SIG_SIM = False
SLEEPYTIME = 0.5
DEBUG = False


def debug(msg):
    """
    Simple debugger
    """
    if DEBUG:
        print(f"[DEBUG] {msg}")


def maybe_start_simulator(start_sim=START_SIG_SIM):
    """
    Maybe start signal simulator
    """
    if start_sim is True:
        print("Starting simulator!")
        start_sig_sim()


# Source: https://github.com/dommodnet/Pi-Pico-Pinout-Ascii-Art
#                         +-----+
#          +--------------| USB |--------------+
#          |        GP25  +-----+              |
#          |1       [LED]                   40 |
#          | [ ]GP0/U0Rx               VBUS[ ] |
#          | [ ]GP1/U0Tx               VSYS[ ] |
#          | [ ]GND                     GND[ ] |
#          | [ ]GP2                      x3[ ] |
#          | [ ]GP3                     3V3[ ] |
#          | [ ]GP4                    AREF[ ] |
#          | [ ]GP5                 A2/GP28[ ] |
#          | [ ]GND                     GND[ ] |
#          | [ ]GP6        +---+    A1/GP27[ ] |
#          | [ ]GP7        |   |    A0/GP26[ ] |
#          | [ ]GP8        |   |        RUN[ ] |
#          | [ ]GP9        +---+       GP22[ ] |
#          | [ ]GND                     GND[ ] |
#          | [ ]GP10                   GP21[ ] |
#          | [ ]GP11         \/        GP20[ ] |
#          | [ ]GP12        ()()       GP19[ ] |
#          | [ ]GP13        ()()       GP18[ ] |
#          | [ ]GND          ()         GND[ ] |
#          | [ ]GP14                   GP17[ ] |
#          | [ ]GP15        DEBUG      GP16[ ] |
#          |20           [ ] [ ] [ ]         21|
#          |            MISO SCK RST           |
#          | Pi-Pico                           |
#          +-----------------------------------+


def maybe_print_headers(headers):
    """
    Print headers if it looks like there's a request for them.

    TODO:
    """
    m = input()
    print(headers)


def main():
    """
    Main entry point
    """
    maybe_start_simulator()

    pulsein_12 = pulsedelay(
        pin1=p1, pin2=p2, stateMachine=0
    )  # Time of flight between blue & green
    pulsein_13 = pulsedelay(
        pin1=p1, pin2=p3, stateMachine=1
    )  # Time of flight between blue & red
    debug(pulsein_12.sm)
    debug(pulsein_13.sm)

    which_sm = 123  # Start by watching 1->2 *and* 1->3
    # which_sm = 12  # Start by watching 1->2 only
    led_1.on()
    led_2.off()

    # DEBUG = True
    if DEBUG:
        debug("Debug mode on!")
        formatter = "pretty"
        import sys

        print(
            "Which pins do you want to watch?  (12, 13, 123, or NODEBUG to turn off debug mode)"
        )
        which_sm = sys.stdin.readline().strip("\n")
        if which_sm == "NODEBUG":
            debug("No debug mode it is!")
            which_sm = 12
            formatter = "csv"
        else:
            which_sm = int(which_sm)
        debug(f"{which_sm} it is!")
    else:
        formatter = "csv"

    debug("Everything looks good!")
    debug("Now entering state of cat-like readiness 😼...")

    i = 0
    # TODO: Don't hardcode header

    # Wait to see if we have a request for headers
    maybe_print_headers(headers=DEFAULT_HEADERS)
    while True:
        if which_sm == 12:
            pulsein_12.activate()
            msg = {"1->2": pulsein_12.get()}
            display(msg=msg, formatter=formatter)
        elif which_sm == 13:
            pulsein_13.activate()
            msg = {"1->3": pulsein_13.get()}
            display(msg=msg, formatter=formatter)
        else:
            pulsein_12.activate()
            pulsein_13.activate()
            msg = {"1->2": pulsein_12.get(), "1->3": pulsein_13.get()}
            display(msg=msg, formatter=formatter)

        sleep(SLEEPYTIME)

        if switch.value() == 1:
            print("Switching!")
            if which_sm == 12:
                which_sm = 13
                led_1.off()
                led_2.on()
            elif which_sm == 13:
                which_sm = 123
                led_1.on()
                led_2.on()
            elif which_sm == 123:
                which_sm = 12
                led_1.on()
                led_2.off()

            print(f"Now looking at {which_sm}")


if __name__ == "__main__":
    main()
