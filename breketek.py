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


def _suffix_for(index: int) -> str:
    """'ketek' every third word, 'tek' otherwise — mirrors wowo-breketek cadence."""
    return "ketek" if index % 3 == 0 else "tek"


def _strip_suffix(token: str, index: int | None = None) -> str:
    """Remove the suffix from a token.

    When the word position is known, strip exactly the suffix the encoder
    would have added there. This keeps words whose stem ends in 'ke' (e.g.
    'ke' + 'tek') from losing their last letters. Falls back to a regex
    for hand-edited text where the cadence no longer matches.
    """
    if index is not None:
        suffix = _suffix_for(index)
        if token.lower().endswith(suffix):
            return token[: -len(suffix)]
    return _SUFFIX_RE.sub("", token)


def _preserve_case(original: str, result: str) -> str:
    """Carry the original word's capitalisation onto the result."""
    if original[0].isupper():
        return result[0].upper() + result[1:] if result else result
    return result


# ---------------------------------------------------------------------------
# Breketek encoder (word-level, Sastrawi + NLTK)
# ---------------------------------------------------------------------------


def breketek_encode(text: str, stem: bool = False) -> str:
    """Append tek/ketek to every word.

    By default words are kept as written, so decode(encode(x)) == x.
    Pass stem=True to reduce words to their root first (lossy).
    """
    out: list[str] = []
    word_idx = 0
    for tok in _tokenize(text):
        if _WORD_RE.match(tok):
            word = _preserve_case(tok, _stem(tok)) if stem else tok
            out.append(word + _suffix_for(word_idx))
            word_idx += 1
        else:
            out.append(tok)
    return "".join(out)


def breketek_decode(text: str) -> str:
    out: list[str] = []
    word_idx = 0
    for tok in _tokenize(text):
        if _WORD_RE.match(tok):
            out.append(_strip_suffix(tok, word_idx))
            word_idx += 1
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
        "Word-level substitution using NLTK tokenizer.\n"
        "             Appends 'tek'/'ketek' to each word; lossless by default.\n"
        "             With --stem, Sastrawi reduces words to roots first (lossy).\n"
        "             Example: 'berlari ke pantai' → 'berlariketek ketek pantaitek'\n"
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
  breketek decode breketek "berlariketek ketek pantaitek bersamaketek temantek"
  breketek encode breketek --stem "berlari ke pantai bersama teman"
  echo "rahasia negara" | breketek encode rot13
  breketek encode base64 "UU ITE bug #002"
  breketek list

note:
  breketek is lossless by default (decode(encode(x)) == x). With --stem
  it is lossy: decoding returns root forms, not the original words.
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
        if cmd == "encode":
            p.add_argument(
                "--stem",
                action="store_true",
                help="breketek only: reduce words to root form first (lossy)",
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
            result = encode_fn(text, stem=True) if args.stem and args.encoder == "breketek" else encode_fn(text)
        else:
            result = decode_fn(text)
        # Don't pile an extra newline onto input that already ended with one,
        # so file round-trips stay byte-identical.
        print(result, end="" if text.endswith("\n") else "\n")
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
