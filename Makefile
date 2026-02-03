# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.de  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 13:25:26 by maprunty          #+#    #+#              #
#    Updated: 2026/02/02 09:34:46 by maprunty        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
# • install: Install project dependencies using pip, uv, pipx, or any other package
# manager of your choice.
# • run: Execute the main script of your project (e.g., via Python interpreter).
# • debug: Run the main script in debug mode using Python’s built-in debugger (e.g.,
# pdb).
# • clean: Remove temporary files or caches (e.g., __pycache__, .mypy_cache) to
# keep the project environment clean
# • lint: Execute the commands flake8 . and mypy . --warn-return-any
# --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs
# --check-untyped-defs
# • lint-strict (optional): Execute the commands flake8 . and mypy . --strict
SHELL := bash
RMFILES=resized __pycache__ .*.sw* 

.PHONY: run
run:  ## Execute the main script. 
	uv run ./a-maze-ing.py

.PHONY: install
install: uv dev## Install dependencies using uv
	uv sync --frozen
	uv pip install -e .

.PHONY: clean
clean: ## Cleans up residual files
	shopt -s globstar nullglob dotglob;\
	$(foreach t,$(RMFILES),rm -rf **/**/$(t);)

##@ Utility
# lifted from:
# https://mmngreco.dev/posts/uv-makefile/
.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)


.PHONY: uv
uv:  ## Install uv if it's not present.
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh

.PHONY: dev
dev: uv ## Install dev dependencies
	uv sync --dev

# .PHONY: lock
# lock: uv ## lock dependencies
# 	uv lock
# 
# .PHONY: test
# test:  ## Run tests
# 	uv run pytest
# 
# .PHONY: lint
# lint:  ## Run linters
# 	uv run ruff check ./src ./tests
# 
# .PHONY: fix
# fix:  ## Fix lint errors
# 	uv run ruff check ./src ./tests --fix
# 	uv run ruff format ./src ./tests
# 
# .PHONY: cov
# cov: ## Run tests with coverage
# 	uv run pytest --cov=src --cov-report=term-missing
# 
# .PHONY: doc
# doc:  ## Build documentation
# 	cd docs && uv run make html

.PHONY: build
build:  ## Build package
	uv build

