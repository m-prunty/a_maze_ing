# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.de  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 13:25:26 by maprunty          #+#    #+#              #
#    Updated: 2026/05/24 03:15:48 by maprunty         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

.PHONY: install run debug clean lint lint-strict build-mazegen

PYTHON     := uv run python3
MAIN       := a_maze_ing.py
CONFIG     := config.txt
MAZEGEN    := libs/mazegen

install:
	uv sync --no-dev

dev: fclean build-mazegen
	uv sync --dev --reinstall-package mazegen

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

fclean: clean
	find . -type d -name ".venv" -exec rm -rf {} +
	find . -type d -name "wheels" -exec rm -rf {} +
	find . -type d -name "dist" -exec rm -rf {} +
	find . -type f -name ".whl" -exec rm -rf {} +
	find . -type f -name "uv.lock" -exec rm -rf {} +
	find . -type f -name "*.sw*" -exec rm -rf {} +

lint:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . 

lint-strict:
	$(PYTHON) -m flake8 .
	$(PYTHON) -m mypy . --strict

build-mazegen:
	rm -f *.whl
	cd $(MAZEGEN) && uv build --package mazegen --wheel --out-dir ../..

