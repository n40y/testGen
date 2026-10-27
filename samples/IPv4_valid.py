# Fichiers contenant un test, exécuté comme témoin de fonctionnement.

def is_valid_IPv4(ip: str) -> bool:
    """
    Vérifie si une adresse IP à un format valide:
    - Comporte 4 octets distincts.
    - Octets < 255.
    """
    if not ip:
        return False
    
    ip_split = ip.split('.')
    
    if len(ip_split) != 4:
        return False
    
    # Si le bit 8 est différent de 0, alors l'octet est supérieur
    # à 255. La fonction retourne False.
    for octet in ip_split:
        n = int(octet)
        return n >= 0 and (n >> 8) == 0
    return True