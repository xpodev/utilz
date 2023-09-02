from miniz.concrete.function import Parameter
from miniz.core import TypeProtocol
from utilz.pattern_matching import IPattern, BasicMatchResult
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm


class ParameterPattern(IPattern):
    _parameter: Parameter

    def __init__(self, local: Parameter):
        self._parameter = local

    @property
    def parameter(self):
        return self._parameter

    def match(self, source: TypeProtocol, **_) -> BasicMatchResult | None:
        if not assignable_to(source, self.parameter.parameter_type):
            return None
        return BasicMatchResult(self, source, [vm.SetArgument(self.parameter)])
