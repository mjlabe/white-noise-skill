import time
from os.path import join, abspath, dirname
from subprocess import call

import RPi.GPIO as GPIO
import daemon
import websocket


def gpio_daemon():
    led_pin = 25
    gpio_pin = 23  # The GPIO pin the button is attached to
    press_threshold = 2  # If button is held this length of time, tells system to leave light on
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(led_pin, GPIO.OUT)
    led = GPIO.PWM(led_pin, 100)
    state = 0

    while True:
        time.sleep(0.2)
        if GPIO.input(gpio_pin) == False:  # Listen for the press, the loop until it steps
            print("Started press")
            pressed_time = time.time()
            while GPIO.input(gpio_pin) == False:
                time.sleep(0.2)
            pressed_time = time.time() - pressed_time
            print("Button pressed %d" % pressed_time)
            if pressed_time > press_threshold:
                if state == 0:
                    call(['python', join(abspath(dirname(__file__)), 'mbus.py'), 'localhost', 'noise.white.intent'])
                    led.start()
                    state = 1
                if state == 1:
                    call(['python', join(abspath(dirname(__file__)), 'mbus.py'), "localhost", "mycroft.stop"])
                    led.stop()
                    state = 0


def run():
    with daemon.DaemonContext():
        gpio_daemon()


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8181/core")
    ws.run_forever()
    run()
