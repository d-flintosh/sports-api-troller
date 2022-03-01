import dataclasses
import json
from abc import abstractmethod, ABC
from datetime import datetime

from src.gcp.gcs import Gcs


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
    def get_player_id(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_league_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_college(self) -> str:
        raise NotImplementedError

    def get_gcs_path_by_date(self, date: datetime, college: str) -> str:
        date_string = date.strftime("%Y-%m-%d")
        return f'{self.get_league_name()}/{college}/by_date/{date_string}/{self.get_player_id()}.json'

    def save(self, gcs: Gcs, date: datetime, college: str) -> None:
        gcs.write(
            url=self.get_gcs_path_by_date(date=date, college=college),
            contents=dataclasses.asdict(self)
        )

    def convert_dataclass_to_json(self):
        return json.dumps(self, cls=EnhancedJSONEncoder)


class EnhancedJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)

