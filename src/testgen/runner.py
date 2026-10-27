# ============================================================================
# src/testgen/runner.py
# 
# Running a pytest test file against a target file          
# ============================================================================

"""
Utilisation de démonstration :

    python runner.py samples/my_file.py references/test_my_file.py
"""

# ATTENTION :
#    le code lancé ici s'exécute sur ta machine. Pour des tests générés
#    par une IA, passer ensuite par Docker (sans réseau) dès que le prototype tourne.
#    L'environnement réduit ci-dessous cache les variables (clé d'API), mais
#    n'empêche PAS un test de lire des fichiers ou d'ouvrir une connexion réseau.


import json
import os
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path

# Variables d'environnement transmises au sous-processus (tout le reste est retiré).
VARIABLES_AUTORISEES = ("PATH", "SYSTEMROOT", "TEMP", "TMP", "LANG", "LC_ALL")


@dataclass
class ResultatTests:
    code_retour: int | None
    tests_total: int = 0
    reussis: int = 0
    echoues: int = 0
    erreurs: int = 0
    ignores: int = 0
    couverture: float | None = None           # pourcentage du fichier cible entier
    couverture_fonction: float | None = None  # pourcentage de la fonction ciblée
    expire: bool = False             # True si le délai maximal est dépassé
    sortie: str = ""                 # sortie brute de pytest, utile au débogage

    @property
    def collecte_ok(self) -> bool:
        """
        False if the test file fails to compile, fails to import,
        or contains no tests (pytest codes 2, 3, 4, and 5).
        """
        return not self.expire and self.code_retour not in (2, 3, 4, 5)


def _environnement_minimal() -> dict[str, str]:
    """
    Restricted environment: the subprocess sees neither API keys nor secrets.
    """
    env = {k: os.environ[k] for k in VARIABLES_AUTORISEES if k in os.environ}
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def _lire_junit(chemin_xml: Path) -> tuple[int, int, int, int]:
    """
    Returns (total, failures, errors, ignored) from the JUnit report.
    """
    racine = ET.parse(chemin_xml).getroot()
    suite = racine if racine.tag == "testsuite" else racine.find("testsuite")
    if suite is None:
        return 0, 0, 0, 0
    return (
        int(suite.get("tests", 0)),
        int(suite.get("failures", 0)),
        int(suite.get("errors", 0)),
        int(suite.get("skipped", 0)),
    )


def _lire_couverture(
    chemin_json: Path,
    nom_fichier: str,
    ligne_debut: int | None = None,
    ligne_fin: int | None = None,
) -> tuple[float | None, float | None]:
    """
    Returns (file coverage, function coverage) as percentages.
    The second value is calculated only if the line range is provided.
    """
    if not chemin_json.exists():
        return None, None

    donnees = json.loads(chemin_json.read_text(encoding="utf-8"))
    fichier = donnees.get("totals", {}).get("percent_covered")

    if ligne_debut is None or ligne_fin is None:
        return fichier, None

    for chemin, infos in donnees.get("files", {}).items():
        if Path(chemin).name != nom_fichier:
            continue
        executees = [n for n in infos.get("executed_lines", [])
                     if ligne_debut <= n <= ligne_fin]
        manquantes = [n for n in infos.get("missing_lines", [])
                      if ligne_debut <= n <= ligne_fin]
        total = len(executees) + len(manquantes)
        if total:
            return fichier, 100 * len(executees) / total

    return fichier, None


def lancer_tests(
    fichier_cible: str | Path,
    fichier_test: str | Path,
    delai: int = 30,
    ligne_debut: int | None = None,
    ligne_fin: int | None = None,
) -> ResultatTests:
    """
    Copies the target and the tests into a temporary directory, then runs pytest.
    If `line_debut` and `line_fin` are provided (ExtractedFunction.lineno and
    end_lineno), coverage is also calculated for that specific function.
    """
    cible = Path(fichier_cible)
    test = Path(fichier_test)

    with tempfile.TemporaryDirectory(prefix="testgen_") as dossier:
        dossier = Path(dossier)
        shutil.copy2(cible, dossier / cible.name)
        shutil.copy2(test, dossier / test.name)

        rapport_xml = dossier / "result.xml"
        rapport_cov = dossier / "coverage.json"

        commande = [
            sys.executable, "-m", "pytest", test.name,
            "-p", "no:cacheprovider",
            f"--junitxml={rapport_xml.name}",
            f"--cov={cible.stem}",
            f"--cov-report=json:{rapport_cov.name}",
        ]

        try:
            processus = subprocess.run(
                commande,
                cwd=dossier,
                env=_environnement_minimal(),
                capture_output=True,
                text=True,
                timeout=delai,
            )
        except subprocess.TimeoutExpired:
            return ResultatTests(
                code_retour=None,
                expire=True,
                sortie=f"Time limit of {delai} exceeded : execution interrupted.",
            )

        resultat = ResultatTests(
            code_retour=processus.returncode,
            sortie=processus.stdout + processus.stderr,
        )

        if rapport_xml.exists():
            total, echecs, erreurs, ignores = _lire_junit(rapport_xml)
            resultat.tests_total = total
            resultat.echoues = echecs
            resultat.erreurs = erreurs
            resultat.ignores = ignores
            resultat.reussis = total - echecs - erreurs - ignores

        resultat.couverture, resultat.couverture_fonction = _lire_couverture(
            rapport_cov, cible.name, ligne_debut, ligne_fin
        )
        return resultat


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage : python runner.py <target_file.py> <test_file.py>")
        sys.exit(1)

    r = lancer_tests(sys.argv[1], sys.argv[2])
    print(f"Collection OK : {r.collecte_ok}")
    print(f"Time limit exceeded : {r.expire}")
    print(f"Total : {r.tests_total} | succeed : {r.reussis} | "
          f"Faileds : {r.echoues} | errors : {r.erreurs} | ignored : {r.ignores}")
    print(f"Total coverage : {r.couverture if r.couverture is not None else 'n/a'} %")
    print("--- pytest output ---")
    print(r.sortie)
