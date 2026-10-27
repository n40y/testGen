# ============================================================================
# src/testgen/llm.py
# 
# Appel au modèle de langage et nettoyage de sa réponse.
# Seule _appeler_api dépend du fournisseur : pour en changer, on ne modifie
# que cette fonction (et la dépendance dans pyproject.toml).
# ============================================================================

import os
import re

from dotenv import load_dotenv


def _load_configuration() -> tuple[str, str]:
    """
    Reads LLM_API_KEY and LLM_MODEL from .env 
    (or from the environment).
    """
    load_dotenv()
    key = os.getenv("LLM_API_KEY")
    model = os.getenv("LLM_MODEL")
    if not key or not model:
        raise RuntimeError(
            "LLM_API_KEY and LLM_MODEL must be specified in .env "
            "(see .env.example)."
        )
    return key, model


def _call_api(instruction: str, cle: str, modele: str) -> str:
    """
    Send the prompt to the model and return the text of its response.
    """
    import anthropic  # import local : seule cette fonction dépend du fournisseur

    client = anthropic.Anthropic(api_key=cle, timeout=60.0)
    try:
        response = client.messages.create(
            model=modele,
            max_tokens=4096,
            messages=[{"role": "user", "content": instruction}],
        )
    except anthropic.APIError as error:
        raise RuntimeError(f"Erreur de l'API : {error}") from error

    if response.stop_reason == "max_tokens":
        raise RuntimeError(
            "Truncated response (max_tokens reached): the code would be incomplete"
        )
    return "".join(b.text for b in response.content if b.type == "text")


def generate_tests(instruction: str) -> str:
    """
    Reads the configuration from .env, calls the API,
    and returns the model's raw response.
    """
    cle, modele = _load_configuration()
    return _call_api(instruction, cle, modele)


_BLOC_CODE = re.compile(r"```[a-zA-Z]*[ \t]*\n(.*?)```", re.DOTALL)


def extract_code(response: str) -> str:
    """
    Extracts Python code from a response: removes the ``` tags and any
    surrounding text.
    This function does not perform any network calls.
    """
    blocs = _BLOC_CODE.findall(response)
    if blocs:
        return max(blocs, key=len).strip() + "\n"

    # Pas de bloc complet : réponse sans balises, ou balise ouvrante sans fermeture.
    text = response.strip()
    text = re.sub(r"^```[a-zA-Z]*[ \t]*\n", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip() + "\n"
