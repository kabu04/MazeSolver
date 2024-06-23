from window_draw import Line, Point

# knows which are walls (u,d,l,r)
# its pos in canvas
# access to window to draw itself
class Cell:
    def __init__(self, win) -> None:
        self.has_left_wall = True
        self.has_right_wall = True
        self.has_top_wall = True
        self.has_bottom_wall = True

        self._x1 = None
        self._x2 = None
        self._y1 = None
        self._y2 = None
        self._win = win
        self._visited = False
    
    # Draws the bordering walls of this cell
    def draw(self, x1, y1, x2, y2):
        if self._win is None:
            return
        self._x1 = x1
        self._y1 = y1
        self._x2 = x2
        self._y2 = y2

        line = Line(Point(x1, y1), Point(x1, y2))
        if self.has_left_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

        line = Line(Point(x1, y1), Point(x2, y1))
        if self.has_top_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")

        line = Line(Point(x2, y1), Point(x2, y2))
        if self.has_right_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")
            
        line = Line(Point(x1, y2), Point(x2, y2))
        if self.has_bottom_wall:
            self._win.draw_line(line, "black")
        else:
            self._win.draw_line(line, "white")


    def draw_move(self, to_cell, undo=False):
        if undo:
            line_color = "gray"
        else:
            line_color = "red"
        center_x, center_y = self.cell_center_coord()

        end_x, end_y = to_cell.cell_center_coord()

        line = Line(Point(center_x, center_y), Point(end_x, end_y))
        self._win.draw_line(line, line_color)
    
    def cell_center_coord(self):
        center_x = self._x1 + abs(self._x2 - self._x1)//2
        center_y = self._y1 + abs(self._y2 - self._y1)//2
        return center_x, center_y