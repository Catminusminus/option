from typing import Any, Callable, Generic, NoReturn, TypeVar, Union

T = TypeVar("T", covariant=True)
U = TypeVar("U")


class Some(Generic[T]):
    _value: T
    __match_args__ = ("value",)
    __slots__ = ("_value",)

    def __init__(self, value: T) -> None:
        self._value = value

    def __repr__(self) -> str:
        return f"Some({repr(self._value)})"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Some) and self.value == other.value

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((True, self._value))

    def is_none(self) -> bool:
        return False

    def is_nothing(self) -> bool:
        return False

    def is_some(self) -> bool:
        return True

    def is_some_and(self, f: Callable[[T], bool]) -> bool:
        return f(self._value)

    @property
    def value(self) -> T:
        return self._value

    def map(self, f: Callable[[T], U]) -> "Some[U]":
        return Some(f(self._value))

    def map_or(self, _: U, f: Callable[[T], U]) -> U:
        return f(self._value)

    def map_or_else(self, _: Callable[[], U], f: Callable[[T], U]) -> U:
        return f(self._value)

    def or_else(self, _: Callable[[], "Some[T]"]) -> "Some[T]":
        return self

    def unwrap(self) -> T:
        return self._value

    def unwrap_or(self, _: object) -> T:
        return self._value

    def unwrap_or_else(self, _: Callable[[], T]) -> T:
        return self._value


class Nothing:
    def __init__(self) -> None:
        pass

    def __repr__(self) -> str:
        return "Nothing"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, Nothing)

    def __ne__(self, other: Any) -> bool:
        return not (self == other)

    def __hash__(self) -> int:
        return hash((False, "nothing"))

    def is_none(self) -> bool:
        return True

    def is_nothing(self) -> bool:
        return True

    def is_some(self) -> bool:
        return False

    def is_some_and(self, f: Callable[[Any], bool]) -> bool:
        return False

    @property
    def value(self) -> None:
        return None

    def map(self, _: Callable[[Any], U]) -> "Nothing":
        return self

    def map_or(self, default: U, _: Callable[[Any], U]) -> U:
        return default

    def map_or_else(self, default: Callable[[], U], _: Callable[[Any], U]) -> U:
        return default()

    def or_else(self, f: Callable[[], Some[T]]) -> Some[T]:
        return f()

    def unwrap(self) -> NoReturn:
        raise UnwrapError(self, "Called `Option.unwrap()` on an `Nothing` value")

    def unwrap_or(self, default: U) -> U:
        return default

    def unwrap_or_else(self, default: Callable[[], T]) -> T:
        return default()


Option = Union[Some[T], Nothing]


class UnwrapError(Exception):
    _option: Option[Any]

    def __init__(self, option: Option[Any], message: str) -> None:
        self._option = option
        super().__init__(message)

    @property
    def option(self) -> Option[Any]:
        return self._option
