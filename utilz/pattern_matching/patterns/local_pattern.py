from miniz.concrete.function import Local
from miniz.core import TypeProtocol
from utilz.pattern_matching import IPattern, BasicMatchResult
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm


class LocalPattern(IPattern):
    _local: Local

    def __init__(self, local: Local):
        self._local = local

    @property
    def local(self):
        return self._local

    def match(self, source: TypeProtocol) -> BasicMatchResult | None:
        if not assignable_to(source, self.local.type):
            return None
        return BasicMatchResult(self, source, [vm.SetLocal(self.local)])
