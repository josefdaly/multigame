from typing import Optional

from pydantic import BaseModel

from .player_state import PlayerState


class GameState(BaseModel):
    uuid: Optional[str]
    players: list[PlayerState]
