import hmac
import posixpath


def sanitize_filename(name: str) -> str:
    return "".join(char if char.isascii() else '_' for char in name)


def is_within_base(base: str, user_path: str) -> bool:
    """
    Chemins Posix sans accès disque.
    Base est absolu et normalisé.
    Normalise les deux avec posixpath.normpath
    True si le résultat est base ou se trouve sous base.
    user_path absolu -> return False.
    """
    if user_path.startswith('/'):
        return False
    
    norm_base = posixpath.normpath(base)
    norm_full = posixpath.normpath(posixpath.join(norm_base, user_path))
    
    return norm_full == norm_base or norm_full.startswith(norm_base + '/')

    
def secure_equals(a: bytes, b: bytes) -> bool:
    if type(a) != type(b):
        return False
    return hmac.compare_digest(a, b)


def is_valid_port(s: str) -> bool:
    """
    True si s ne contient que des chiffres ASCII 0-9, sans zéro initial,
    de valeur 1 à 65535.
    """
    if not s.isdigit():
        return False
    if len(s) > 1 and s[0] == '0':
        return False
    val = int(s)
    return 1 <= val <= 65535


def mask_secret(secret: str, visible: int=4) -> str:
    """
    emplace par * tous les caractères sauf les visible derniers ;
    si len(secret) <= visible, tout est masqué ;
    ValueError si visible < 0.
    """
    if visible < 0:
        raise ValueError("visible must be >= 0")
    
    if len(secret) <= visible:
        return '*' * len(secret)
    return '*' * (len(secret) - visible) + secret[-visible:]


def html_escape(s: str) -> str:
    return (
        s.replace('&', '&amp;')
        .replace('<', '&lt;')
        .replace('>', '&gt;')
        .replace('"', '&quot;')
        .replace("'", '&#x27;')
    )


def sanitize_header_value(value: str) -> str:
    return value.replace('\r', '').replace('\n', '')

    
def validate_password(pw: str) -> bool:
    specials = "#@$*%!&"
    if len(pw) < 12:
        return False
    
    minuscul = sum(1 for x in pw if x.islower())
    majuscul = sum(1 for x in pw if x.isupper())
    digit = sum(1 for x in pw if x.isdigit())
    special = sum(1 for x in pw if x in specials)
    
    return bool(minuscul and majuscul and digit and special)
