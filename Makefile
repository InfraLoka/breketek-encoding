PYTHON  := python3
VENV    := .venv
BIN     := $(VENV)/bin
PIP     := $(BIN)/pip
RUN     := $(BIN)/python breketek.py

.DEFAULT_GOAL := help

# ── Setup ─────────────────────────────────────────────────────────────────────

$(VENV)/bin/activate: requirements.txt
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip -q
	$(PIP) install -r requirements.txt -q
	@touch $(VENV)/bin/activate

.PHONY: setup
setup: $(VENV)/bin/activate  ## Create venv and install dependencies
	@echo "✓ venv ready — use 'make encode ENCODER=breketek TEXT=...'"

# ── Run ───────────────────────────────────────────────────────────────────────
# Usage:
#   make encode TEXT="some words"         — inline text
#   make encode FILE=input.txt            — from file
#   make encode FILE=input.txt ENCODER=rot13
#   echo "piped" | make encode            — from stdin (no TEXT or FILE needed)

_ENCODER := $(or $(ENCODER),breketek)
_INPUT   := $(if $(FILE),--file $(FILE),$(if $(TEXT),"$(TEXT)",))

.PHONY: encode
encode: setup  ## Encode TEXT or FILE with ENCODER (default: breketek)
	$(RUN) encode $(_ENCODER) $(_INPUT)

.PHONY: decode
decode: setup  ## Decode TEXT or FILE with ENCODER (default: breketek)
	$(RUN) decode $(_ENCODER) $(_INPUT)

.PHONY: list
list: setup  ## List all available encoders
	$(RUN) list

.PHONY: test
test: setup  ## Run end-to-end test suite
	$(BIN)/pytest tests/ -v

# ── Cleanup ───────────────────────────────────────────────────────────────────

.PHONY: clean
clean:  ## Remove venv
	rm -rf $(VENV)

# ── Help ──────────────────────────────────────────────────────────────────────

.PHONY: help
help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*##"}; {printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2}'
