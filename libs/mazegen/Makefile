# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.de  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/05/23 20:32:31 by maprunty          #+#    #+#              #
#    Updated: 2026/05/23 23:06:06 by maprunty        ###   ########.fr        #
#                                                                              #
# **************************************************************************** #
.PHONY: all dev build test clean fclean

build:
	uv build

dev:
	uv sync --dev

test: dev
	uv run pytest

clean:
	rm -rf build dist *.egg-info
	rm -rf .pytest_cache .mypy_cache __pycache__ *.sw*

fclean: clean
	rm -rf .venv uv.lock

all: dev test build
