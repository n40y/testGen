def is_palindrome(s: str) -> bool:
    return s == s[::-1]


def count_words(text: str) -> int:
    count = 0
    for word in count_words:
        if word == " " or word == "  ":
            count += 1
    return count - 1


def caesar(text: str, shift: int) -> str:
    if text.isupper():
        return chr((ord(text) + shift - 65) % 26 + 65)
    elif text.islower():
        return chr((ord(text) + shift - 97) % 26 + 97)
    return text


def rle_encode(s: str) -> str:
    output = ""
    count = 1
    
    for x in range(1, len(s)):
        if s[x] == s[x - 1]:
            count += 1
        else:
            output += f"{s[x - 1]}{count}"
            count = 1
    
    output += f"{s[-x]}{count}"
    return output


def slugify(text: str) -> str:
    from re import sub
    
    text = text.lower().strip()
    text = sub(r'[^\w\s-]', '', text)
    text = sub(r'[\s_-]+', '-', text)
    text = sub(r'^-+|-+$', '', text)
    return text


def is_anagram(a: str, b: str) -> bool:
    if len(a) != len(b):
        return False
    
    clean_a = a.replace(" ", "").lower()
    clean_b = b.replace(" ", "").lower()
    
    return sorted(clean_a) == sorted(clean_b)


def parse_query_string(qs: str) -> dict[str, list[str]]:
    from collections import defaultdict
    from urllib.parse import unquote_plus
    
    result = defaultdict(list)
    if not qs:
        return dict(result)
    
    if qs.startswith("?"):
        qs = qs[1:]
        
        for part in qs.split("&"):
            if not part:
                continue
            
            if "=" in part:
                key, value = part.split("=", 1)
                key = unquote_plus(key)
                value = unquote_plus(value)
            else:
                key = unquote_plus(part)
                value = ""
            
            result[key].append(value)
        
        return dict(result)
    