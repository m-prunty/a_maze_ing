# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.de  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 13:25:26 by maprunty          #+#    #+#              #
#    Updated: 2026/05/10 09:55:48 by maprunty        ###   ########.fr        #
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



.PHONY: install run debug clean lint lint-strict build-mazegen

PYTHON     := uv run python3
MAIN       := a_maze_ing.py
CONFIG     := config.txt
MAZEGEN    := libs/mazegen

install:
	uv sync --no-dev

dev:
	uv sync --dev

run:
	$(PYTHON) $(MAIN) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(MAIN) $(CONFIG)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name "*.egg-info"  -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name "build" -exec rm -rf {} +
	find . -type d -name "resized" -exec rm -rf {} +
	find . -type f -name "*.pyc"       -delete
	rm -rf dist/

fclean: clean
	rm -rf .venv uv.lock wheels/

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . 

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

build-mazegen:
	uv build --package mazegen --wheel --out-dir wheels/


#
#
#
#SHELL := bash
#
#IMG_CACHE := includes/resized/*.png 
#
#RMFILES :=__pycache__ .*.sw* *.egg-info dist build $(IMG_CACHE) .venv uv.lock .mypy_cache .python-version
#
#CFG := FILENAME=config.txt\\nWIDTH=25\\nHEIGHT=25\\nENTRY=0,0\\nEXIT=0,25\
#\\nOUTPUT_FILE=maze.txt\\nPERFECT=True\\nPIC_SCALAR=1\\nPIC=[87, 81, 119, 20, 23]
#
#PYTHON=/usr/bin/python3
#
#.PHONY: run
#run: $(IMG_CACHE) ## Execute the main script. 
# 	uv run ./a_maze_ing.py
#	python3 main.py
#
#.PHONY: install
#install: ## Install dependencies
#	rm -rf wheels/*
#	$(PYTHON) -m pip install build #--break-system-packages
# 	$(PYTHON) -m pip uninstall common graphics mazegen
	# build libs
#	cd libs/common && $(PYTHON) -m build --wheel --outdir ../../wheels
#	$(PYTHON) -m pip install wheels/common*.whl --force-reinstall
#	
#	cd libs/graphics && $(PYTHON) -m build --wheel --outdir ../../wheels
#	cd libs/mazegen && $(PYTHON) -m build --wheel --outdir ../../wheels
#	cd libs/mlx/python && $(PYTHON) -m build --wheel --outdir ../../../wheels
#
	# install local deps
#	$(PYTHON) -m pip install wheels/graphics*.whl --force-reinstall
#	$(PYTHON) -m pip install wheels/mazegen*.whl --force-reinstall
#	$(PYTHON) -m pip install wheels/mlx*.whl --force-reinstall
#
#.PHONY: clean
#clean: ## Cleans up residual files
#	shopt -s globstar nullglob dotglob;\
#	$(foreach t,$(RMFILES),rm -rf **/**/$(t);)
#
##@ Utility
# lifted from:
# https://mmngreco.dev/posts/uv-makefile/
#.PHONY: help
#help:  ## Display this help
#	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make <target>\033[36m\033[0m\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
#
#.PHONY: mkconfig 
#mkconfig: ## mk config file from defaults defined at top of make 
#	echo -e $(CFG) > config.txt
#
#lint: 
#	flake8 . --exclude=libs/mlx 
#	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs  --exclude=libs/mlx
#
#.PHONY: uv
#uv:  ## Install uv if it's not present.
#	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
#
#.PHONY: dev
#dev: uv ## Install dev dependencies
#	uv sync --dev
#
#$(IMG_CACHE): ##tmp place to store imaages
#	mkdir -p $@
#
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
#
#.PHONY: build
#build:  ## Build package
#	uv build
#
