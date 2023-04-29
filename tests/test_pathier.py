import os
import sys
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


def test__size():
    assert (root / "test_pathier.py").size() > 0
    assert root.size() > 0


def test__format_size():
    assert Pathier.format_size(1234) == "1.23 kb"


def test__age():
    assert root.age > 0
    assert (root / "yeet").age is None


def test__dob():
    assert root.dob is not None
    assert (root / "yeet").dob is None


def test__mod_date():
    assert root.mod_date is not None
    assert (root / "yeet").mod_date is None


def test__mod_delta():
    assert root.mod_delta is not None
    assert (root / "yeet").mod_date is None


def test__is_larger():
    assert (root / "dummy.json").is_larger(root / "blank.txt")


def test__is_older():
    assert (root / "dummy.json").is_older(root / "blank.txt")


def test__modified_more_recently():
    assert (root / "test_pathier.py").modified_more_recently(root / "blank.txt")


def test__move_under():
    path = Pathier("a/b/c/d/e")
    assert path.move_under("b") == Pathier("a/b/c")
    assert path.move_under("d") == path
    assert path.move_under("a") == Pathier("a/b")


def test__separate():
    path = Pathier("a/b/c/d/e")
    assert path.separate("c") == Pathier("d/e")
    assert path.separate("c", True) == Pathier("c/d/e")


def test__mkcwd():
    og_cwd = Pathier.cwd()
    os.chdir(root)
    cwd = Pathier.cwd()
    path = (root - 1) / "src" / "pathier"
    path.mkcwd()
    assert Pathier.cwd() != cwd
    assert Pathier.cwd() == path
    os.chdir(og_cwd)


def test__add_to_PATH():
    path = str(root)

    assert path not in sys.path
    assert not root.in_PATH

    root.add_to_PATH()
    assert sys.path[0] == path
    assert root.in_PATH

    root.add_to_PATH(1)
    assert sys.path[1] != path

    root.remove_from_PATH()
    assert path not in sys.path
    assert not root.in_PATH

    root.add_to_PATH(1)
    assert sys.path[1] == path
    assert root.in_PATH

    root.append_to_PATH()
    assert sys.path[-1] != path

    root.remove_from_PATH()
    root.append_to_PATH()
    assert sys.path[-1] == path
    assert root.in_PATH
    root.remove_from_PATH()


def test__backup():
    path = root / "dummy.dummy"
    ret_val = path.backup()
    assert ret_val is None
    path = root / "dummy.toml"
    ret_val = path.backup()
    assert ret_val.exists()
    ret_val.delete()
    ret_val = path.backup(True)
    assert ret_val.exists()
    ret_val.delete()


def test__execute():
    test_path = root / "test_pathier.py"
    # Don't want to execute pytest infinitely
    test_path.write_text(test_path.read_text().replace("execute", "execute"))
    root.execute("pytest -s")
    test_path.write_text(
        test_path.read_text().replace("test__execute()", "test__execute()")
    )
