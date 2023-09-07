from typeclass import Typeclass, typeclass_api

from miniz.core import ObjectProtocol
from utilz.code_generation.core import CodeGenerationResult


class IScope(Typeclass):
    @typeclass_api
    def get_member(self, item: CodeGenerationResult, name: str) -> CodeGenerationResult | ObjectProtocol:
        raise NotImplementedError
