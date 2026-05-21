#!/usr/bin/env python3
"""breketek-encoding: CLI encode/decode tool with Indonesian NLP support."""

from __future__ import annotations

import argparse
import base64
import re
import sys

# ---------------------------------------------------------------------------
# Optional NLP dependencies — graceful degradation if not installed
# ---------------------------------------------------------------------------

try:
    from Sastrawi.Stemmer.StemmerFactory import StemmerFactory as _SF

    _stemmer = _SF().create_stemmer()
    SASTRAWI_OK = True
except ImportError:
    _stemmer = None  # type: ignore[assignment]
    SASTRAWI_OK = False

try:
    from nltk.tokenize import RegexpTokenizer as _RT

    # Splits into word tokens (letters only) and everything else,
    # preserving whitespace and punctuation for lossless reconstruction.
    _tokenizer = _RT(r"[a-zA-Z]+|[^a-zA-Z]+")
    NLTK_OK = True
except ImportError:
    _tokenizer = None  # type: ignore[assignment]
    NLTK_OK = False

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

_WORD_RE = re.compile(r"^[a-zA-Z]+$")
_SUFFIX_RE = re.compile(r"(ketek|tek)$", re.IGNORECASE)


def _tokenize(text: str) -> list[str]:
    if NLTK_OK and _tokenizer is not None:
        return _tokenizer.tokenize(text)
    # Fallback: same pattern via re
    return re.findall(r"[a-zA-Z]+|[^a-zA-Z]+", text)


def _stem(word: str) -> str:
    if SASTRAWI_OK and _stemmer is not None:
        return _stemmer.stem(word.lower())
    return word.lower()


def _add_suffix(stem: str, index: int) -> str:
    """Append 'ketek' every third word, 'tek' otherwise — mirrors wowo-breketek cadence."""
    suffix = "ketek" if index % 3 == 0 else "tek"
    return stem + suffix


def _strip_suffix(token: str) -> str:
    return _SUFFIX_RE.sub("", token)


def _preserve_case(original: str, result: str) -> str:
    """Carry the original word's capitalisation onto the result."""
    if original[0].isupper():
        return result[0].upper() + result[1:] if result else result
    return result


# ---------------------------------------------------------------------------
# Breketek encoder (word-level, Sastrawi + NLTK)
# ---------------------------------------------------------------------------


def breketek_encode(text: str) -> str:
    tokens = _tokenize(text)
    out: list[str] = []
    word_idx = 0
    for tok in tokens:
        if _WORD_RE.match(tok):
            stem = _stem(tok)
            encoded = _add_suffix(stem, word_idx)
            encoded = _preserve_case(tok, encoded)
            out.append(encoded)
            word_idx += 1
        else:
            out.append(tok)
    return "".join(out)


def breketek_decode(text: str) -> str:
    tokens = _tokenize(text)
    out: list[str] = []
    for tok in tokens:
        if _WORD_RE.match(tok):
            stripped = _strip_suffix(tok.lower())
            out.append(_preserve_case(tok, stripped))
        else:
            out.append(tok)
    return "".join(out)


# ---------------------------------------------------------------------------
# ROT-13
# ---------------------------------------------------------------------------

_ROT13_TABLE = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "NOPQRSTUVWXYZABCDEFGHIJKLMnopqrstuvwxyzabcdefghijklm",
)


def rot13_encode(text: str) -> str:
    return text.translate(_ROT13_TABLE)


rot13_decode = rot13_encode


# ---------------------------------------------------------------------------
# ROT-47
# ---------------------------------------------------------------------------


def rot47_encode(text: str) -> str:
    result = []
    for ch in text:
        code = ord(ch)
        if 33 <= code <= 126:
            result.append(chr(33 + (code - 33 + 47) % 94))
        else:
            result.append(ch)
    return "".join(result)


rot47_decode = rot47_encode


# ---------------------------------------------------------------------------
# Base64
# ---------------------------------------------------------------------------


def b64_encode(text: str) -> str:
    return base64.b64encode(text.encode()).decode()


def b64_decode(text: str) -> str:
    try:
        return base64.b64decode(text.encode()).decode()
    except Exception as exc:
        raise ValueError(f"Invalid base64: {exc}") from exc


# ---------------------------------------------------------------------------
# Reverse
# ---------------------------------------------------------------------------


def reverse_encode(text: str) -> str:
    return text[::-1]


reverse_decode = reverse_encode


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------

ENCODERS: dict[str, tuple] = {
    "breketek": (breketek_encode, breketek_decode),
    "rot13":    (rot13_encode,    rot13_decode),
    "rot47":    (rot47_encode,    rot47_decode),
    "base64":   (b64_encode,      b64_decode),
    "reverse":  (reverse_encode,  reverse_decode),
}

_DESCRIPTIONS = {
    "breketek": (
        "Word-level substitution using Sastrawi stemmer + NLTK tokenizer.\n"
        "             Stems each Indonesian word then appends 'tek'/'ketek'.\n"
        "             Example: 'berlari ke pantai' → 'lariketek keтek pantaitek'\n"
        f"             Sastrawi: {'✓' if SASTRAWI_OK else '✗ (pip install PySastrawi)'}"
        f"  NLTK: {'✓' if NLTK_OK else '✗ (pip install nltk)'}"
    ),
    "rot13":   "ROT13 letter shift (symmetric)",
    "rot47":   "ROT47 printable-ASCII shift (symmetric)",
    "base64":  "Standard Base64 encode / decode",
    "reverse": "Reverses the input string (symmetric)",
}


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="breketek",
        description="breketek-encoding — encode and decode text using various methods.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
examples:
  breketek encode breketek "berlari ke pantai bersama teman"
  breketek decode breketek "lariketek keтek pantaitek bersamaketek temantek"
  echo "rahasia negara" | breketek encode rot13
  breketek encode base64 "UU ITE bug #002"
  breketek list

note:
  breketek encoder is lossy — decoding returns stemmed (root) forms,
  not the original inflected words. This is intentional: it mirrors
  the split-key ambiguity discussed in docs.md.
        """,
    )

    sub = parser.add_subparsers(dest="command", required=True)

    for cmd in ("encode", "decode"):
        p = sub.add_parser(cmd, help=f"{cmd} text using the specified encoder")
        p.add_argument(
            "encoder",
            choices=list(ENCODERS.keys()),
            metavar="ENCODER",
            help=f"encoder to use: {', '.join(ENCODERS.keys())}",
        )
        p.add_argument(
            "text",
            nargs="?",
            help="inline text to process (reads from stdin if omitted)",
        )
        p.add_argument(
            "-f", "--file",
            metavar="PATH",
            help="read input from a file instead of inline text or stdin",
        )

    sub.add_parser("list", help="list all available encoders with their status")

    return parser


def run_list() -> None:
    print("Available encoders:\n")
    for name, desc in _DESCRIPTIONS.items():
        print(f"  {name:<12} {desc}")
    print()


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "list":
        run_list()
        return

    if args.file is not None:
        try:
            with open(args.file, encoding="utf-8") as fh:
                text = fh.read()
        except OSError as exc:
            print(f"Error reading file: {exc}", file=sys.stderr)
            sys.exit(1)
    elif args.text is not None:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
        if not text:
            parser.error("stdin is empty — provide TEXT, --file PATH, or pipe content")
    else:
        parser.error("provide TEXT, --file PATH, or pipe via stdin")

    encode_fn, decode_fn = ENCODERS[args.encoder]

    try:
        if args.command == "encode":
            print(encode_fn(text))
        else:
            print(decode_fn(text))
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
