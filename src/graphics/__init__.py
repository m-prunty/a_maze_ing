# *************************************************************************** #
#                                                                             #
#                                                        :::      ::::::::    #
#    __init__.py                                       :+:      :+:    :+:    #
#                                                    +:+ +:+         +:+      #
#    By: maprunty <maprunty@student.42heilbronn.d  +#+  +:+       +#+         #
#                                                +#+#+#+#+#+   +#+            #
#    Created: 2026/02/01 14:10:37 by maprunty         #+#    #+#              #
#    Updated: 2026/02/04 05:48:36 by maprunty        ###   ########.fr        #
#                                                                             #
# *************************************************************************** #


# from mlx import mlx
# from .mlx_context import Mlx_context
# from .engine.window import Window
# from .assets.textures import Textures

# __all__ = ["Mlx_context", "Window", "mlx", "Textures"]


from .render import Render

__all__ = ["Render"]