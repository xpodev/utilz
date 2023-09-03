from typeclass import Typeclass, typeclass_api

from utilz.code_generation.core import CodeGenerationResult


class IScope(Typeclass):
    @typeclass_api
    def get_member(self, item: CodeGenerationResult, name: str) -> CodeGenerationResult:
        raise NotImplementedError
