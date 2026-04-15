import pytest
from pydantic import ValidationError

from lib.schemas.player_state import PlayerState


def test_uuid_is_only_required_field():
    p = PlayerState(uuid="abc-123")
    assert p.uuid == "abc-123"
    assert p.x is None
    assert p.y is None
    assert p.direction is None
    assert p.moving is None
    assert p.anim_tick is None
    assert p.vx is None
    assert p.vy is None


def test_uuid_required():
    with pytest.raises(ValidationError):
        PlayerState()


def test_full_payload_roundtrip():
    p = PlayerState(uuid="abc-123", x=1.0, y=2.0, direction="right", moving=True, anim_tick=3, vx=1.0, vy=0.0)
    assert p.x == 1.0
    assert p.y == 2.0
    assert p.direction == "right"
    assert p.moving is True
    assert p.anim_tick == 3
    assert p.vx == 1.0
    assert p.vy == 0.0


def test_partial_serialize_excludes_none():
    p = PlayerState(uuid="abc-123", x=10.0, direction="up")
    data = p.model_dump(exclude_none=True)
    assert data == {"uuid": "abc-123", "x": 10.0, "direction": "up"}
    assert "y" not in data
    assert "moving" not in data
    assert "vx" not in data


def test_partial_deserialize_from_dict():
    payload = {"uuid": "abc-123", "x": 5.0, "moving": False}
    p = PlayerState(**payload)
    assert p.uuid == "abc-123"
    assert p.x == 5.0
    assert p.moving is False
    assert p.y is None
    assert p.vx is None


def test_uuid_only_serializes_to_single_key():
    p = PlayerState(uuid="abc-123")
    data = p.model_dump(exclude_none=True)
    assert data == {"uuid": "abc-123"}
