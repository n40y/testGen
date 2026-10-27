# Fichiers contenant un test, exécuté comme témoin de fonctionnement.


def is_prime(num: int) -> bool:
    """
    Return true if variable num is a prime number.
    """
    if num <= 1: return False
    if num in (2, 3): return True
    if (num & 1) == 0 or num % 3 == 0: return False
    
    sqrt = int(num ** 0.5)
    
    for x in range(5, sqrt + 1, 6):
        if num % x == 0 or num % (x + 2) == 0:
            return False
    return True