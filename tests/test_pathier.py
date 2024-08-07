import os
import sys
import time
from datetime import datetime
from typing import Any

import pytest

from pathier.pathier import Pathier

root = Pathier(__file__).parent
dummy_obj = {"str": "yeet", "int": 44, "list": [1, 2, 3, 4, 5], "path": root}


def assert_dummy(obj: Any):
    assert obj["str"] == "yeet"
    assert obj["int"] == 44
    assert obj["list"] == [1, 2, 3, 4, 5]
    assert str(obj["path"]).endswith(
        f"{root.parent.stem}/{root.stem}"
    )  # "pathier/tests"


def test__pathier__is_this_thing_on():
    path = Pathier("dummy.json")


def test__str():
    path = Pathier("a/windows/test/path", convert_backslashes=False)
    assert str(path) == "a\\windows\\test\\path"
    path = Pathier("a/windows/test/path")
    assert str(path) == "a/windows/test/path"


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


def test__pickle_dumps():
    for name in ["dummy.pickle", "dummy.pkl"]:
        path = root / "dummy" / name
        path.pickle_dumps(dummy_obj)
        assert path.exists()
        path.delete()
        assert not path.exists()
        path.dumps(dummy_obj)
        assert path.exists()


def test__pickle_loads():
    for name in ["dummy.pickle", "dummy.pkl"]:
        path = root / "dummy" / name
        obj = path.pickle_loads()
        assert obj == dummy_obj


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
    assert Pathier("a/b/c/a/d/e").moveup("a") == Pathier("a/b/c/a")


def test__pathier__sub():
    assert (root - 1).stem == "pathier"


def test__pathier__touch():
    path = root / "nested" / "touch" / "test" / "folder" / "yeet.txt"
    assert not path.exists()
    path.touch()
    assert path.exists
    path.moveup("nested").delete()


def test__size():
    assert (root / "test_pathier.py").size > 0
    assert root.size > 0


def test__format_size():
    assert Pathier.format_bytes(1234) == "1.23 kb"


def test__formatted_size():
    path = Pathier(__file__)
    assert path.formatted_size == path.format_bytes(path.size)


def test__age():
    if root.age:
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


def test__move_under__duplicate_parts():
    path = Pathier("a/b/c/a/d/e")
    assert path.move_under("a") == Pathier("a/b/c/a/d")


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
    assert ret_val
    assert ret_val.exists()
    ret_val.delete()
    ret_val = path.backup(True)
    assert ret_val
    assert ret_val.exists()
    ret_val.delete()


def test__execute():
    test_path = root / "test_pathier.py"
    # Don't want to execute pytest infinitely
    # Also counts as testing `replace` I guess
    test_path.replace_strings([("test__execute", "execute")], 1)
    root.execute("pytest -s")
    test_path.replace_strings([("execute()", "test__execute()")], 1)


def test__append():
    appender = root / "appender.txt"
    appender.append("1")
    assert appender.read_text().splitlines() == ["1"]
    appender.append("2")
    assert appender.read_text().splitlines() == ["1", "2"]
    appender.append("3", False)
    appender.append("4")
    assert appender.read_text().splitlines() == ["1", "2", "34"]
    appender.delete()


def test__split():
    file = root / "join_split.txt"
    data = [str(n) for n in range(10)]
    file.join(data)
    assert file.split() == data
    file.delete()


def test__read_tracking():
    file = root / "tracker.txt"
    file.write_text("tracking\n")
    time.sleep(2)
    assert not file.last_read_time
    file.read_text()
    assert file.last_read_time
    time.sleep(0.1)
    assert datetime.now() > file.last_read_time
    assert not file.modified_since_last_read
    last_read_time = file.last_read_time
    file.write_text("tracking\n")
    time.sleep(2)
    assert file.modified_since_last_read
    assert file.last_read_time == last_read_time
    if file.modified_since_last_read:
        file.read_text()
    assert file.last_read_time != last_read_time
    assert not file.modified_since_last_read
    file.delete()
