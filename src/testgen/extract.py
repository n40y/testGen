# ============================================================================
# src/testgen/extract.py
# 
# Reads a Python file and isolates a function using the `ast` module.
# It returns (name, signature, docstring, source code, module name,
# parent class and line range).
# ============================================================================

"""
Extracting a function from a Python file

Demonstration:

    python extract.py samples/my_file.py my_function
    python extract.py samples/calculator.py Calcul.div     # method of a class
"""

import ast
import sys
import textwrap
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

_FUNCTION_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)
FunctionNode = ast.FunctionDef | ast.AsyncFunctionDef


def _qualify(name: str, parent_class: str | None) -> str:
    """'Class.method' for a method, 'function' otherwise."""
    return f"{parent_class}.{name}" if parent_class else name


@dataclass
class ExtractedFunction:
    name: str
    code: str
    signature: str
    docstring: str | None
    module: str                 # file name without dot extension
    path: Path
    parent_class: str | None    # None if the function is not a method
    lineno: int                 # first line of the function in the file (1-based)
    end_lineno: int             # last line of the function in the file

    @property
    def qualified_name(self) -> str:
        return _qualify(self.name, self.parent_class)


def _build_signature(node: FunctionNode) -> str:
    """
    Reconstructs the definition line: def name(args) -> return.
    """
    begin = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    signature = f"{begin} {node.name}({ast.unparse(node.args)})"
    if node.returns is not None:
        signature += f" -> {ast.unparse(node.returns)}"
    return signature


def _iter_functions(
    node: ast.AST, current_class: str | None = None
) -> Iterator[tuple[FunctionNode, str | None]]:
    """
    Walks the tree and yields (function node, name of the enclosing class).
    The class is None when the function is not directly inside a class.
    """
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ClassDef):
            yield from _iter_functions(child, child.name)
        elif isinstance(child, _FUNCTION_TYPES):
            yield child, current_class
            # A function nested inside a function is not a method.
            yield from _iter_functions(child, None)
        else:
            yield from _iter_functions(child, current_class)


def list_functions(file_path: str | Path) -> list[str]:
    """
    Returns the names of all functions defined in the file.
    Methods are returned as 'Class.method'.
    """
    source = Path(file_path).read_text(encoding="utf-8")
    tree = ast.parse(source)
    return [_qualify(n.name, cls) for n, cls in _iter_functions(tree)]


def extract_function(file_path: str | Path, function_name: str) -> ExtractedFunction:
    """
    Isolates a function: source code, signature, docstring, class, lines.
    `function_name` can be 'name' or 'Class.name' (needed if the name is ambiguous).
    """
    path = Path(file_path)
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)

    matches = [
        (node, cls)
        for node, cls in _iter_functions(tree)
        if function_name in (node.name, _qualify(node.name, cls))
    ]

    if not matches:
        availables = ", ".join(list_functions(path)) or "none"
        raise ValueError(
            f"Function '{function_name}' not found in {path}. "
            f"Available functions: {availables}"
        )

    if len(matches) > 1:
        candidates = ", ".join(_qualify(n.name, c) for n, c in matches)
        raise ValueError(
            f"Function name '{function_name}' is ambiguous in {path}. "
            f"Use 'Class.method'. Candidates: {candidates}"
        )

    node, parent_class = matches[0]

    # padded=True keeps the original indentation of the first line, so that
    # textwrap.dedent can then remove the same indentation from every line.
    segment = ast.get_source_segment(source, node, padded=True) or ""

    return ExtractedFunction(
        name = node.name,
        code = textwrap.dedent(segment),
        signature = _build_signature(node),
        docstring = ast.get_docstring(node),
        module = path.stem,
        path = path,
        parent_class = parent_class,
        lineno = node.lineno,
        end_lineno = node.end_lineno or node.lineno,
    )


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage :  python extract.py <file.py> <function_name>")
        sys.exit(1)

    result = extract_function(sys.argv[1], sys.argv[2])
    print(f"Module          : {result.module}")
    print(f"Class           : {result.parent_class}")
    print(f"Lines           : {result.lineno}-{result.end_lineno}")
    print(f"Signature       : {result.signature}")
    print(f"Docstring       : {result.docstring}")
    print("-------     code    -------")
    print(result.code)
