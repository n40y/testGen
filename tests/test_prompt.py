# ============================================================================
# src/tests/test_prompt.py
# 
# 
# ============================================================================

from pathlib import Path

from testgen.extract import extract_function
from testgen.prompt import build_instruction

SAMPLES = Path(__file__).parent.parent / "samples"


def test_simple_function_imports_the_function():
    f = extract_function(SAMPLES / "primes.py", "is_prime")
    text = build_instruction(f, "Return True if number is prime.")
    assert "from primes import is_prime" in text
    assert "def is_prime" in text
    assert "Return True if number is prime." in text


def test_method_requests_an_instance():
    f = extract_function(SAMPLES / "calculator.py", "Calcul.div")
    texte = build_instruction(f, "")
    assert "from calculator import Calcul" in texte
    assert "Calcul()" in texte


def test_missing_objective_is_reported():
    f = extract_function(SAMPLES / "primes.py", "is_prime")
    assert "Not provided" in build_instruction(f, "   ")


def test_triple_backticks_in_the_code_do_not_break_the_block(tmp_path):
    source = tmp_path / "piege.py"
    source.write_text('def f():\n    """Example ```python x```"""\n    return 1\n',
                      encoding="utf-8")
    text = build_instruction(extract_function(source, "f"), "test")
    assert "````python" in text
