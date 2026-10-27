# Bugs connus des fonctions témoins

Liste de référence pour mesurer si les tests générés détectent les vrais bugs.
Une fonction sans bug sert à mesurer les faux positifs (tests qui accusent du
code correct).

## calculator.py — `Calcul.div`

- Division par zéro non gérée : `div(10, 0)` et `div(0, 0)` lèvent `ZeroDivisionError`.
- Logique de branche incorrecte quand `a <= b` : `div(2, 10)` renvoie 5, alors que
  `a // b` donnerait 0 (comportement attendu supposé, à confirmer).

Les autres méthodes (`add`, `substract`, `mul`) ne contiennent aucun bug connu.

## IPv4_valid.py — `is_valid_IPv4`

- `return` placé dans la boucle `for` : seul le premier octet est vérifié.
  `"1.999.1.1"` et `"1.2.3."` sont acceptés à tort.
- `int()` lève `ValueError` sur une entrée non numérique (`"a.b.c.d"`) au lieu de
  renvoyer `False`.
- `int()` accepte des formes non conformes : `" 1"`, `"+1"`, `"1_0"`.
- Zéros en tête (`"01.1.1.1"`) acceptés : à décider si c'est un défaut.
- Docstring inexacte : elle annonce « octets < 255 » alors que 255 est valide
  (le code est correct sur ce point, pas la documentation).

## primes.py — `is_prime`

- Aucun bug connu (témoin sans bug). Vérifiée contre une version naïve sur les
  entiers de -5 à 199 999 : aucun écart.
- Limite théorique, non démontrée : `int(num ** 0.5)` peut être imprécis sur de
  très grands entiers (`math.isqrt` est plus sûr).
