# ============================================================================
# src/testgen/report.py
# 
# Affiche le résultat des tests dans le terminal et l'enregistre en JSON.
# ============================================================================

import json
from dataclasses import asdict
from pathlib import Path

from testgen.extract import ExtractedFunction
from testgen.runner import ResultatTests


def report_print(function: ExtractedFunction, result: ResultatTests) -> None:
    """
    Displays the test results (passed / failed) in the terminal.
    """
    print(f"=== Report : {function.qualified_name} "
          f"({function.module}.py, lines {function.lineno}-{function.end_lineno}) ===")

    if result.expire:
        print("Maximum time limit exceeded: execution interrupted "
              "(infinite loop possible in a test or in the code).")
        return

    if not result.collecte_ok:
        print("The generated tests are not executable "
              "(syntax error, import error, or no tests).")
        print("Final lines of the pytest output:")
        print("\n".join(result.sortie.splitlines()[-15:]))
        return

    print(f"Tests : {result.tests_total} | succeed : {result.reussis} | "
          f"Failures : {result.echoues} | errors : {result.erreurs} | "
          f"Ignored : {result.ignores}")

    if result.couverture_fonction is not None:
        print(f"Function coverage : {result.couverture_fonction:.0f} %")
    if result.couverture is not None:
        print(f"File cover        : {result.couverture:.0f} %")

    problemes = [ligne for ligne in result.sortie.splitlines()
                 if ligne.startswith(("FAILED", "ERROR"))]
    for ligne in problemes:
        print(f"  {ligne}")

    if result.echoues or result.erreurs:
        print("Tests are failing: either a real bug in the code OR an incorrect test. "
              "To be checked by hand.")
    else:
        print("All tests pass: this is not proof that the code "
              "is correct (mutation testing will be required).")


def save_report(function: ExtractedFunction, result: ResultatTests,
                dossier: str | Path = "generated") -> Path:
    """
    Save the result as JSON and return the file path.
    """
    dossier = Path(dossier)
    dossier.mkdir(parents=True, exist_ok=True)
    chemin = dossier / f"rapport_{function.qualified_name.replace('.', '_')}.json"

    contenu = {
        "function": function.qualified_name,
        "module": function.module,
        "lines": [function.lineno, function.end_lineno],
        "collecte_ok": result.collecte_ok,
        "result": asdict(result),
    }
    chemin.write_text(json.dumps(contenu, indent=2, ensure_ascii=False),
                      encoding="utf-8")
    return chemin
