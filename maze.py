from cells import Cell
import time
import random
import sys

class Maze:
    def __init__(
        self,
        x1,
        y1,
        num_rows,
        num_cols,
        cell_size_x,
        cell_size_y,
        win=None,
        seed=None
    ):
        self.count = 0
        self.x1 = x1
        self.y1 = y1
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.cell_size_x = cell_size_x
        self.cell_size_y = cell_size_y
        self.win = win
        if seed:
            random.seed(seed)
        self._create_cells()
        self._break_entrance_and_exit()
        self._break_walls_r(0, 0)
        self._reset_cells_visited()

    def _create_cells(self):
        self._cells = []
        for i in range(0, self.num_cols):
            self._cells.append([])
            for j in range(0, self.num_rows):
                self._cells[i].append(Cell(self.win))
        
        for i in range(0, self.num_cols):
            for j in range(0, self.num_rows):
                self._draw_cell(i,j)

    def _draw_cell(self, i, j):
       x1 = self.x1 + i * self.cell_size_x
       x2 = self.x1 + (i + 1) * self.cell_size_x

       y1 = self.y1 + j * self.cell_size_y
       y2 = self.y1 + (j + 1) * self.cell_size_y

       self._cells[i][j].draw(x1,y1,x2,y2)
       self._animate()
    
    def _break_entrance_and_exit(self):
        entrance = self._cells[0][0]
        entrance.has_top_wall = False
        exit = self._cells[self.num_cols - 1][self.num_rows - 1]
        exit.has_bottom_wall = False
        self._draw_cell(0,0)
        self._draw_cell(self.num_cols - 1, self.num_rows - 1)

    def _break_walls_r(self, i, j):
        self._cells[i][j]._visited = True
        while True:
            # [up, right, down, left]
            ls = [(i, j - 1), (i + 1, j), (i, j + 1), (i - 1, j)]
            possible_dir = []
            for k in range(0, len(ls)):
                if self.can_move(ls[k]):
                    possible_dir.append(ls[k])
            if len(possible_dir) == 0:
                self._draw_cell(i,j)
                break
            dir = random.randrange(len(possible_dir))
            self._break_wall_between_cells(possible_dir[dir][0], possible_dir[dir][1], i, j)
            self._break_walls_r(possible_dir[dir][0], possible_dir[dir][1])

    def can_move(self, dir_tup):
        # not within bounds
        if (dir_tup[0] < 0 or dir_tup[0] >= len(self._cells) or 
            dir_tup[1] < 0 or dir_tup[1] >= len(self._cells[0])):
            return False
        # if cell has already been visited
        if self._cells[dir_tup[0]][dir_tup[1]]._visited:
            return False
        return True
    
    def can_move_no_wall(self, i, j, dir_tup):
        if dir_tup[0] == i + 1 and not self._cells[i][j].has_right_wall:
            return True
        if dir_tup[0] == i - 1 and not self._cells[i][j].has_left_wall:
            return True
        if dir_tup[1] == j + 1 and not self._cells[i][j].has_bottom_wall:
            return True
        if dir_tup[1] == j - 1 and not self._cells[i][j].has_top_wall:
            return True
        return False

            
    
    def _break_wall_between_cells(self,i, j, other_i, other_j):
        if other_i == i and other_j == j - 1:
            self._cells[i][j].has_top_wall = False
            self._cells[other_i][other_j].has_bottom_wall = False
        if other_i == i + 1 and other_j == j:
            self._cells[i][j].has_right_wall = False
            self._cells[other_i][other_j].has_left_wall = False
        if other_i == i and other_j == j + 1:
            self._cells[i][j].has_bottom_wall = False
            self._cells[other_i][other_j].has_top_wall = False
        if other_i == i - 1 and other_j == j:
            self._cells[i][j].has_left_wall = False
            self._cells[other_i][other_j].has_right_wall = False

    def _reset_cells_visited(self):
        for i in range(0, len(self._cells)):
            for j in range(0, len(self._cells[0])):
                self._cells[i][j]._visited = False

    def solve(self):
        return self._solve_r(0, 0)
    
    def _solve_r(self, i, j):
        self._animate()

        if i == len(self._cells) - 1 and j == len(self._cells[0]) - 1:
            return True
        
        self._cells[i][j]._visited = True
        # move right 
        if self.can_move((i + 1, j)) and self.can_move_no_wall(i, j, (i + 1, j)):
            self._cells[i][j].draw_move(self._cells[i + 1][j])
            if self._solve_r(i + 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i + 1][j], True)


        # move down
        if self.can_move((i, j + 1)) and self.can_move_no_wall(i, j, (i, j + 1)):
            self._cells[i][j].draw_move(self._cells[i][j + 1])
            if self._solve_r(i, j + 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j + 1], True)

        # move left
        if self.can_move((i - 1, j)) and self.can_move_no_wall(i, j, (i - 1, j)):
            self._cells[i][j].draw_move(self._cells[i - 1][j])
            if self._solve_r(i - 1, j):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i - 1][j], True)

        # move up 
        if self.can_move((i, j - 1)) and self.can_move_no_wall(i, j, (i, j - 1)):
            self._cells[i][j].draw_move(self._cells[i][j - 1])
            if self._solve_r(i, j - 1):
                return True
            else:
                self._cells[i][j].draw_move(self._cells[i][j - 1], True)

        return False

    def _animate(self):
        if self.win is None:
            return
        self.win.redraw()
        time.sleep(.05)
