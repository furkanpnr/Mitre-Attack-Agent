from abc import ABC, abstractmethod
from rich import print

class IAttack(ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_description(self):
        pass

    @abstractmethod
    def get_result(self):
        pass

    @abstractmethod
    def stop(self):
        pass


class Attack(IAttack):

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.result = {}
        self._running = False

    def execute(self):
        raise NotImplementedError("execute method should be implemented.")

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_result(self):
        return self.result
    
    def stop(self):
        self.running = False
        print(f"[bold red]{self.name} Attack stopped.")

    @property
    def running(self):
        return self._running
    
    @running.setter
    def running(self, value):
        if not isinstance(value, bool):
            raise ValueError("running should be a boolean value.")
        self._running = value