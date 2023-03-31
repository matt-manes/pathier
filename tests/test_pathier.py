from typing import Any

import pytest

from pathier.pathier import Pathier

root = Pathier(__file__).parent
dummy_obj = {"str": "yeet", "int": 44, "list": [1, 2, 3, 4, 5]}


def assert_dummy(obj: Any):
    assert obj["str"] == "yeet"
    assert obj["int"] == 44
    assert obj["list"] == [1, 2, 3, 4, 5]


def test__pathier__is_this_thing_on():
    path = Pathier("dummy.json")


def test__pathier__json_loads():
    path = root / "dummy.json"
    obj = path.json_loads()
    assert_dummy(obj)


def test__pathier__toml_loads():
    path = root / "dummy.toml"
    obj = path.toml_loads()
    assert_dummy(obj)


def test__pathier__loads():
    for file in ["dummy.json", "dummy.toml"]:
        path = root / file
        obj = path.loads()
        assert_dummy(obj)


def test__pathier__json_dumps():
    path = root / "dummy" / "dummy.json"
    path.json_dumps(dummy_obj, indent=2)
    obj = path.loads()
    assert_dummy(obj)


def test__pathier__toml_dumps():
    path = root / "dummy" / "dummy.toml"
    path.toml_dumps(dummy_obj)
    obj = path.loads()
    assert_dummy(obj)


def test__pathier__dumps():
    base = root / "dummy" / "dummier"
    for file in ["dummy.json", "dummy.toml"]:
        path = base / file
        path.dumps(dummy_obj, indent=2)
        obj = path.loads()
        assert_dummy(obj)


def test__pathier__copy():
    path = root / "dummy"
    new_path = path.copy(path / "dummy2")
    obj = (new_path / "dummy.toml").loads()
    assert_dummy(obj)
    obj["str"] = "not yeet"
    (new_path / "dummy.toml").dumps(obj)
    new_path.copy(path / "dummy.toml")
    obj = (path / "dummy.toml").loads()
    # Will fail if overwrite protection didn't work
    assert_dummy(obj)


def test__pathier__delete():
    path = root / "dummy"
    path.delete()
    assert not path.exists()


def test__pathier__moveup():
    assert root.moveup("pathier").stem == "pathier"


def test__pathier__sub():
    assert (root - 1).stem == "pathier"


def test__pathier__touch():
    path = root / "nested" / "touch" / "test" / "folder" / "yeet.txt"
    assert not path.exists()
    path.touch()
    assert path.exists
    path.moveup("nested").delete()
