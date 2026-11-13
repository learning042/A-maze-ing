MYPY_FLAGS = --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs

MYPY_STRICT = --strict

MAIN = main.py

PKG_MANAGER ?= uv

PYTHON ?= python3.10

VENV_NAME ?= venv

CONFIG_FILE ?= config.txt

EXCLUDES = $(VENV_NAME),.venv

MYPY_EXCLUDES = '(^|/)($(VENV_NAME)/|\.venv)/'

RUN = $(if $(filter uv,$(PKG_MANAGER)),uv run,)


install:
	@if [ "$(PKG_MANAGER)" = "uv" ]; then \
		$(PKG_MANAGER) sync; \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PKG_MANAGER) install -r requirements.txt; \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
		exit 1; \
	fi
	
run:
	@if [ "$(PKG_MANAGER)" = "uv" ]; then \
		uv run $(MAIN) $(CONFIG_FILE); \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PYTHON) $(MAIN) $(CONFIG_FILE); \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
		exit 1; \
	fi
debug:
	@if [ "$(PKG_MANAGER)" = "uv" ]; then \
		uv run $(PYTHON) -m pdb $(MAIN); \
	elif [ "$(PKG_MANAGER)" = "pip" ]; then \
		$(PYTHON) -m pdb $(MAIN); \
	else \
		echo "Invalid package manager. Try again with uv or pip"; \
		exit 1;\
	fi

venv: 
	$(PYTHON) -m venv $(VENV_NAME)

clean:
	find . -name "__pycache__" -exec rm -rf {} +
	find . -name ".mypy_cache" -exec rm -rf {} +

lint:
	@$(RUN) flake8 --extend-exclude=$(EXCLUDES) .
	@$(RUN) mypy . $(MYPY_FLAGS) --exclude $(MYPY_EXCLUDES)

lint-strict:
	@$(RUN) flake8 --extend-exclude=$(EXCLUDES) .
	@$(RUN) mypy . $(MYPY_STRICT) --exclude $(MYPY_EXCLUDES) 

.PHONY: install run debug venv clean lint lint-strict
