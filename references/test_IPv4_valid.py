# Tests écrits à la main pour samples/IPv4_valid.py (référence de comparaison).
#
# Ce fichier est volontairement en deux parties :
#   1. des tests qui doivent PASSER (le comportement correct déjà en place) ;
#   2. des tests qui doivent ÉCHOUER tant que les bugs connus existent
#      (voir samples/bugs_connus.md).
#
# Lancement : python -m testgen.runner samples/IPv4_valid.py references/test_IPv4_valid.py

from IPv4_valid import is_valid_IPv4


# --- 1. Comportement correct ---

def test_adresse_valide():
    assert is_valid_IPv4("192.168.1.1")


def test_bornes_valides():
    assert is_valid_IPv4("0.0.0.0")
    assert is_valid_IPv4("255.255.255.255")


def test_chaine_vide():
    assert not is_valid_IPv4("")


def test_nombre_d_octets_incorrect():
    assert not is_valid_IPv4("1.2.3")
    assert not is_valid_IPv4("1.2.3.4.5")


def test_premier_octet_trop_grand():
    assert not is_valid_IPv4("256.1.1.1")


# --- 2. Tests qui détectent les bugs connus ---

def test_deuxieme_octet_trop_grand():
    # Bug : le return dans la boucle ne vérifie que le premier octet.
    assert not is_valid_IPv4("1.999.1.1")


def test_octet_vide():
    # Bug : même cause, "1.2.3." est accepté.
    assert not is_valid_IPv4("1.2.3.")


def test_octets_non_numeriques():
    # Bug : int() lève ValueError au lieu de renvoyer False.
    assert not is_valid_IPv4("a.b.c.d")
