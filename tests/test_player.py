from lib.player import Player
from lib.schemas.player_state import PlayerState


def _make_player(**kwargs) -> Player:
    defaults = dict(x=10.0, y=20.0, direction="down", moving=False, anim_tick=0, vx=0.0, vy=0.0)
    return Player(**{**defaults, **kwargs})


# --- to_state ---

def test_to_state_returns_player_state():
    p = _make_player()
    assert isinstance(p.to_state(), PlayerState)


def test_to_state_all_fields_populated():
    p = _make_player(x=5.0, y=15.0, direction="right", moving=True, anim_tick=3, vx=1.0, vy=0.5)
    s = p.to_state()
    assert s.uuid == p.uuid
    assert s.x == 5.0
    assert s.y == 15.0
    assert s.direction == "right"
    assert s.moving is True
    assert s.anim_tick == 3
    assert s.vx == 1.0
    assert s.vy == 0.5


def test_to_state_no_none_fields():
    s = _make_player().to_state()
    assert all(v is not None for v in s.model_dump().values())


# --- from_state ---

def test_from_state_restores_all_fields():
    original = _make_player(x=7.0, direction="left", moving=True, vx=-1.0)
    restored = Player.from_state(original.to_state())
    assert restored.uuid == original.uuid
    assert restored.x == 7.0
    assert restored.direction == "left"
    assert restored.moving is True
    assert restored.vx == -1.0


def test_from_state_preserves_uuid():
    p = _make_player()
    assert Player.from_state(p.to_state()).uuid == p.uuid


# --- apply_state ---

def test_apply_state_updates_present_fields():
    p = _make_player(x=0.0, y=0.0)
    p.apply_state(PlayerState(uuid=p.uuid, x=99.0, direction="up"))
    assert p.x == 99.0
    assert p.direction == "up"


def test_apply_state_ignores_none_fields():
    p = _make_player(y=42.0, moving=True)
    p.apply_state(PlayerState(uuid=p.uuid, x=1.0))  # y and moving not included
    assert p.y == 42.0
    assert p.moving is True


def test_apply_state_uuid_only_changes_nothing():
    p = _make_player(x=5.0, direction="right")
    p.apply_state(PlayerState(uuid=p.uuid))
    assert p.x == 5.0
    assert p.direction == "right"


# --- roundtrip ---

def test_roundtrip_to_and_from_state():
    original = _make_player(x=3.0, y=7.0, direction="up", moving=True, anim_tick=2, vx=0.5, vy=-0.5)
    restored = Player.from_state(original.to_state())
    assert restored.x == original.x
    assert restored.y == original.y
    assert restored.direction == original.direction
    assert restored.moving == original.moving
    assert restored.anim_tick == original.anim_tick
    assert restored.vx == original.vx
    assert restored.vy == original.vy
