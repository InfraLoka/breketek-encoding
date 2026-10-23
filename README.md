# breketek-encoding

A Python CLI for encoding and decoding text using multiple methods, including **breketek** — a word-level substitution cipher powered by [NLTK](https://www.nltk.org/) tokenization, with optional [Sastrawi](https://github.com/har07/PySastrawi) Indonesian stemming.

Inspired by the split-key encryption edge cases discussed in `docs.md` (UU ITE Bug #002): when a message and its meaning live in different places, who bears the burden of proving what it says?

---

## Requirements

- Python 3.9+
- `make`

All Python dependencies are managed inside a local virtual environment (`.venv`). No system-wide installs needed.

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/your-org/breketek-encoding.git
cd breketek-encoding

# 2. Set up venv + install deps
make setup

# 3. Encode something
make encode TEXT="Prabowo gitu siapa ya merdeka"
# → Prabowoketek gitutek siapatek yaketek merdekatek

# (add --stem to reduce words to roots first; lossy)

# 4. Decode it back
make decode TEXT="Prabowoketek gitutek siapatek yaketek merdekatek"
# → Prabowo gitu siapa ya merdeka
```

---

## Encoders

### `breketek` (default)

Word-level substitution cipher using **NLTK** for tokenization. Each word is suffixed with `tek` or `ketek` in a fixed cadence — mirroring the *wowo-breketek* speech style. Optionally, **Sastrawi** can reduce words to their Indonesian root form first (`--stem`).

```
berlari ke pantai bersama teman
→ berlariketek ketek pantaitek bersamaketek temantek
```

With `--stem`:

```
berlari ke pantai bersama teman
→ lariketek ketek pantaitek samaketek temantek
```

**Behavior:**
- Words are kept exactly as written by default; pass `--stem` to reduce them to roots first (`berlari` → `lari`)
- Every 3rd word gets `ketek`, the rest get `tek`; decoding strips exactly the suffix expected at each word position, so words ending in `ke` survive
- Punctuation, numbers, and whitespace pass through unchanged
- Capitalisation is preserved exactly (`KawalIbam`, `UU`, `KOST`)
- **Lossless by default** — `decode(encode(x)) == x`. With `--stem` encoding is lossy: decoding returns the stemmed root, not the original inflected form.

### `rot13`

ROT13 letter substitution. Shifts each letter by 13. Symmetric — encode and decode are the same operation.

```
UU ITE Bug #001  →  HH VGR Oht #001
```

### `rot47`

ROT47 shifts all printable ASCII characters (codes 33–126) by 47. Symmetric.

```
Hello, World!  →  w6==@[ (@C=5P
```

### `base64`

Standard Base64 encoding and decoding.

```
rahasia negara  →  cmFoYXNpYSBuZWdhcmE=
```

### `reverse`

Reverses the input string. Symmetric.

```
prabowo merdeka  →  akedrем owowabarp
```

---

## Text file support

Both the CLI and `make` targets accept a plain `.txt` file (or any UTF-8 text file) as input via the `-f` / `--file` flag. The entire file content — including newlines — is processed as one body of text.

### Encode a file

```bash
# CLI
.venv/bin/python breketek.py encode breketek --file input.txt
.venv/bin/python breketek.py encode breketek -f input.txt      # short flag

# make
make encode FILE=input.txt
make encode FILE=input.txt ENCODER=base64
```

### Decode a file

```bash
# CLI
.venv/bin/python breketek.py decode breketek --file encoded.txt
.venv/bin/python breketek.py decode breketek -f encoded.txt

# make
make decode FILE=encoded.txt
make decode FILE=encoded.txt ENCODER=rot13
```

### Save output to a file

Redirect stdout to write the result to a new file:

```bash
.venv/bin/python breketek.py encode breketek --file input.txt > encoded.txt
.venv/bin/python breketek.py decode breketek --file encoded.txt > decoded.txt

# make
make encode FILE=input.txt > encoded.txt
```

### Full encode → decode pipeline

```bash
# encode a document, save it, then decode it back
.venv/bin/python breketek.py encode breketek -f article.txt > article.enc.txt
.venv/bin/python breketek.py decode breketek -f article.enc.txt > article.dec.txt
```

### Multiline files

Newlines and whitespace are preserved. Each line is processed independently — punctuation and line breaks pass through unchanged, only word tokens are encoded.

```
# input.txt
Prabowo gitu siapa
berlari ke pantai
merdeka!
```

```bash
.venv/bin/python breketek.py encode breketek -f input.txt
```

```
# output
Prabowoketek gitutek siapatek
lariketek ketek pantaitek
merdekaketek!
```

### Input priority

When multiple input sources are provided, the tool uses this order of precedence:

| Priority | Source | How |
|----------|--------|-----|
| 1 | `--file` / `-f` | `--file path/to/file.txt` |
| 2 | Inline text | `"some text"` as positional argument |
| 3 | Stdin | `cat file.txt \| breketek encode breketek` |

---

## Real-world example

The following is an example of the type of content discussed in `docs.md` — text that could be considered defamatory under UU ITE Pasal 27 Ayat (3), where the meaning depends on how and by whom it is read. This demonstrates how breketek encoding creates the *split-key ambiguity* from Bug #002: the encoded form is meaningless without the decoder, and the decoded form returns the original text exactly (or stemmed roots, if encoded with `--stem`).

**Original text (plaintext):**

```
Subfomo khusus buat ngomongin Rahmat Wibowo: kumpulan bukti kejahatan, perilaku,
progress hukum dan sebagainya. Rahmat Wibowo adalah alumni ITB, masuk ITB di tahun
2019. Di tahun 2023, dia dipecat AWS dan di tahun 2026 dia lepas kendali dan meneror
orang2 yang tidak sepaham dengannya. Bagi yang memiliki bukti terkait kasus Rahmat
Wibowo, bisa dikirim secara DM ke akun fomo dengan username *@awas* atau dipost di
subfomo ini. Bukti berupa Screen Record lebih kuat di pengadilan dibanding hanya
sekedar screenshoot
```

**Encoded (breketek):**

```bash
.venv/bin/python breketek.py encode breketek -f example/subfomo_rahmat_wibowo.txt
# or
make encode FILE=example/subfomo_rahmat_wibowo.txt
```

```
Subfomoketek khusustek buattek ngomonginketek Rahmattek Wibowotek: kumpulanketek buktitek
kejahatantek, perilakuketek, progresstek hukumtek danketek sebagainyatek. Rahmattek
Wibowoketek adalahtek alumnitek ITBketek, masuktek ITBtek diketek tahuntek 2019. Ditek
tahunketek 2023, diatek dipecattek AWSketek dantek ditek tahunketek 2026 diatek lepastek
kendaliketek dantek menerortek orangketek2 yangtek tidaktek sepahamketek dengannyatek.
Bagitek yangketek memilikitek buktitek terkaitketek kasustek Rahmattek Wibowoketek,
bisatek dikirimtek secaraketek DMtek ketek akunketek fomotek dengantek usernameketek
*@awastek* atautek dipostketek ditek subfomotek iniketek. Buktitek berupatek Screenketek
Recordtek lebihtek kuatketek ditek pengadilantek dibandingketek hanyatek sekedartek
screenshootketek
```

**Decoded back (lossless — identical to the original):**

```
Subfomo khusus buat ngomongin Rahmat Wibowo: kumpulan bukti kejahatan, perilaku, progress hukum dan sebagainya. Rahmat Wibowo adalah alumni ITB, masuk ITB di tahun 2019. Di tahun 2023, dia dipecat AWS dan di tahun 2026 dia lepas kendali dan meneror orang2 yang tidak sepaham dengannya. Bagi yang memiliki bukti terkait kasus Rahmat Wibowo, bisa dikirim secara DM ke akun fomo dengan username *@awas* atau dipost di subfomo ini. Bukti berupa Screen Record lebih kuat di pengadilan dibanding hanya sekedar screenshoot
```

**With `--stem` (lossy):** words are reduced to roots (`kejahatan` → `jahat`, `dipecat` → `pecat`, `pengadilan` → `adil`) and the original cannot be recovered.

This illustrates Bug #002 in practice: the encoded form distributed on a public forum has no legible content without the breketek decoder. In stem mode the decoded form returns roots only, so no single version of the text is the complete, original message; in the default mode the decoder restores it fully. Under UU ITE, the question of whether this constitutes distributing defamatory *Informasi Elektronik* depends on which layer — encoded or decoded — the court treats as the operative text.

---

## Usage

### CLI directly

```bash
.venv/bin/python breketek.py <command> <encoder> [text] [-f FILE] [--stem]   # --stem: encode breketek only
```

| Command | Description |
|---------|-------------|
| `encode ENCODER TEXT` | Encode text |
| `decode ENCODER TEXT` | Decode text |
| `list`                | Show all encoders and their status |

**Input sources** (checked in this order):

| Source | How |
|--------|-----|
| File   | `breketek encode breketek --file input.txt` |
| Inline | `breketek encode breketek "some text"` |
| Stdin  | `echo "some text" \| breketek encode breketek` |

**Examples:**

```bash
# breketek encoder
.venv/bin/python breketek.py encode breketek "berlari ke pantai"
.venv/bin/python breketek.py decode breketek "lariketek ketek pantaitek"

# from a file
.venv/bin/python breketek.py encode breketek --file docs.md
.venv/bin/python breketek.py encode base64 -f input.txt

# stdin pipe
cat secret.txt | .venv/bin/python breketek.py encode rot13
echo "cmFoYXNpYSBuZWdhcmE=" | .venv/bin/python breketek.py decode base64

# other encoders
.venv/bin/python breketek.py encode rot13 "UU ITE Bug #001"
.venv/bin/python breketek.py encode rot47 "Hello, World!"
.venv/bin/python breketek.py encode base64 "rahasia negara"
.venv/bin/python breketek.py encode reverse "prabowo merdeka"
.venv/bin/python breketek.py list
```

### Via `make`

```bash
make encode TEXT="Prabowo gitu siapa"          # breketek by default
make encode FILE=docs.md                        # from a file
make encode FILE=input.txt ENCODER=base64       # different encoder + file
make decode TEXT="Prabowoketek gitutek"
make decode FILE=encoded.txt ENCODER=rot13
echo "piped input" | make encode                # stdin
make list
```

---

## Makefile targets

| Target | Description |
|--------|-------------|
| `make setup` | Create `.venv` and install all dependencies |
| `make encode` | Encode using `TEXT=`, `FILE=`, or stdin; `ENCODER=` optional |
| `make decode` | Decode using `TEXT=`, `FILE=`, or stdin; `ENCODER=` optional |
| `make list` | List available encoders |
| `make test` | Run the full end-to-end test suite |
| `make clean` | Remove `.venv` |
| `make help` | Show all targets |

---

## Tests

46 end-to-end tests covering all encoders, all input modes, and error handling:

```bash
make test
```

```
tests/test_e2e.py::TestList::test_shows_all_encoders        PASSED
tests/test_e2e.py::TestBrckEncoder::test_encode_appends_tek_suffix  PASSED
tests/test_e2e.py::TestBrckEncoder::test_encode_stem_flag_stems_inflected_words PASSED
tests/test_e2e.py::TestBrckEncoder::test_round_trip_is_stable        PASSED
tests/test_e2e.py::TestInputModes::test_file_breketek_round_trip     PASSED
...
46 passed in ~6s
```

Test groups:

| Group | What it covers |
|-------|----------------|
| `TestList` | `list` command output and dependency status |
| `TestBrckEncoder` | encode, decode, round-trip, stemming, suffix pattern, capitalisation |
| `TestRot13` | symmetric round-trip, non-alpha passthrough |
| `TestRot47` | symmetric round-trip, whitespace passthrough |
| `TestBase64` | encode, decode, round-trip, invalid input error |
| `TestReverse` | encode, round-trip |
| `TestInputModes` | inline text, `--file`, `-f`, stdin, multiline |
| `TestErrors` | missing file, empty stdin, invalid encoder, bad base64 |

---

## Project structure

```
breketek-encoding/
├── breketek.py          # CLI + all encoders
├── Makefile             # setup, encode, decode, test, clean
├── requirements.txt     # PySastrawi, nltk, pytest
├── pyrightconfig.json   # Pyright venv path
├── .vscode/
│   └── settings.json    # VS Code interpreter → .venv
├── example/
│   └── subfomo_rahmat_wibowo.txt  # real-world UU ITE example text
├── tests/
│   └── test_e2e.py      # 46 end-to-end tests
├── docs.md              # UU ITE encryption edge-case article (inspiration)
└── LICENSE
```

---

## Dependencies

| Package | Purpose |
|---------|---------|
| [PySastrawi](https://github.com/har07/PySastrawi) | Indonesian stemmer — used only with `--stem` |
| [NLTK](https://www.nltk.org/) | `RegexpTokenizer` — splits text into word and non-word tokens |
| [pytest](https://pytest.org) | Test runner |

Install all at once:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

---

## Background

The `breketek` encoder takes its name and style from *wowo-breketek* — an Indonesian internet speech pattern where words are suffixed with `tek` or `ketek`, popularised by references to figures like Prabowo ("prabowotek"). The encoder uses Sastrawi to strip Indonesian morphological affixes before applying the suffix, making the output more linguistically grounded than a simple string append.

The project was also inspired by `docs.md`, which analyses two legal edge cases in UU ITE (Indonesia's electronic information law): foreign-language ambiguity (Bug #001) and split-key encryption (Bug #002). The breketek encoder embodies Bug #002 — a message whose meaning requires a separate key (the decoder) to recover, and which is lossy when `--stem` is used.

---

## License

See [LICENSE](LICENSE).
