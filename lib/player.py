import uuid as uuid_lib

from lib.schemas.player_state import PlayerState


class Player:
    def __init__(self, x: float, y: float, direction: str, moving: bool, anim_tick: int, vx: float, vy: float):
        self.uuid: str = str(uuid_lib.uuid4())
        self.x: float = x
        self.y: float = y
        self.direction: str = direction
        self.moving: bool = moving
        self.anim_tick: int = anim_tick
        self.vx: float = vx
        self.vy: float = vy
        
        self.dirty: bool = False  # Whether this player's state has changed since the last update   

    def to_state(self) -> PlayerState:
        return PlayerState(
            uuid=self.uuid,
            x=self.x,
            y=self.y,
            direction=self.direction,
            moving=self.moving,
            anim_tick=self.anim_tick,
            vx=self.vx,
            vy=self.vy,
        )

    @classmethod
    def from_state(cls, state: PlayerState) -> "Player":
        player = cls(
            x=state.x,
            y=state.y,
            direction=state.direction,
            moving=state.moving,
            anim_tick=state.anim_tick,
            vx=state.vx,
            vy=state.vy,
        )
        player.uuid = state.uuid
        return player

    def apply_state(self, state: PlayerState) -> None:
        if state.x is not None:
            self.x = state.x
        if state.y is not None:
            self.y = state.y
        if state.direction is not None:
            self.direction = state.direction
        if state.moving is not None:
            self.moving = state.moving
        if state.anim_tick is not None:
            self.anim_tick = state.anim_tick
        if state.vx is not None:
            self.vx = state.vx
        if state.vy is not None:
            self.vy = state.vy
