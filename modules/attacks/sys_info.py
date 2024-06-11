import os, pwd
import platform
import requests
import uuid
from .attack import MitreAttack, istanbul_tz
from datetime import datetime

class SystemInfo:
    """First Attack to get the system information of the target machine."""

    @classmethod
    def get(cls) -> dict:
        """Returns the system information.

        Returns:
            dict: The system information.
        """
        return {
                'public_ip': cls._get_public_ip(),
                'local_ip': cls._get_local_ip(),
                'mac_addr': cls._get_mac_addr(),
                'os_name': platform.system(),
                'os_version': platform.version(),
                'os_arch': cls._get_os_arch(),
                'processor': platform.processor(),
                'user_name': cls._get_login(),
            }

    @classmethod
    def _get_local_ip(cls):
         try:
            local_ip = os.popen('hostname -I').read().split()[0]
            return local_ip
         except Exception as e:
             return None
         
    @classmethod
    def _get_public_ip(cls):
        try:
            res = requests.get(url='https://api.ipify.org', timeout=5)
            if res.status_code != 200:
                return None
            return res.text
        except Exception as e:
            return None
        
    @classmethod
    def _get_mac_addr(cls):
        mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        return ":".join([mac[e:e+2] for e in range(0, 12, 2)])
    
    @classmethod
    def _get_os_arch(cls):
        arch = platform.architecture()
        return f"{arch[0]}/{arch[1]}"
    
    @classmethod
    def _get_result(cls):
        
        try:
            data = cls.get()
            success = True
        except Exception:
            data = {}
            success = False
        
        result = {
            "result_type": "system_info",
            "success": success,
            "executed_date": datetime.now(istanbul_tz),
            "machine": cls._get_mac_addr(),
            "attack": MitreAttack.SYS_INFO.value,
            "data":  data
        }
        
        return result
    
    @classmethod
    def _get_login(csl):
        try:
            return os.getlogin()
        except OSError:
            return os.environ.get('USER') or pwd.getpwuid(os.getuid()).pw_name
        except Exception:
            pass