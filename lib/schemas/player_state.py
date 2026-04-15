from typing import Optional

from pydantic import BaseModel


class PlayerState(BaseModel):
    uuid: str
    x: Optional[float] = None
    y: Optional[float] = None
    direction: Optional[str] = None
    moving: Optional[bool] = None
    anim_tick: Optional[int] = None
    vx: Optional[float] = None
    vy: Optional[float] = None
