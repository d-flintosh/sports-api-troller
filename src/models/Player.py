from abc import abstractmethod, ABC


class Player(ABC):
    @abstractmethod
    def has_stats(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def convert_to_tweet(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_college(self) -> str:
        raise NotImplementedError
