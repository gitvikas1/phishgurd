import re
from urllib.parse import urlparse

SUSPICIOUS_WORDS = [
    "login","verify","update","secure","account","bank","free","click",
    "confirm","urgent","limited","prize","gift","win","signin","wallet",
]

SUSPICIOUS_TLDS = [
    "zip","xyz","top","gq","work","country","kim","men","loan","lol",
    "support","trade","party","link","click","fit","tk","ml","cf"
]

ip_regex = re.compile(
    r"^(?:\d{1,3}\.){3}\d{1,3}$"  # IPv4 (simple)
)

def has_ip(host):
    return bool(ip_regex.match(host))

def count_chars(s, chars):
    return sum(1 for ch in s if ch in chars)

def extract_url_features(url: str):
    # Ensure scheme so urlparse behaves
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+\-.]*://", url):
        url = "http://" + url
    parsed = urlparse(url)

    host = parsed.hostname or ""
    path = parsed.path or ""
    query = parsed.query or ""
    full = parsed.geturl()

    # Features
    url_length = len(full)
    host_length = len(host)
    path_length = len(path)
    num_digits = sum(ch.isdigit() for ch in full)
    num_special = count_chars(full, "@-_?&#%=:;~$+!*',()[]{}")
    num_dots = host.count(".")
    uses_https = 1 if parsed.scheme == "https" else 0
    contains_ip = 1 if has_ip(host) else 0
    has_at = 1 if "@" in full else 0
    has_hyphen = 1 if "-" in host else 0
    has_port = 1 if parsed.port else 0
    subdomain_count = max(0, num_dots - 1)
    has_hex = 1 if re.search(r"%[0-9a-fA-F]{2}", full) else 0
    many_slashes = 1 if full.count("/") > 5 else 0
    suspicious_words = sum(1 for w in SUSPICIOUS_WORDS if w in full.lower())
    tld = host.split(".")[-1].lower() if "." in host else ""
    suspicious_tld = 1 if tld in SUSPICIOUS_TLDS else 0

    return [
        url_length, host_length, path_length, num_digits, num_special,
        num_dots, uses_https, contains_ip, has_at, has_hyphen, has_port,
        subdomain_count, has_hex, many_slashes, suspicious_words, suspicious_tld
    ]
