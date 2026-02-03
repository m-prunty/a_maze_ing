from a_maze import A_Maze

class Options():
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        
    def parse_config(self):
    	print(A_Maze.cfg_from_file("config.txt"))
     
    # def reset_siz(self, width: int, height: int):
	# 	self.width = width
	# 	self.height = height


# def reset_grid()


if __name__ == "__main__":
    opt = Options(100, 100)
    opt.parse_config()