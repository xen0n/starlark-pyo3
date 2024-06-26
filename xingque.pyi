from typing import Callable, Iterable, Iterator, Protocol, Self

VERSION: str
STARLARK_RUST_VERSION: str

# starlark::codemap

class CodeMap:
    def __init__(self, filename: str, source: str) -> None: ...
    # TODO: empty_static
    def full_span(self) -> Span: ...
    def file_span(self, span: Span) -> FileSpan: ...
    @property
    def filename(self) -> str: ...
    def byte_at(self, pos: Pos) -> int: ...
    def find_line(self, pos: Pos) -> int: ...
    @property
    def source(self) -> str: ...
    def source_span(self, span: Span) -> str: ...
    def line_span(self, line: int) -> Span: ...
    def line_span_opt(self, line: int) -> Span | None: ...
    def resolve_span(self, span: Span) -> ResolvedSpan: ...
    def source_line(self, line: int) -> str: ...
    def source_line_at_pos(self, pos: Pos) -> str: ...

class FileSpan:
    def __init__(self, filename: str, source: str) -> None: ...
    @property
    def file(self) -> CodeMap: ...
    @property
    def span(self) -> Span: ...
    @property
    def filename(self) -> str: ...
    @property
    def source_span(self) -> str: ...
    def resolve_span(self) -> ResolvedSpan: ...
    def resolve(self) -> ResolvedFileSpan: ...

class Pos:
    def __init__(self, x: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def get(self) -> int: ...
    def __int__(self) -> int: ...
    def __add__(self, other: int) -> Self: ...
    def __iadd__(self, other: int) -> None: ...

class ResolvedFileLine:
    file: str
    line: int
    def __init__(self, file: str, line: int) -> None: ...
    def __eq__(self, other: object) -> bool: ...

class ResolvedFileSpan:
    file: str
    span: ResolvedSpan
    def __init__(self, file: str, span: ResolvedSpan) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    def begin_file_line(self) -> ResolvedFileLine: ...

class ResolvedPos:
    def __init__(self, line: int, column: int) -> None: ...
    @property
    def line(self) -> int: ...
    @property
    def column(self) -> int: ...

class ResolvedSpan:
    def __init__(self, begin: ResolvedPos, end: ResolvedPos) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def begin(self) -> ResolvedPos: ...
    @property
    def end(self) -> ResolvedPos: ...
    def __contains__(self, pos: ResolvedPos) -> bool: ...
    def contains(self, pos: ResolvedPos) -> bool: ...

class Span:
    def __init__(self, begin: Pos, end: Pos) -> None: ...
    def __eq__(self, other: object) -> bool: ...
    @property
    def begin(self) -> Pos: ...
    @property
    def end(self) -> Pos: ...
    def merge(self, other: Self) -> Self: ...
    # TODO: merge_all
    def end_span(self) -> Self: ...
    def __contains__(self, pos: Pos | int) -> bool: ...
    def contains(self, pos: Pos | int) -> bool: ...

# starlark::environment

class FrozenModule:
    @staticmethod
    def from_globals(globals: Globals) -> FrozenModule: ...
    def get_option(self, name: str) -> object | None: ...
    def get(self, name: str) -> object | None: ...
    def names(self) -> Iterator[str]: ...
    def describe(self) -> str: ...
    # TODO: documentation
    # TODO: aggregated_heap_profile_info
    @property
    def extra_value(self) -> object | None: ...

class Globals:
    def __init__(self) -> None: ...
    @staticmethod
    def standard() -> Globals: ...
    @staticmethod
    def extended_by(extensions: Iterable[LibraryExtension]) -> Globals: ...
    def names(self) -> Iterator[str]: ...
    def __iter__(self) -> Iterator[tuple[str, object]]: ...
    def describe(self) -> str: ...
    @property
    def docstring(self) -> str | None: ...
    # TODO: documentation

class GlobalsBuilder:
    def __init__(self) -> None: ...
    @staticmethod
    def standard() -> GlobalsBuilder: ...
    @staticmethod
    def extended_by(extensions: Iterable[LibraryExtension]) -> GlobalsBuilder: ...
    def struct(self, name: str, f: Callable[[_SubGlobalsBuilder], None]) -> None: ...
    def with_(self, f: Callable[[_SubGlobalsBuilder], None]) -> Self: ...
    def with_struct(
        self, name: str, f: Callable[[_SubGlobalsBuilder], None]
    ) -> Self: ...
    def build(self) -> Globals: ...
    def set(self, name: str, value: object) -> None: ...
    # TODO: set_function

class _SubGlobalsBuilder:
    def struct(self, name: str, f: Callable[[_SubGlobalsBuilder], None]) -> None: ...
    def with_(self, f: Callable[[_SubGlobalsBuilder], None]) -> Self: ...
    def with_struct(
        self, name: str, f: Callable[[_SubGlobalsBuilder], None]
    ) -> Self: ...
    def set(self, name: str, value: object) -> None: ...

class LibraryExtension:
    STRUCT_TYPE: LibraryExtension
    """Definitions to support the `struct` type, the `struct()` constructor."""

    RECORD_TYPE: LibraryExtension
    """Definitions to support the `record` type, the `record()` constructor and `field()` function."""

    ENUM_TYPE: LibraryExtension
    """Definitions to support the `enum` type, the `enum()` constructor."""

    MAP: LibraryExtension
    """A function `map(f, xs)` which applies `f` to each element of `xs` and returns the result."""

    FILTER: LibraryExtension
    """A function `filter(f, xs)` which applies `f` to each element of `xs` and returns those for which `f` returns `True`.
    As a special case, `filter(None, xs)` removes all `None` values.
    """

    PARTIAL: LibraryExtension
    """Partially apply a function, `partial(f, *args, **kwargs)` will create a function where those `args` `kwargs`
    are already applied to `f`.
    """

    DEBUG: LibraryExtension
    """Add a function `debug(x)` which shows the Rust `Debug` representation of a value.
    Useful when debugging, but the output should not be considered stable.
    """

    PRINT: LibraryExtension
    """Add a function `print(x)` which prints to stderr."""

    PPRINT: LibraryExtension
    """Add a function `pprint(x)` which pretty-prints to stderr."""

    BREAKPOINT: LibraryExtension
    """Add a function `breakpoint()` which will drop into a console-module evaluation prompt."""

    JSON: LibraryExtension
    """Add a function `json()` which will generate JSON for a module."""

    TYPING: LibraryExtension
    """Provides `typing.All`, `typing.Callable` etc.
    Usually used in conjunction with `Dialect.enable_types`."""

    INTERNAL: LibraryExtension
    """Utilities exposing starlark-rust internals.
    These are not for production use."""

    CALL_STACK: LibraryExtension
    """Add a function `call_stack()` which returns a string representation of
    the current call stack."""

class Module:
    extra_value: object | None = None
    def __init__(self) -> None: ...
    def names(self) -> Iterator[str]: ...
    def get(self, name: str) -> object: ...
    def set(self, name: str, value: object) -> None: ...
    def freeze(self) -> FrozenModule: ...

# starlark::eval

class _FileLoader(Protocol):
    def load(self, path: str) -> FrozenModule: ...

class DictFileLoader:
    def __init__(self, modules: dict[str, FrozenModule]) -> None: ...
    def load(self, path: str) -> FrozenModule: ...

class Evaluator:
    def __init__(self, module: Module | None = None) -> None: ...
    # TODO: disable_gc
    def eval_statements(self, statements: AstModule) -> object: ...
    def local_variables(self) -> dict[str, object]: ...
    def verbose_gc(self) -> None: ...
    def enable_static_typechecking(self, enable: bool) -> None: ...
    def set_loader(self, loader: _FileLoader) -> None: ...
    # TODO: enable_profile
    # TODO: write_profile
    # TODO: gen_profile
    # TODO: coverage
    def enable_terminal_breakpoint_console(self) -> None: ...
    # TODO: call_stack
    # TODO: call_stack_top_frame
    def call_stack_count(self) -> int: ...
    def call_stack_top_location(self) -> FileSpan | None: ...
    # TODO: set_print_handler
    # TODO: heap
    @property
    def module(self) -> Module: ...
    # TODO: frozen_heap
    # TODO: set_module_variable_at_some_point (is this okay to expose?)
    def set_max_callstack_size(self, stack_size: int) -> None: ...
    def eval_module(self, ast: AstModule, globals: Globals) -> object: ...
    def eval_function(self, function: object, *args, **kwargs) -> object: ...

# starlark::syntax

class DialectTypes:
    DISABLE: DialectTypes
    PARSE_ONLY: DialectTypes
    ENABLE: DialectTypes

class Dialect:
    enable_def: bool
    enable_lambda: bool
    enable_load: bool
    enable_keyword_only_arguments: bool
    enable_types: DialectTypes
    enable_load_reexport: bool
    enable_top_level_stmt: bool
    enable_f_strings: bool
    def __init__(
        self,
        enable_def: bool = False,
        enable_lambda: bool = False,
        enable_load: bool = False,
        enable_keyword_only_arguments: bool = False,
        enable_types: DialectTypes = DialectTypes.DISABLE,
        enable_load_reexport: bool = False,
        enable_top_level_stmt: bool = False,
        enable_f_strings: bool = False,
    ) -> None: ...
    EXTENDED: Dialect
    STANDARD: Dialect

class AstLoad:
    @property
    def span(self) -> FileSpan: ...
    @property
    def module_id(self) -> str: ...
    @property
    def symbols(self) -> dict[str, str]: ...

class AstModule:
    @staticmethod
    def parse_file(path: str, dialect: Dialect = Dialect.STANDARD) -> AstModule: ...
    @staticmethod
    def parse(
        filename: str,
        content: str,
        dialect: Dialect = Dialect.STANDARD,
    ) -> AstModule: ...
    @property
    def loads(self) -> list[AstLoad]: ...
    def file_span(self, x: Span) -> FileSpan: ...
    @property
    def stmt_locations(self) -> list[FileSpan]: ...
    def replace_binary_operators(self, replace: dict[str, str]) -> None: ...

# starlark::values

class FrozenValue:
    pass

class HeapSummary:
    def summary(self) -> dict[str, tuple[int, int]]: ...
    @property
    def total_allocated_bytes(self) -> int: ...

class Heap:
    def __init__(self) -> None: ...
    @property
    def allocated_bytes(self) -> int: ...
    @property
    def peak_allocated_bytes(self) -> int: ...
    @property
    def available_bytes(self) -> int: ...
    def allocated_summary(self) -> HeapSummary: ...

class Value:
    pass
