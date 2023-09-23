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

from my_mpu import MyMpu
from pulsedelay import pulsedelay
from simulation import in_sig_sim, start_sig_sim
from trigger import trigger
from counter import counter
from report import process_data


data = array.array("I", [0] * 8)
start = ticks_ms()

START_SIG_SIM = False
SLEEPYTIME = 0.5

if START_SIG_SIM is True:
    print("Starting simulator!")
    start_sig_sim()


p1 = Pin(14, Pin.IN)  # Blue LED
p2 = Pin(15, Pin.IN)  # Green LED

pulsein = pulsedelay(p1, p2)

print("Everything looks good!")
print("Now entering state of cat-like readiness 😼...")

i = 0
while True:
    print(pulsein.get(), " microseconds")
    sleep(SLEEPYTIME)
