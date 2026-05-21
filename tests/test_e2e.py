"""End-to-end tests for the breketek CLI.

All tests invoke the script via subprocess using the venv Python, so they
exercise the full stack: argument parsing → encoding/decoding → output.
"""

from __future__ import annotations

import subprocess
import tempfile
import os
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

ROOT = Path(__file__).parent.parent
PYTHON = str(ROOT / ".venv" / "bin" / "python")
SCRIPT = str(ROOT / "breketek.py")


def cli(*args: str, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        [PYTHON, SCRIPT, *args],
        capture_output=True,
        text=True,
        input=stdin,
        cwd=str(ROOT),
    )


def encode(encoder: str, text: str) -> str:
    return cli("encode", encoder, text).stdout.strip()


def decode(encoder: str, text: str) -> str:
    return cli("decode", encoder, text).stdout.strip()


# ---------------------------------------------------------------------------
# list command
# ---------------------------------------------------------------------------


class TestList:
    def test_shows_all_encoders(self):
        r = cli("list")
        assert r.returncode == 0
        for name in ("breketek", "rot13", "rot47", "base64", "reverse"):
            assert name in r.stdout

    def test_shows_sastrawi_status(self):
        r = cli("list")
        assert "Sastrawi" in r.stdout

    def test_shows_nltk_status(self):
        r = cli("list")
        assert "NLTK" in r.stdout


# ---------------------------------------------------------------------------
# breketek encoder
# ---------------------------------------------------------------------------


class TestBrckEncoder:
    """Breketek is intentionally lossy: inflected words decode to their stems."""

    # --- encode ---

    def test_encode_appends_tek_suffix(self):
        out = encode("breketek", "prabowo gitu siapa")
        assert out == "prabowoketek gitutek siapatek"

    def test_encode_stems_inflected_words(self):
        # berlari → stem lari → lariketek
        # bersama → stem sama → samatek
        out = encode("breketek", "berlari bersama")
        assert out == "lariketek samatek"

    def test_encode_preserves_capitalisation(self):
        out = encode("breketek", "Prabowo gitu Siapa")
        assert out.startswith("Prabowo")  # capital preserved after suffix
        assert "Siapa" in out

    def test_encode_preserves_punctuation(self):
        out = encode("breketek", "merdeka!")
        assert out.endswith("!")

    def test_encode_preserves_newlines(self):
        r = cli("encode", "breketek", "lari\npantai")
        assert "\n" in r.stdout

    def test_encode_preserves_numbers(self):
        out = encode("breketek", "ada 3 teman")
        assert "3" in out

    def test_encode_suffix_alternates_ketek_tek(self):
        # index 0 → ketek, index 1 → tek, index 2 → tek
        out = encode("breketek", "prabowo gitu siapa")
        parts = out.split()
        assert parts[0].endswith("ketek")
        assert parts[1].endswith("tek")
        assert parts[2].endswith("tek")

    # --- decode ---

    def test_decode_strips_tek_suffix(self):
        out = decode("breketek", "gitutek siapatek")
        assert out == "gitu siapa"

    def test_decode_strips_ketek_suffix(self):
        out = decode("breketek", "prabowoketek")
        assert out == "prabowo"

    def test_decode_preserves_punctuation(self):
        out = decode("breketek", "merdekaketek!")
        assert out.endswith("!")

    def test_decode_preserves_capitalisation(self):
        out = decode("breketek", "Prabowoketek gitutek")
        assert out.startswith("P")

    # --- round-trip (stable stems only) ---

    def test_round_trip_already_stemmed_words(self):
        # Words already in root form → encode/decode is lossless
        text = "prabowo gitu siapa"
        assert decode("breketek", encode("breketek", text)) == text

    def test_round_trip_is_stable(self):
        # Second encode→decode produces the same result as the first
        text = "berlari ke pantai"
        once = decode("breketek", encode("breketek", text))
        twice = decode("breketek", encode("breketek", once))
        assert once == twice

    def test_round_trip_inflected_returns_stem(self):
        # berlari → encodes as lariketek → decodes as lari (stem, not berlari)
        out = decode("breketek", encode("breketek", "berlari"))
        assert out == "lari"


# ---------------------------------------------------------------------------
# ROT-13
# ---------------------------------------------------------------------------


class TestRot13:
    def test_encode(self):
        assert encode("rot13", "Hello") == "Uryyb"

    def test_decode_is_same_as_encode(self):
        assert decode("rot13", "Uryyb") == "Hello"

    def test_round_trip(self):
        text = "UU ITE bug report #001"
        assert decode("rot13", encode("rot13", text)) == text

    def test_non_alpha_unchanged(self):
        assert encode("rot13", "123!@#") == "123!@#"


# ---------------------------------------------------------------------------
# ROT-47
# ---------------------------------------------------------------------------


class TestRot47:
    def test_encode(self):
        out = encode("rot47", "Hello")
        assert out != "Hello"
        assert len(out) == len("Hello")

    def test_round_trip(self):
        text = "berlari ke pantai bersama 3 teman!"
        assert decode("rot47", encode("rot47", text)) == text

    def test_whitespace_unchanged(self):
        out = encode("rot47", "a b")
        assert out[1] == " "


# ---------------------------------------------------------------------------
# Base64
# ---------------------------------------------------------------------------


class TestBase64:
    def test_encode(self):
        assert encode("base64", "hello") == "aGVsbG8="

    def test_decode(self):
        assert decode("base64", "aGVsbG8=") == "hello"

    def test_round_trip(self):
        text = "rahasia negara UU ITE"
        assert decode("base64", encode("base64", text)) == text

    def test_invalid_input_exits_nonzero(self):
        r = cli("decode", "base64", "!!!not_base64!!!")
        assert r.returncode != 0
        assert "Error" in r.stderr


# ---------------------------------------------------------------------------
# Reverse
# ---------------------------------------------------------------------------


class TestReverse:
    def test_encode(self):
        assert encode("reverse", "abcd") == "dcba"

    def test_round_trip(self):
        text = "prabowo merdeka"
        assert decode("reverse", encode("reverse", text)) == text


# ---------------------------------------------------------------------------
# Input modes
# ---------------------------------------------------------------------------


class TestInputModes:
    # --- inline text ---

    def test_inline_text(self):
        r = cli("encode", "rot13", "hello")
        assert r.returncode == 0
        assert r.stdout.strip() == "uryyb"

    # --- stdin ---

    def test_stdin_pipe(self):
        r = cli("encode", "rot13", stdin="hello")
        assert r.returncode == 0
        assert r.stdout.strip() == "uryyb"

    def test_stdin_multiline(self):
        r = cli("encode", "rot13", stdin="hello\nworld")
        assert r.returncode == 0
        assert "uryyb" in r.stdout
        assert "jbeyq" in r.stdout

    # --- file ---

    def test_file_input(self, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text("hello world", encoding="utf-8")
        r = cli("encode", "rot13", "--file", str(f))
        assert r.returncode == 0
        assert r.stdout.strip() == "uryyb jbeyq"

    def test_file_input_short_flag(self, tmp_path):
        f = tmp_path / "input.txt"
        f.write_text("hello", encoding="utf-8")
        r = cli("encode", "rot13", "-f", str(f))
        assert r.returncode == 0
        assert r.stdout.strip() == "uryyb"

    def test_file_multiline(self, tmp_path):
        f = tmp_path / "multiline.txt"
        f.write_text("prabowo\ngitu\nsiapa", encoding="utf-8")
        r = cli("encode", "breketek", "--file", str(f))
        assert r.returncode == 0
        lines = r.stdout.strip().splitlines()
        assert len(lines) == 3

    def test_file_breketek_round_trip(self, tmp_path):
        src = tmp_path / "src.txt"
        src.write_text("prabowo gitu siapa", encoding="utf-8")
        encoded = cli("encode", "breketek", "--file", str(src)).stdout.strip()
        enc_file = tmp_path / "enc.txt"
        enc_file.write_text(encoded, encoding="utf-8")
        decoded = cli("decode", "breketek", "--file", str(enc_file)).stdout.strip()
        assert decoded == "prabowo gitu siapa"

    def test_file_base64_round_trip(self, tmp_path):
        src = tmp_path / "src.txt"
        src.write_text("rahasia negara", encoding="utf-8")
        encoded = cli("encode", "base64", "--file", str(src)).stdout.strip()
        assert decode("base64", encoded) == "rahasia negara"


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


class TestErrors:
    def test_missing_file_exits_nonzero(self):
        r = cli("encode", "rot13", "--file", "/nonexistent/file.txt")
        assert r.returncode != 0
        assert "Error" in r.stderr

    def test_no_input_exits_nonzero(self):
        # No TEXT, no --file, no stdin — should error
        r = subprocess.run(
            [PYTHON, SCRIPT, "encode", "rot13"],
            capture_output=True,
            text=True,
            stdin=subprocess.DEVNULL,
            cwd=str(ROOT),
        )
        assert r.returncode != 0

    def test_invalid_encoder_exits_nonzero(self):
        r = cli("encode", "nonexistent", "hello")
        assert r.returncode != 0

    def test_invalid_base64_decode(self):
        r = cli("decode", "base64", "not!valid!base64!!!")
        assert r.returncode != 0
