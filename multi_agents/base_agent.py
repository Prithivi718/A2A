from abc import ABC, abstractmethod
import ast
import json


class BaseAgent(ABC):

    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def description(self)-> str:
        pass

    @abstractmethod
    def instruction(self)-> str:
        pass

    @abstractmethod
    def model(self) -> str:
        pass


    @abstractmethod
    def process_task(self, *args, **kwargs)-> str:
        pass