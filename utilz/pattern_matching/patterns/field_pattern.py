from miniz.interfaces.oop import IField
from miniz.type_system import assignable_to
from miniz.vm import instructions as vm
from utilz.analysis.analyzers import ResultTypeAnalyzer
from utilz.code_generation.code_objects import BoundMemberCode
from utilz.code_generation.core import CodeGenerationResult
from utilz.pattern_matching import IPattern, BasicMatchResult


class FieldPattern(IPattern):
    _field: IField

    def __init__(self, field: IField):
        self._field = field

    @property
    def field(self):
        return self._field

    def match(self, source: CodeGenerationResult, *, target: CodeGenerationResult = None, **kwargs) -> BasicMatchResult | None:
        instance = []
        if self.field.is_instance_bound:
            if isinstance(target, BoundMemberCode):
                instance = target.instance
            else:
                instance = target.code
        source_type = ResultTypeAnalyzer.quick_analysis(source.code, {}).result_type
        if not assignable_to(source_type, self.field.field_type):
            return None
        return BasicMatchResult(self, source, [*instance, *source.code, vm.SetField(self.field)])
