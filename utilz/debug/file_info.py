from pathlib import Path


__all__ = [
    "DocumentInfo",
    "Position",
    "Span",
]


class DocumentInfo:
    _path: Path

    def __init__(self, path: str | Path):
        super().__init__()
        if isinstance(path, str):
            path = Path(path)
        self._path = path

    @property
    def path(self):
        return self._path

    @property
    def path_string(self):
        return str(self._path)

    @classmethod
    def from_path(cls, path: "str | Path | DocumentInfo") -> "DocumentInfo":
        if isinstance(path, str):
            path = Path(path)
        if isinstance(path, Path):
            path = DocumentInfo(path.resolve())
        return path

    def __str__(self):
        return f"Document @ {self.path}"


class Position:
    _line: int
    _column: int

    def __init__(self, line: int, column: int):
        super().__init__()
        self._line = line
        self._column = column

    @property
    def line(self):
        return self._line

    @property
    def column(self):
        return self._column

    def move_by(self, line: int, column: int):
        self._line += line
        self._column += column

    def move_to(self, line: int, column: int):
        self._line = line
        self._column = column

    def next_line(self):
        self._line += 1
        self._column = 1

    def next_column(self):
        self._column += 1

    def copy(self):
        return Position(self._line, self._column)

    def set(self, position: "Position"):
        self._line = position._line
        self._column = position._column

    def __str__(self):
        return f'{self._line}:{self._column}'

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self._line}, {self._column})'


class Span:
    _start: Position
    _end: Position

    def __init__(self, start: Position, end: Position):
        super().__init__()
        self._start = start
        self._end = end

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @classmethod
    def combine(cls, *spans: "Span"):
        if not spans:
            raise ValueError
        min_span = max_span = spans[0]
        for span in spans:
            if span.start.line < min_span.start.line:
                min_span = span
            elif span.start.line == min_span.start.line and span.start.column < min_span.start.column:
                min_span = span

            if span.end.line > max_span.end.line:
                max_span = span
            elif span.end.line == max_span.end.line and span.end.column > max_span.end.column:
                max_span = span
        return Span(min_span.start, max_span.end)

    def __str__(self):
        return f"Span: {self._start} -> {self._end}"

    def __repr__(self):
        return f"Span({repr(self._start)}, {repr(self._end)})"
