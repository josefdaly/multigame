import uuid

from lib.schemas.player_state import PlayerState

class Player:
    def __init__(self, x, y, direction, moving, anim_tick, vx, vy):
        self.state = PlayerState(
            uuid=str(uuid.uuid4()),
            x=x,
            y=y,
            direction=direction,
            moving=moving,
            anim_tick=anim_tick,
            vx=vx,
            vy=vy,
        )

    @property
    def uuid(self):
        return self.state.uuid
    
    @property
    def x(self):
        return self.state.x
    
    @x.setter
    def x(self, value):
        self.state.x = value

    @property
    def y(self):
        return self.state.y

    @y.setter
    def y(self, value):
        self.state.y = value

    @property
    def direction(self):
        return self.state.direction

    @direction.setter
    def direction(self, value):
        self.state.direction = value

    @property
    def moving(self):
        return self.state.moving

    @moving.setter
    def moving(self, value):
        self.state.moving = value

    @property
    def anim_tick(self):
        return self.state.anim_tick

    @anim_tick.setter
    def anim_tick(self, value):
        self.state.anim_tick = value

    @property
    def vx(self):
        return self.state.vx

    @vx.setter
    def vx(self, value):
        self.state.vx = value

    @property
    def vy(self):
        return self.state.vy

    @vy.setter
    def vy(self, value):
        self.state.vy = value
