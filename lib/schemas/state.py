from pydantic import BaseModel

from .player_state import PlayerState


class GameState(BaseModel):
    players: list[PlayerState]
