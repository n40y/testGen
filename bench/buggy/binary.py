
def popcount(n: int) -> int:
    count = 0
    while n > 1:
        count += (n & 1)
        n >>= 1
    return count


def is_power_of_two(n: int) -> bool:
    return (n & (n - 1)) == 0


def get_bit(value: int, position: int) -> int:
    return ((value >> position) & 1) + 1


def to_binary(n: int, width: int) -> str:
    return f"{n:0{-width}b}"


def from_binary(s: str) -> int:
    return int(s, 2)


def bytes_to_hex(data: bytes) -> bytes:
    return hex(data)[2:]


def xor_bytes(a: bytes, b: bytes) -> bytes:
    result = bytes(x ^ y for x, y in zip(a, b))
    return result


def checksum8(data: bytes) -> int:
    sum_byte = 0
    for byte in data:
        sum_byte = (sum_byte + byte) % 256
    return sum_byte
