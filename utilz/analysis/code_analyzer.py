from dataclasses import dataclass
from typing import TypeVar, Generic, Type, Any

from miniz.core import ObjectProtocol, TypeProtocol
from miniz.interfaces.signature import IParameter
from miniz.vm.instruction import Instruction

_T = TypeVar("_T", bound="Analyzer")


class AnalyzerResult(Generic[_T]):
    _analyzer: _T

    def __init__(self, analyzer: _T):
        self._analyzer = analyzer

    @property
    def analyzer(self):
        return self._analyzer


@dataclass(slots=True, frozen=True)
class CodeAnalysisResult:
    code: list[Instruction]
    context: dict[IParameter, ObjectProtocol]

    additional_information: dict[Type[_T], AnalyzerResult[_T] | Any] | None


class Analyzer:
    def analyze(self: _T, result: CodeAnalysisResult) -> AnalyzerResult[_T]:
        raise NotImplementedError(f"{type(self).__name__}.analyze({CodeAnalysisResult.__name__})")

    def reset(self):
        raise NotImplementedError(f"{type(self).__name__}.reset()")

    @classmethod
    def quick_analysis(cls: Type[_T], code: list[Instruction], context: dict[IParameter, ObjectProtocol], *args, **kwargs) -> AnalyzerResult[_T]:
        analyzer = CodeAnalyzer()
        analyzer.add_analyzer(cls(*args, **kwargs))
        return analyzer.analyze(code, context).additional_information[cls]


class CodeAnalyzer:
    _analyzers: list[Analyzer]

    def __init__(self):
        self._analyzers = []

    @property
    def analyzers(self):
        return self._analyzers

    def add_analyzer(self, analyzer: Analyzer):
        self._analyzers.append(analyzer)

    def reset(self):
        for analyzer in self._analyzers:
            analyzer.reset()

    def analyze(self, code: list[Instruction], context: dict[IParameter, ObjectProtocol]) -> CodeAnalysisResult:
        self.reset()

        result = CodeAnalysisResult(code=code, context=context, additional_information={})

        for analyzer in self._analyzers:
            result.additional_information[type(analyzer)] = analyzer.analyze(result)

        return result

    @classmethod
    def quick_analysis(cls, code: list[Instruction], context: dict[IParameter, ObjectProtocol], *analyzers: Analyzer):
        result = cls()
        for analyzer in analyzers:
            result.add_analyzer(analyzer)
        return result.analyze(code, context)
