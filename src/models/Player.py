from abc import abstractmethod, ABC


class Player(ABC):
    @abstractmethod
    def is_decent_day(self) -> bool:
        pass

    @abstractmethod
    def convert_to_tweet(self) -> str:
        pass

    @abstractmethod
    def get_college(self) -> str:
        pass
