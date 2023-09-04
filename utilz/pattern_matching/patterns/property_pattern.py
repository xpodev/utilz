from miniz.concrete.function import Function
from miniz.interfaces.oop import IProperty
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm
from utilz.analysis.analyzers import ResultTypeAnalyzer
from utilz.code_generation.code_objects import BoundMemberCode
from utilz.code_generation.core import CodeGenerationResult
from utilz.pattern_matching import IPattern, BasicMatchResult


class PropertyPattern(IPattern):
    _property: IProperty

    def __init__(self, prop: IProperty):
        self._property = prop

    @property
    def property(self):
        return self._property

    def match(self, source: CodeGenerationResult, *, target: CodeGenerationResult = None, **kwargs) -> BasicMatchResult | None:
        instance = []
        if self.property.is_instance_bound:
            if isinstance(target, BoundMemberCode):
                instance = target.instance
            else:
                instance = target.code
        source_type = ResultTypeAnalyzer.quick_analysis(source.code, {}).result_type
        if not assignable_to(source_type, self.property.property_type):
            return None
        if self.property.setter is None:
            return None
        assert isinstance(self.property.setter, Function)
        return BasicMatchResult(self, source, [*instance, *source.code, vm.Call(self.property.setter)])
