import logging
import threading
import pynput

logging.basicConfig(level=logging.INFO)


class AutoClicker:
    logger = logging.getLogger()
    DELAY = 0.05

    def __init__(self) -> None:
        self.mouse = pynput.mouse.Controller()
        self.exit_flag = threading.Event()
        self.exit_flag.set()

    def run(self) -> None:
        with (
            pynput.keyboard.Listener(on_press=self.onPress) as self.listener,
            pynput.mouse.Listener(on_move=self.onMove) as self.mouse_listener,
        ):
            self.start()
            self.listener.join()
            self.mouse_listener.join()

    def onMove(self, *args):
        if not self.exit_flag.is_set():
            self.stop()

    def onPress(self, key) -> None:
        if key == pynput.keyboard.KeyCode(char="a"):
            self.logger.info("key pressed")
            self.logger.info(self.exit_flag.is_set())
            if self.exit_flag.is_set():
                self.start()
            else:
                self.stop()

        if key == pynput.keyboard.KeyCode(char="b"):
            self.listener.stop()
            self.mouse_listener.stop()

    def start(self) -> None:
        self.logger.info("starting clicker")
        self.exit_flag.clear()
        threading.Thread(target=self.clicker).start()

    def stop(self) -> None:
        self.logger.info("stopping clicker")
        self.exit_flag.set()

    def clicker(self) -> None:
        self.logger.info("thread started")
        while not self.exit_flag.wait(timeout=self.DELAY):
            self.mouse.click(pynput.mouse.Button.left)


if __name__ == "__main__":
    clicker = AutoClicker()

    clicker.run()
