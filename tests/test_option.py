import pytest

from option import Nothing, Option, Some, UnwrapError

# Some Test


def test_some_is_none():
    assert not Some(1).is_none()
    assert not Some("A").is_none()


def test_some_is_nothing():
    assert not Some(1).is_nothing()
    assert not Some("A").is_nothing()


def test_some_is_some():
    assert Some(1).is_some()
    assert Some("A").is_some()


def test_some_is_some_and():
    assert Some(1).is_some_and(lambda x: x == 1)
    assert not Some(2).is_some_and(lambda x: x == 1)
    assert Some("A").is_some_and(lambda x: "A" in x)
    assert not Some("B").is_some_and(lambda x: "A" in x)


def test_some_value():
    assert Some(1).value == 1
    assert Some("A").value == "A"


def test_some_map():
    assert Some(1).map(lambda x: x + 1).value == 2
    assert Some(1).map(lambda x: str(x)).value == "1"
    assert Some("A").map(lambda x: x + "B").value == "AB"
    assert Some("A").map(lambda x: len(x)).value == 1


def test_some_map_or():
    assert Some(1).map_or(0, lambda x: x + 1) == 2
    assert Some(1).map_or("A", lambda x: str(x)) == "1"
    assert Some("A").map_or("B", lambda x: x + "B") == "AB"
    assert Some("A").map_or(0, lambda x: len(x)) == 1


def test_some_map_else():
    assert Some(1).map_or_else(lambda: 0, lambda x: x + 1) == 2
    assert Some(1).map_or_else(lambda: "A", lambda x: str(x)) == "1"
    assert Some("A").map_or_else(lambda: "B", lambda x: x + "B") == "AB"
    assert Some("A").map_or_else(lambda: 0, lambda x: len(x)) == 1


def test_some_or_else():
    assert Some(1).or_else(lambda: Some(2)).value == 1
    assert Some("A").or_else(lambda: Some("B")).value == "A"


def test_some_unwrap():
    assert Some(1).unwrap() == 1
    assert Some("A").unwrap() == "A"


def test_some_unwrap_or():
    assert Some(1).unwrap_or(2) == 1
    assert Some("A").unwrap_or("B") == "A"


def test_some_unwrap_or_else():
    assert Some(1).unwrap_or_else(lambda: 2) == 1
    assert Some("A").unwrap_or_else(lambda: "B") == "A"


# Nothing Test
def test_nothing_is_none():
    assert Nothing().is_none()


def test_nothing_is_nothing():
    assert Nothing().is_nothing()


def test_nothing_is_some():
    assert not Nothing().is_some()


def test_nothing_is_some_and():
    assert not Nothing().is_some_and(lambda x: x == 1)
    assert not Nothing().is_some_and(lambda x: "A" in x)


def test_nothing_value():
    assert Nothing().value == None


def test_nothing_map():
    assert Nothing().map(lambda x: x + 1).value == None
    assert Nothing().map(lambda x: str(x)).value == None
    assert Nothing().map(lambda x: x + "B").value == None
    assert Nothing().map(lambda x: len(x)).value == None


def test_nothing_map_or():
    assert Nothing().map_or(0, lambda x: x + 1) == 0
    assert Nothing().map_or("A", lambda x: str(x)) == "A"
    assert Nothing().map_or("B", lambda x: x + "B") == "B"
    assert Nothing().map_or(0, lambda x: len(x)) == 0


def test_nothing_map_else():
    assert Nothing().map_or_else(lambda: 0, lambda x: x + 1) == 0
    assert Nothing().map_or_else(lambda: "A", lambda x: str(x)) == "A"
    assert Nothing().map_or_else(lambda: "B", lambda x: x + "B") == "B"
    assert Nothing().map_or_else(lambda: 0, lambda x: len(x)) == 0


def test_nothing_or_else():
    assert Nothing().or_else(lambda: Some(2)).value == 2
    assert Nothing().or_else(lambda: Some("B")).value == "B"


def test_nothing_unwrap():
    with pytest.raises(UnwrapError) as _:
        Nothing().unwrap()


def test_nothing_unwrap_or():
    assert Nothing().unwrap_or(2) == 2
    assert Nothing().unwrap_or("B") == "B"


def test_nothing_unwrap_or_else():
    assert Nothing().unwrap_or_else(lambda: 2) == 2
    assert Nothing().unwrap_or_else(lambda: "B") == "B"


def test_some_match():
    a = Some(1)
    match a:
        case Some(x):
            assert x == 1
        case Nothing():
            assert False


def test_nothing_match():
    a = Nothing()
    match a:
        case Some(x):
            assert x == 1
        case Nothing():
            assert True
