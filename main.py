from config import _screen_capture, _clipboard_attack

from threading import Thread
from rich import print

def main():
    clipboard_thread = Thread(target=_clipboard_attack.execute)
    screen_capture_thread = Thread(target=_screen_capture.execute)

    clipboard_thread.start()
    screen_capture_thread.start()

    print(f"[bold green]System started!")
    

    print("[bold yellow]Press Enter to stop the attacks.")
    input()
    _clipboard_attack.stop()
    _screen_capture.stop()
          
if __name__ == '__main__':
    main()