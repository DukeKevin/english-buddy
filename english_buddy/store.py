from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .models import BuddyResponse


class ResultStatus(str, Enum):
    PENDING = "pending"
    DONE = "done"
    ERROR = "error"


@dataclass
class ResultEntry:
    scene: str
    status: ResultStatus = ResultStatus.PENDING
    result: Optional[BuddyResponse] = None
    error: Optional[str] = None


class ResultStore:
    def __init__(self):
        self._data: dict[str, ResultEntry] = {}
        self._msg_ids: dict[str, str] = {}

    def create(self, result_id: str, scene: str, msg_id: str = ""):
        self._data[result_id] = ResultEntry(scene=scene)
        if msg_id:
            self._msg_ids[msg_id] = result_id

    def get_by_msg_id(self, msg_id: str) -> Optional[str]:
        return self._msg_ids.get(msg_id)

    def set_result(self, result_id: str, result: BuddyResponse):
        entry = self._data[result_id]
        entry.status = ResultStatus.DONE
        entry.result = result

    def set_error(self, result_id: str, error: str):
        entry = self._data[result_id]
        entry.status = ResultStatus.ERROR
        entry.error = error

    def get(self, result_id: str) -> Optional[ResultEntry]:
        return self._data.get(result_id)


store = ResultStore()
