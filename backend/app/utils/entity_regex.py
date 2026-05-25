"""Regex-based entity extraction helpers."""

import re
from typing import TypedDict


class ExtractedEntities(TypedDict):
    emails: list[str]
    usernames: list[str]
    urls: list[str]
    domains: list[str]
    phone_numbers: list[str]
    wallet_addresses: list[str]


EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
URL_RE = re.compile(
    r"https?://[^\s<>\"']+|www\.[^\s<>\"']+",
    re.IGNORECASE,
)
DOMAIN_RE = re.compile(
    r"(?<![@/])(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}(?![\w/])",
)
PHONE_RE = re.compile(r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{2,4}\)?[-.\s]?\d{3,4}[-.\s]?\d{3,4}")
USERNAME_RE = re.compile(r"(?<![\w@])(?:@|u/|user:)\s*([A-Za-z0-9_.-]{3,32})", re.IGNORECASE)
WALLET_RE = re.compile(
    r"\b(?:0x[a-fA-F0-9]{40}|bc1[a-zA-HJ-NP-Z0-9]{25,90}|[13][a-km-zA-HJ-NP-Z1-9]{25,34}|T[A-Za-z1-9]{33})\b"
)


def extract_entities_regex(text: str) -> ExtractedEntities:
    emails = list(dict.fromkeys(EMAIL_RE.findall(text)))
    urls = list(dict.fromkeys(URL_RE.findall(text)))
    domains_from_urls = []
    for url in urls:
        clean = url.replace("https://", "").replace("http://", "").replace("www.", "")
        host = clean.split("/")[0].split("?")[0]
        if host:
            domains_from_urls.append(host)
    domains = list(
        dict.fromkeys(
            domains_from_urls
            + [d for d in DOMAIN_RE.findall(text) if d not in emails and "@" not in d]
        )
    )
    usernames = list(dict.fromkeys(m.group(1) if m.lastindex else m.group(0) for m in USERNAME_RE.finditer(text)))
    phones = list(dict.fromkeys(PHONE_RE.findall(text)))
    wallets = list(dict.fromkeys(WALLET_RE.findall(text)))
    return {
        "emails": emails,
        "usernames": usernames,
        "urls": urls,
        "domains": domains,
        "phone_numbers": phones,
        "wallet_addresses": wallets,
    }
