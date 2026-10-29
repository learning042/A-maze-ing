MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

MYPY_STRICT = --strict

MAIN = main.py

PKG_MANAGER ?= uv

PYTHON ?= python3.10

VENV_NAME ?= venv

CONFIG_FILE ?= config.txt

install:
	@if  [ "$(PKG_MANAGER)" = "uv" ]; then \
		$(PKG_MANAGER) sync; \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PKG_MANAGER) install -r requirements.txt; \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
	fi
	
run:
	@if [ "$(PKG_MANAGER)" = "uv" ]; then \
		uv run $(MAIN) $(CONFIG_FILE); \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PYTHON) $(MAIN) $(CONFIG_FILE); \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
	fi
debug:
	@if [ "$(PKG_MANAGER)" = "uv" ]; then \
		uv run $(PYTHON) -m pdb $(MAIN); \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PYTHON) -m pdb $(MAIN); \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
	fi

venv: 
	$(PYTHON) -m venv $(VENV_NAME)

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +

lint:
	flake8 --extend-exclude=./$(VENV_NAME) .
	mypy . $(MYPY_FLAGS) --exclude '(^|/)$(VENV_NAME)/'

lint-strict:
	flake8 --extend-exclude=./$(VENV_NAME) .
	mypy . $(MYPY_STRICT) --exclude '(^|/)$(VENV_NAME)/'

.PHONY: install run debug venv clean lint lint-strict
