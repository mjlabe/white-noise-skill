import subprocess
import websocket
from os.path import join, dirname, abspath

process = subprocess.Popen(['python', join(abspath(dirname(__file__)), "gpio.py")])


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8181/core")
    ws.run_forever()
