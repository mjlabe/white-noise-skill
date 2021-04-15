import daemon
from gpio.lights import start_ws


def run():
    with daemon.DaemonContext():
        start_ws()


if __name__ == "__main__":
    run()
