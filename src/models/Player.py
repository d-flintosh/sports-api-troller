from abc import abstractmethod, ABC


class Player(ABC):
    @abstractmethod
    def has_stats(self) -> bool:
        pass

    @abstractmethod
    def convert_to_tweet(self) -> str:
        pass

    @abstractmethod
    def get_college(self) -> str:
        pass
