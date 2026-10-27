# Fonctions corrects, contenant méthodes liées aux réseaux.

def ipv4_to_int(ip: str) -> int:
    parts = ip.split('.')
    if len(parts) != 4:
        raise ValueError("Invalid IP format.")
    
    octets = []
    for x in parts:
        try:
            val = int(x)
        except ValueError:
            raise ValueError("Invalid IP in input.")
        
        if val < 0 or val > 255:
            raise ValueError("Invalid IP in input.")
        octets.append(val)
        
    a, b, c, d = octets
    
    return (a << 24) | (b << 16) | (c << 8) | d


def cidr_contains(cidr_str: str, ip: str) -> bool:
    if '/' not in cidr_str:
        raise ValueError("Invalid CIDR format (missing '/').")
    
    net_ip, prefix_str = cidr_str.split('/')
    prefix = int(prefix_str)
    
    if not (0 <= prefix <= 32):
        raise ValueError("Invalid CIDR prefix.")
        
    def to_int(addr: str) -> int:
        parts = list(map(int, addr.split('.')))
        return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]
    
    ip_int = to_int(ip)  
    net_int = to_int(net_ip)
    
    mask = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
    
    return (ip_int & mask) == (net_int & mask)


def is_private(ip: str) -> bool:
    from ipaddress import ip_address
    
    try:
        return ip_address(ip).is_private
    except ValueError:
        return False
    
    