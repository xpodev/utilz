from typeclass import typeclass_api, Typeclass

from miniz.core import ObjectProtocol
from miniz.interfaces.overloading import Argument
from utilz.code_generation.core import CodeGenerationResult


class ICallable(Typeclass):
    @typeclass_api
    def curvy_call(self, compiler, item: CodeGenerationResult, args: list[Argument], kwargs: list[tuple[str, Argument]]) -> CodeGenerationResult | ObjectProtocol:
        raise NotImplementedError

    @typeclass_api
    def square_call(self, compiler, item: CodeGenerationResult, args: list[Argument], kwargs: list[tuple[str, Argument]]) -> CodeGenerationResult | ObjectProtocol:
        raise NotImplementedError
