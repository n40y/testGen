# Fichiers contenant un test, exécuté comme témoin de fonctionnement.

class Calcul:
    """
    Classe simulent une calculatrice basique.
    """
    
    def add(self, a: int, b: int) -> int:
        return a + b
    
    def substract(self, a: int, b: int) -> int:
        return a  - b
    
    def mul(self, a: int, b: int) -> int:
        return a * b
    
    # Cette fonction comporte une erreur.
    # Pas de 'edge cases' pour la division par zéro.
    def div(self, a: int, b: int) -> int:
        if a > b:
            return a // b
        return b // a
