# Fonctions binaires sans erreurs.

def popcount(n: int) -> int:
    count = 0
    while n > 0:
        count += (n & 1)
        n >>= 1
    return count


def is_power_of_two(n: int) -> bool:
    if n <= 0:
        return False 
    return (n & (n - 1)) == 0


def get_bit(value: int, position: int) -> int:
    return (value >> position) & 1


def to_binary(n: int, width: int) -> str:
    if n < 0 or n >= (1 << width):
        raise ValueError("n does not fit into width.")
    
    return f"{n:{width}b}"


def from_binary(s: str) -> int:
    if not s:
        raise ValueError("Empty input.")
    
    for x in s:
        if x not in ('0', '1'):
            raise ValueError("invalid character in binary string.")
    
    return int(s, 2)


def bytes_to_hex(data: bytes) -> bytes:
    from binascii import hexlify
    return hexlify(data)


def xor_bytes(a: bytes, b: bytes) -> bytes:
    if len(a) != len(b):
        raise ValueError("The inputs have differents lengths.")
    
    result = bytes(x ^ y for x, y in zip(a, b))
    return result


def checksum8(data: bytes) -> int:
    sum_byte = 0
    for byte in data:
        sum_byte = (sum_byte + byte) % 256
    return sum_byte
