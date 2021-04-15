import subprocess
from os.path import join, dirname, abspath

import daemon
import websocket

from gpio.lights import on_message, on_error, on_close


def start_ws():
    process = subprocess.Popen(['python', join(abspath(dirname(__file__)), 'button.py')])
    print("Started button watch")
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8181/core",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.run_forever()


def run():
    with daemon.DaemonContext():
        start_ws()


if __name__ == "__main__":
    run()
