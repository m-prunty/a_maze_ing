#! /usr/bin/env python3
# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    a_maze_ing.py                                     :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: sdeppe <sdeppe@student.42heilbronn.de>    +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 01:26:52 by sdeppe           #+#    #+#              #
#    Updated: 2026/05/10 05:59:23 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #
"""Main file to run A-maze-ing."""

import os

RED = "\033[0;31m"
GREEN = "\033[0;32m"
PURPLE = "\033[0;35m"
LIGHT_BLUE = "\033[1;34m"
BOLD = "\033[1m"
END = "\033[0m"


# print("Current Python:", sys.executable)
# print("Virtual Environment:", venv_name)
# if venv_path:
#    print("Environment Path:", venv_path)
#    print(
#        f"\n{GREEN}SUCCESS{END}:"
#        + " You're in an isolated environment!\n"
#        + "Safe to install packages without affecting\n"
#        + "the global system.\n"
#    )
#    print("Package installation path:\n" + f"{BOLD}{sys.prefix}{END}")
# else:
#    print(
#        f"\n{RED}WARNING{END}:"
#        + " You're in the global environment!\n"
#        + "The machines can see everything you install.\n"
#    )
#    print(
#        "To enter the construct, run:\n"
#        + f"{BOLD}python -m venv matrix_env{END}\n"
#        + f"{BOLD}source matrix_env/bin/activate{LIGHT_BLUE} # On Unix{END}\n"
#        + f"{BOLD}matrix_env\\Scripts\\activate{LIGHT_BLUE}"
#        + f" # On Windows{END}\n"
#    )
#    print("Then run this program again.")
def not_venv_warning() -> str:
    return (
        f"\n{RED}WARNING{END}:"
        + "You're not in a virtual environment!\n"
        + "To enter the construct, run:\n"
        + (
            f"{BOLD}make install{END}\nfollowed by:\n"
            if not os.path.exists("./.venv")
            else ""
        )
        + f"{BOLD}make run{END}\n"
        + "or activate the venv manually:\n"
        + f"{BOLD}python -m venv .venv{END}\n"
        + f"{BOLD}source .venv/bin/activate{LIGHT_BLUE}"
    )


def main() -> None:
    print(
        f"\n{PURPLE}A_Maze_ing{END}:",
    )
    venv_path, venv_name = os.path.split(os.getenv("VIRTUAL_ENV", "None"))
    if venv_path:
        print("Welcome to the Maze")
        try:
            from src import Start

            start = Start()
            start.render_start()
        except Exception as e:
            print(f"Error during main loop: {e}")
    else:
        print(not_venv_warning())


if __name__ == "__main__":
    main()
