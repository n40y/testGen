# ============================================================================
# main.py
# 
# Command Line's entry point.
#
#   python main.py samples/IPv4_valid.py is_valid_IPv4 \
#       --objectif "Renvoie True si la chaîne est une adresse IPv4 valide"
# ============================================================================

import argparse
import sys
from pathlib import Path

from testgen.extract import extract_function
from testgen.llm import extract_code, generate_tests
from testgen.prompt import build_instruction
from testgen.report import report_print, save_report
from testgen.runner import lancer_tests


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Generates and executes pytest tests for a Python function."
    )
    parser.add_argument("file", help="Python file containing the function")
    parser.add_argument("function", help="function name (or Class.method)")
    parser.add_argument("--objective", default="",
                        help="what the function should do (otherwise: the docstring)")
    parser.add_argument("--see-instructions", action="store_true",
                        help="displays the prompt without calling the model")
    args = parser.parse_args(argv)

    try:
        function = extract_function(args.file, args.function)
    except (OSError, ValueError, SyntaxError) as error:
        print(f"Error : {error}", file=sys.stderr)
        return 2

    instruction = build_instruction(function, args.objective)
    if args.see_instruction:
        print(instruction)
        return 0

    try:
        response = generate_tests(instruction)
    except RuntimeError as error:
        print(f"Erreur : {error}", file=sys.stderr)
        return 2

    folder = Path("generated")
    folder.mkdir(exist_ok=True)
    test_file = folder / f"test_{function.qualified_name.replace('.', '_')}.py"
    test_file.write_text(extract_code(response), encoding="utf-8")
    print(f"Tests écrits dans {test_file}")

    result = lancer_tests(
        function.path, test_file,
        ligne_debut=function.lineno, ligne_fin=function.end_lineno,
    )
    report_print(function, result)
    print(f"JSON Report : {save_report(function, result)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
