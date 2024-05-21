import os
import platform
import requests

class SystemInfo:
    """First Attack to get the system information of the target machine."""

    @classmethod
    def get(cls) -> dict:
        """Returns the system information.

        Returns:
            dict: The system information.
        """
        return {
                'os_name': platform.system(),
                'os_version': platform.version(),
                'os_arch': platform.architecture(),
                'processor': platform.processor(),
                'user': os.getlogin(),
                'public_ip': SystemInfo._get_public_ip(),
                'local_ip': SystemInfo._get_local_ip(),
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
