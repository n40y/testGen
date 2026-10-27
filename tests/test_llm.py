# ============================================================================
# src/tests/test_llm.py
# 
# 
# ============================================================================

from testgen.llm import extract_code


def test_block_python_with_text_around():
    response = "Here is :\n```python\ndef test_a():\n    assert True\n```\nFin."
    assert extract_code(response) == "def test_a():\n    assert True\n"


def test_response_without_tags():
    assert extract_code("def test_a(): pass") == "def test_a(): pass\n"


def test_bloc_non_ferme():
    response = "```python\ndef test_a():\n    assert True"
    assert extract_code(response) == "def test_a():\n    assert True\n"


def test_multiple_blocks_keeps_the_longest():
    response = "```\nx = 1\n```\n```python\ndef test_a():\n    assert True\n```"
    assert "def test_a" in extract_code(response)
