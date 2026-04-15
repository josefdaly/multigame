import math
import pyxel

from .player import Player
from lib.schemas.state import GameState

# Sprite sheet layout in image bank 0 — 3 rows of 3 frames each (8x8 px per frame):
#   v=0:  side-walk  (shared for left & right; left is drawn with w=-8 to flip)
#   v=8:  down-walk  (front-facing, toward camera)
#   v=16: up-walk    (back-facing, away from camera)
# Column layout per row: frame0 @ u=0, frame1 @ u=8, frame2 @ u=16
#
# Colors: 7=skin(white), 8=red shirt, 5=dark-blue pants, 4=dark hair, 0=transparent

SPRITE_SHEET = {
    #          v_offset, [frame0, frame1, frame2]
    "side": (0, [
        # stride A — arms wide, legs spread to x=1 and x=4
        ["07700000", "07700000", "78887000", "08880000", "05550000", "05005000", "00000000", "00000000"],
        # neutral  — arms tucked, legs together
        ["07700000", "07700000", "07870000", "08880000", "05550000", "00550000", "00550000", "00000000"],
        # stride B — arms wide, legs spread to x=2 and x=4
        ["07700000", "07700000", "78887000", "08880000", "05550000", "00505000", "00000000", "00000000"],
    ]),
    "down": (8, [
        # stride A — front view, legs step wide (x=0 and x=4)
        ["07770000", "07770000", "78887000", "08880000", "05550000", "50005000", "00000000", "00000000"],
        # neutral  — legs together
        ["07770000", "07770000", "78887000", "08880000", "05550000", "00550000", "00550000", "00000000"],
        # stride B — legs at x=1 and x=3 (closer step)
        ["07770000", "07770000", "78887000", "08880000", "05550000", "05050000", "00000000", "00000000"],
    ]),
    "up": (16, [
        # stride A — back view (dark hair), legs step wide (x=0 and x=4)
        ["04400000", "04400000", "78887000", "08880000", "05550000", "50005000", "00000000", "00000000"],
        # neutral  — legs together
        ["04400000", "04400000", "78887000", "08880000", "05550000", "00550000", "00550000", "00000000"],
        # stride B — legs at x=1 and x=3
        ["04400000", "04400000", "78887000", "08880000", "05550000", "05050000", "00000000", "00000000"],
    ]),
}

ANIM_CYCLE = [0, 1, 2, 1]  # one full walk cycle through frame indices
ANIM_SPEED = 2              # game frames per animation step
SPEED = 1.0                 # max pixels per frame on a cardinal axis
ACCEL = 0.1                # speed gained per frame (reaches SPEED in ~7 frames)


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Roguelike")

        for direction, (v_offset, frames) in SPRITE_SHEET.items():
            for i, frame_data in enumerate(frames):
                pyxel.images[0].set(i * 8, v_offset, frame_data)

        self.player = Player(
            x=76.0,
            y=56.0,
            direction="down",   # "right" | "left" | "up" | "down"
            moving=False,
            anim_tick=0,
            vx=0.0,
            vy=0.0,
        )
        self.state = GameState(players=[self.player.state])

        pyxel.run(self.update, self.draw)

    @property
    def players(self):
        return self.state.players

    def _handle_input(self):
        dx = 0
        dy = 0

        if pyxel.btn(pyxel.KEY_LEFT):
            dx -= 1
        if pyxel.btn(pyxel.KEY_RIGHT):
            dx += 1
        if pyxel.btn(pyxel.KEY_UP):
            dy -= 1
        if pyxel.btn(pyxel.KEY_DOWN):
            dy += 1

        if dx != 0 or dy != 0:
            self.player.moving = True
            length = math.sqrt(dx * dx + dy * dy)
            target_vx = (dx / length) * SPEED
            target_vy = (dy / length) * SPEED

            # Accelerate velocity vector toward target; caps step at ACCEL per frame
            diff_x = target_vx - self.player.vx
            diff_y = target_vy - self.player.vy
            diff_len = math.sqrt(diff_x * diff_x + diff_y * diff_y)
            if diff_len <= ACCEL:
                self.player.vx, self.player.vy = target_vx, target_vy
            else:
                self.player.vx += (diff_x / diff_len) * ACCEL
                self.player.vy += (diff_y / diff_len) * ACCEL

            # Horizontal takes priority for facing direction
            if dx != 0:
                self.player.direction = "right" if dx > 0 else "left"
            else:
                self.player.direction = "down" if dy > 0 else "up"
        else:
            self.player.vx = 0.0
            self.player.vy = 0.0

        self.player.x = max(0.0, min(152.0, self.player.x + self.player.vx))
        self.player.y = max(0.0, min(112.0, self.player.y + self.player.vy))

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        self.player.moving = False

        self._handle_input()

        if self.player.moving:
            self.player.anim_tick += 1
        else:
            self.player.anim_tick = 0

    def _render_player(self, player):
        if player.moving:
            cycle_pos = (player.anim_tick // ANIM_SPEED) % len(ANIM_CYCLE)
            frame_idx = ANIM_CYCLE[cycle_pos]
        else:
            frame_idx = 1  # neutral standing frame

        u = frame_idx * 8

        if player.direction in ("right", "left"):
            v = SPRITE_SHEET["side"][0]
            w = 8 if player.direction == "right" else -8
        elif player.direction == "down":
            v = SPRITE_SHEET["down"][0]
            w = 8
        else:  # up
            v = SPRITE_SHEET["up"][0]
            w = 8

        pyxel.blt(int(player.x), int(player.y), 0, u, v, w, 8, 0)

    def draw(self):
        pyxel.cls(0)
        for player in self.players:
            self._render_player(player)
            
