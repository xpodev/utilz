from miniz.core import TypeProtocol
from utilz.pattern_matching import IPattern
from utilz.pattern_matching.core import IMatchResult
from miniz.vm.instruction import Instruction


class SignatureMatchResult(IMatchResult):
    ...


class SignaturePattern(IPattern):
    def match(
            self,
            source: TypeProtocol,
            *,
            args: list[list[Instruction]] = None,
            kwargs: dict[str, list[Instruction]] = None,
            allow_partial: bool = False,
            **_
    ) -> SignatureMatchResult | None:
        ...
