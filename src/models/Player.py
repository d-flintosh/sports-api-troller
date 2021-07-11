import dataclasses
import json
from abc import abstractmethod, ABC


class Player(ABC):
    @abstractmethod
    def has_stats(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def had_a_great_day(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def convert_to_tweet(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_college(self) -> str:
        raise NotImplementedError

    def convert_dataclass_to_json(self):
        return json.dumps(self, cls=EnhancedJSONEncoder)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

