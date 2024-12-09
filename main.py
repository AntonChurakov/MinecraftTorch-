import neopixel

from machine import Pin, deepsleep, Timer, freq  # Import only required functions/classes

import time

import random

import network



# --- Constants and Settings ---

WS_PIN = 16  # GPIO pin for WS2812

LED_NUM = 8  # Number of LEDs in the ring

MAX_BRIGHTNESS = 255  # Maximum brightness for LEDs (0-255)

INACTIVITY_PERIOD_MS = 2 * 60 * 60 * 1000  # Inactivity period before deep sleep (2 hours)



# --- Hardware Initialization ---

neo_ring = neopixel.NeoPixel(Pin(WS_PIN), LED_NUM)



# Disable Wi-Fi to save energy

wifi = network.WLAN(network.STA_IF)

wifi.active(False)



# Lower ESP32 clock frequency to save power

freq(80_000_000)  # 80 MHz



# Timer for entering deep sleep

sleep_timer = Timer(-1)





# --- Functions ---

def turn_off():

    """

    Turns off the LEDs and puts the ESP32 into deep sleep.

    """

    for i in range(LED_NUM):

        neo_ring[i] = (0, 0, 0)

    neo_ring.write()

    print("Device is entering deep sleep...")

    deepsleep()





def get_fire_color():

    """

    Generates a random color to simulate fire.



    Returns:

        tuple: A color tuple in the format (R, G, B).

    """

    red = random.randint(MAX_BRIGHTNESS // 255, MAX_BRIGHTNESS)

    green = random.randint(1, MAX_BRIGHTNESS // 50)

    blue = random.randint(0, MAX_BRIGHTNESS // 50)

    return red, green, blue





def flicker():

    """

    Updates the LED colors to simulate fire flickering.

    """

    for i in range(LED_NUM):

        if random.random() <0.8:  # 100% chance to update this LED

            neo_ring[i] = get_fire_color()

        else:

            neo_ring[i] = (0, 0, 0)  # Turn off the LED

    neo_ring.write()

    time.sleep_ms(random.randint(100, 800))  # Delay between updates





# --- Main Code ---

# Set the timer for INACTIVITY_PERIOD_MS

sleep_timer.init(period=INACTIVITY_PERIOD_MS, mode=Timer.ONE_SHOT, callback=lambda t: turn_off())



while True:

    flicker()
