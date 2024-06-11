import requests
from rich import print
from retry import retry
from datetime import datetime
import json

class Proxy:
    
    def __init__(self, base_uri: str, version: str) -> None:
        self.base_uri = base_uri
        self.version = version
        self.headers = {'Content-Type': 'application/json'}
        self._generate_urls()
        
        
    
    def _generate_urls(self):
        self.api_url = f"{self.base_uri}/api/{self.version}"
        self.machine_url = f"{self.api_url}/machine/"
        self.result_url = f"{self.api_url}/attack-result/"
    
    def _generate_result_data(self,
                              result_type: str,
                              success: bool,
                              executed_date:datetime,
                              machine: str,
                              attack: str,
                              data: dict):
        
        return self._dump({
            "result_type": result_type,
            "success": success,
            "executed_date": executed_date.isoformat(),
            "machine": machine,
            "attack": attack,
            "data":  data
        })
    
    def _dump(self, data: dict):
        return json.dumps(data)
      
    @retry(exceptions=(ConnectionError), tries=1, delay=2)
    def register_machine(self, machine_data: dict):
        json = self._dump(machine_data)
        
        response = requests.post(self.machine_url, 
                                 data=json,
                                 headers=self.headers)
        
        if response.status_code not in [200, 201]:
            print(f"[bold red]Error while registering the machine!")
            print(response.json())
    
    
    @retry(exceptions=(ConnectionError), tries=1, delay=2)       
    def send_result(self, result_data: dict):
        response = requests.post(self.result_url, 
                                 data=result_data, 
                                 headers=self.headers)
        
        if response.status_code not in [200, 201]:
            print(f"[bold red]Error while sending result!")
            print(result_data)
            print(response.json())
        