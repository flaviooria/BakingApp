from typing_extensions import TypeVar, Union, Generic, Callable

L = TypeVar("L")
R = TypeVar("R")
T = TypeVar("T")


class Either(Generic[L, R]):

    def __init__(self, value: Union[L, R]):
        self.__inner_value = value

    def is_left(self) -> bool:
        return isinstance(self, Left)

    def is_right(self) -> bool:
        return isinstance(self, Right)

    def fold(self, left_fn: Callable[[L], T], right_fn: Callable[[R], T]):
        """
        Aplica una función a Left o Right, dependiendo del tipo.
        - left_fn: Función que se aplica si es Left.
        - right_fn: Función que se aplica si es Right.
        Retorna el resultado de la función aplicada.
        """
        if self.is_left():
            return left_fn(self.__inner_value)
        else:
            return right_fn(self.__inner_value)


class Left(Either[L, R]):
    def __init__(self, value: L):
        super().__init__(value)


class Right(Either[L, R]):
    def __init__(self, value: R):
        super().__init__(value)
