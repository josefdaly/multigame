from lib.schemas.player_state import PlayerState
from lib.schemas.state import GameState


def test_empty_state():
    state = GameState(players=[])
    assert state.players == []


def test_state_with_partial_players():
    state = GameState(players=[
        PlayerState(uuid="p1"),
        PlayerState(uuid="p2", x=10.0, y=20.0),
    ])
    assert len(state.players) == 2
    assert state.players[0].uuid == "p1"
    assert state.players[0].x is None
    assert state.players[1].x == 10.0


def test_state_serialize_excludes_none():
    state = GameState(players=[PlayerState(uuid="p1", x=5.0)])
    data = state.model_dump(exclude_none=True)
    assert data == {"players": [{"uuid": "p1", "x": 5.0}]}


def test_state_deserialize_from_dict():
    payload = {
        "players": [
            {"uuid": "p1"},
            {"uuid": "p2", "direction": "left", "moving": True},
        ]
    }
    state = GameState(**payload)
    assert state.players[0].uuid == "p1"
    assert state.players[0].x is None
    assert state.players[1].direction == "left"
    assert state.players[1].moving is True


def test_state_roundtrip():
    original = GameState(players=[
        PlayerState(uuid="p1", x=1.0, y=2.0, direction="down", moving=False, anim_tick=0, vx=0.0, vy=0.0),
    ])
    data = original.model_dump()
    restored = GameState(**data)
    assert restored.players[0].uuid == "p1"
    assert restored.players[0].x == 1.0
    assert restored.players[0].direction == "down"
